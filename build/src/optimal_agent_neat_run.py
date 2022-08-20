import os
import pickle
import neat
import helpers
# from OrbitEnvNoGFX import OrbitEnv
from OrbitEnv import OrbitEnv
import matplotlib.pyplot as plt
import numpy as np
import helpers as h
import pandas as pd
import random
"""
Code to implement neuro evolution comes from the Neat-python library as well as the Sentdex youtube channel.
This file was edited from the code in neuro_evolution.py

https://github.com/CodeReclaimers/neat-python/tree/master/examples
https://www.youtube.com/watch?v=ZC0gMhYhwW0
"""

#################
# INITIAL SETUP #
#################

# Get the observation
env = OrbitEnv(mode="neat")
observation = env.reset()

# Specify what model you choose
model_folder = "data/neat/models"
model_name = "winner07260118"

with open(f'{model_folder}/{model_name}', 'rb') as f:
    agent = pickle.load(f)


# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

net = neat.nn.FeedForwardNetwork.create(agent, config)

done = False
start_time = helpers.current_time()
#####################
# INITIAL SETUP END #
#####################

#####################
# SUBDOMAIN METHODS #
#####################

def create_dataframe(filepath_data, filepath_setup):
    """
    Takes the data and setup CSVs and combines them into 1 larger csv.
    """

    df_1 = pd.read_csv(filepath_data, sep=',')
    df_2 = pd.read_csv(filepath_setup, sep=',')


    #reference for concat: https://www.youtube.com/watch?v=iYWKfUOtGaw
    df_rl = pd.concat([df_1, df_2], axis=1)
    df_rl.columns = df_rl.columns.str.replace(' ', '')

    return df_rl

def filtered_df(df, cols, i, operator, pivot):
    """
    params: The parameters are the totality of the information required to filter the dataframe
    """

    if operator == ">":
        return (df[cols[i]] > pivot)
    else:
        return (df[cols[i]] <= pivot)

def get_random_filters_given_columns(dataframe):
    """
    Using the column titles, and the min/max of the column,
    this function returns a random boolean condition or filter
    """

    #     list of the columns
    #     lists of the min/max value of each column

    excluded_cols = ['wassuccesful',
                     'reward',
                     'actualsteps',
                     'targetsteps',
                     'runscompleted',
                     'length',
                     'height']

    cols = [col for col in dataframe.columns if col not in excluded_cols]
    i = random.randint(0,len(cols)-1)

    maxs = [dataframe[col].max() for col in cols]
    mins = [dataframe[col].min() for col in cols]

#     print(i)
#     print(maxs)
#     print(mins)

    filt_info = []
    pivot = random.randint(mins[i],
                           maxs[i])
    b = random.randint(0,1)

    if b == 0:
#         filt = (dataframe[cols[i]] > pivot)
        filt = filtered_df(dataframe, cols, i, ">", pivot)

        filt_info.append((dataframe, cols, i, ">", pivot))
#         print(f"{cols[i]}>{pivot}")
    else:
#         filt = (dataframe[cols[i]] <= pivot)
        filt = filtered_df(dataframe, cols, i, "<=", pivot)
        filt_info.append((dataframe, cols, i, "<=", pivot))
#         print(f"{cols[i]}<={pivot}")


    return filt, filt_info

def average_reward_given_filters(dataframe, fltr):
    """

    @Description: Given a table of data (like a csv or a dataframe) it finds the average
    reward after filtering the table


    """

    # filter the dataframe
    # reference fro loc: https://www.youtube.com/watch?v=Lw2rlcxScZY
    df_avg = dataframe.loc[fltr, 'reward']
#     print(pd.DataFrame(df_avg))


    # get the average of those that meet our conditions
    avg_reward = np.mean(df_avg)

    return avg_reward

# rl11
path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/agents/2_star_2_planet/rl1"
filepath_data = f"/{path}/data_rlearn.csv"
filepath_setup = f"/{path}/setup_rlearn.csv"

df_rl = create_dataframe(filepath_data, filepath_setup)
filt, _ = get_random_filters_given_columns(df_rl)
average_reward_given_filters(df_rl, filt)

def sub_domain_search(df_agent_1, agent_1, df_agent_2, agent_2):

    fitness_subdomain_winner = []

    # 1. You have two CSVs containing data that corresponds to two agents.
    # via params

    # you ensure each data tihng has the same columns
    if list(df_agent_1.columns) != list(df_agent_2.columns):
        raise Exception("These dataframes have different columns and cannot be compared. Perhaps the corresponding agents were trained with different inputs?")


    # 4. You create one or many random filters given the columns from the parameter, and the min/max of those columns.
    filt, filt_conditions = get_random_filters_given_columns(df_agent_1)

    #  check the performance of each agent in chosen filter
    agent_1_performance = average_reward_given_filters(df_agent_1, filt)
    agent_2_performance = average_reward_given_filters(df_agent_2, filt)

    difference = np.abs(agent_1_performance - agent_2_performance)

    # 6. You record all of the filters and which CSV has a higher reward (in a tuple like: Tuple[filter_conditions, better] ).
    if agent_1_performance >= agent_2_performance:
        fitness_subdomain_winner.append((difference, filt_conditions, agent_1))
    else:
        fitness_subdomain_winner.append((difference, filt_conditions, agent_2))

#     print(fitness_subdomain_winner)
#     print(fitness_subdomain_winner[0][0])
#     print(np.array(fitness_subdomain_winner).shape)

    # put biggest differences at the top of the list
#     fitness_subdomain_winner = fitness_subdomain_winner.sort()
#     fitness_subdomain_winner = fitness_subdomain_winner.reverse()

    return fitness_subdomain_winner

def auto_sub_domain_search(df_agent_1, df_agent_2, num_checks):
    """
    @param df_agent_1: dataframe of agent 1
    @param df_agent_2: dataframe of agent 2
    @param num_checks: number of checks to perform

    @return: Returns a List of tuples with N values. Each tuple contains the fitness, filter conditions and superior agent for a random subdomain.

    """
    fitness_subdomain_winner = []

    # 1. You have two CSVs containing data that corresponds to two agents.
    # via params

    # you ensure each data tihng has the same columns
    if list(df_agent_1.columns) != list(df_agent_2.columns):
        raise Exception("These dataframes have different columns and cannot be compared. Perhaps the corresponding agents were trained with different inputs?")

    # 7. You do this check N times.
    for i in range(num_checks):

        # 4. You create one or many random filters given the columns from the parameter, and the min/max of those columns.
        filt, filt_conditions = get_random_filters_given_columns(df_agent_1)

        #  check the performance of each agent in chosen filter
        agent_1_performance = average_reward_given_filters(df_agent_1, filt)
        agent_2_performance = average_reward_given_filters(df_agent_2, filt)

        difference = np.abs(agent_1_performance - agent_2_performance)

        # 6. You record all of the filters and which CSV has a higher reward (in a tuple like: Tuple[filter_conditions, better] ).
        if agent_1_performance >= agent_2_performance:
            fitness_subdomain_winner.append((difference, filt_conditions, "agent_1"))
        else:
            fitness_subdomain_winner.append((difference, filt_conditions, "agent_2"))

    return fitness_subdomain_winner

discovered_subdomains = auto_sub_domain_search(df_rl, df_rl, 3)
for i in discovered_subdomains:
    print("="*500)
    print("#"*500)
    print("="*500)
    print(i[0])
    print(i[2])
    print()
    print()

#########################
# SUBDOMAIN METHODS END #
#########################



# This loop is copied from the reinforcement_learning.py file. Which comes from another tutorial
num_loops = 0
for i in range(num_loops):
    while not done:
        action = net.activate(observation)
        observation, reward, done, info = env.step(action)
        # print(f"{i} Done. reward: {reward}")

    done = False

    # reset. we now Know the initial conditions
    env.reset()

    # ============================================================================

    # First we get dataframes containing data about all of the AIs used
    df_1 = None
    df_2 = None

    # We choose a filter that we have investigated in the past

    # Using the observation from env.reset(), we check what f



    # We then ask ourselves find out where the current run lies relative to the filter (pivot)
    # a = fitler(df_1)
    # b = filter(df_2)

    # then apply it to the dataframes from each model


    # now we choose the winner and load it

    print("choosing new agent")
    model_folder = "data/neat/models"
    model_name = "winner07260118"

    with open(f'{model_folder}/{model_name}', 'rb') as f:
        agent = pickle.load(f)

    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    net = neat.nn.FeedForwardNetwork.create(agent, config)

    # ============================================================================



print(f"that was {num_loops} loops.")
print(f"\n\nThat took {(helpers.current_time() - start_time)/60}m")

