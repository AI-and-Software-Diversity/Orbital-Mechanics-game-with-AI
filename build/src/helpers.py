import pygame
import logging
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


def euclidian_distance(body1, body2):
    """
    Finds the Euclidean distance between two bodies.
    """

    distance = np.abs(np.linalg.norm(
        np.array([body1.x, body1.y]) - np.array([body2.x, body2.y])
    ))

    return distance

def text_box(str, font_size, screen, x, y):
    """
    Draws text on the screen.

    Reference: https://www.fontspace.com/press-start-2p-font-f11591
    """

    font = pygame.font.Font('assets/PressStart2P-vaV7.ttf', font_size)
    text = font.render(str, True, (255,255,255))
    screen.blit(text, (x, y))

def law_of_gravitation(body1, body2):

    """
    We calculate the force of body 1 applies on body 2 on each body newtonian mechanics
    The pull body1 applies to body2
    F_12 = G(m_1 * m_2/r^2)
    https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

    The specific method used was the Euler-Cromer method
    https://www.youtube.com/watch?v=rPkJtpVJwSw&list=PLdCdV2GBGyXOOutOEKggaZo1rCHtUYh-A

    Which followed this tutorial
    https://www.youtube.com/watch?v=4ycpvtIio-o&list=PLdCdV2GBGyXOExPW4u8H88S5mwrx_8vWK&index=2
    """

    # if body1 == body2:
    #     return 0

    if body1.mass != 0 and body2.mass != 0 and body1 != body2:
        if body1 == body2:
            raise Exception("The bodies can not be the same")

        G = 400
        r_vec = np.array([body1.x, body1.y])-np.array([body2.x, body2.y])
        r_mag = np.linalg.norm((np.array([body1.x, body1.y])-np.array([body2.x, body2.y])))
        r_hat = r_vec/r_mag

        try:
            F_mag = G * body1.mass * body2.mass / r_mag**2
        except ZeroDivisionError as err:
            logging.error(err)

        F_vector = F_mag * r_hat

        return F_vector
    else:
        return 0

def current_time():
    """Returns the current time"""
    return round(time.time().real, 2)

def all_planets_destroyed(pnts):
    """Returns true if all planets are destroyed."""
    if len([pnt for pnt in pnts if pnt.alive == False]) == len([pnt for pnt in pnts]):
        return True
    return False

def scale_vectors(vec1, vec2, factor):
    """
    :param vec1: The initial vector (point in space)
    :param vec2: The seconds vector (point in space)
    :return factor: The scaled difference between them (route from vex 2 to vec 1)
    """
    resultant_vec = (np.array(vec1) - np.array(vec2)) / 500_000

    return (resultant_vec) * factor

def not_created_yet():
    print("THIS HAS NOT YET BEEN IMPLEMENTED")

def get_collumn_from_csv(file, chosen_col):
    """
    Returns a numpy array of data from a csv column (Not including the first line read)

    file: the filepath of the csv
    chosen_col: the index of the column you want
    index's:
        0:was successful,
        1:reward,
        2:actual
        3:steps,
        4:target steps,
        5:runs completed
    """

    import pandas as pd

    df = pd.read_csv(file)

    full_col = df.to_numpy().transpose()[chosen_col]
    # print(col[-1])

    return np.array(full_col)

def get_rlearn_graph(data, timesteps):
    """
    Creaates a graph that emulates tensorboard graphs.
    Timesteps Describes how many runs are collated into one datapoint.

    Reference: https://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
    """
    aves = [np.mean(data[i:i + timesteps + 1]) for i in range(0, len(data), timesteps)]
    print(len(aves))
    plt.plot(range(0, len(aves)), aves)
    plt.show()

def setup_csv(num_planets, num_stars):
    """
    Automatically creates the title row for setup_csv's given #planets and #stars
    """
    title_string = ""

    for i in range(num_stars):
        title_string = title_string + f"star_{i+1}_x_pos,"

    for i in range(num_stars):
        title_string = title_string + f"star_{i+1}_y_pos,"

    for i in range(num_stars):
        title_string = title_string + f"star_{i+1}_m,"

    for i in range(num_planets):
        title_string = title_string + f"planet_{i+1}_m,"

    title_string = title_string + "length,height"

    return title_string

def pred_csv(num_planets):
    """
    Automatically creates the title row for pred_csv's given #planets
    """

    title_string = ""
    for i in range(num_planets):
        title_string = title_string + f"planet_{i+1}_x_pos,planet_{i+1}_y_pos,planet_{i+1}_x_mom,planet_{i+1}_y_mom,"
    title_string = title_string[0:-1]

    return title_string


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

    filt_info = []
    pivot = random.randint(mins[i],
                           maxs[i])
    b = random.randint(0,1)

    if b == 0:
        filt = filtered_df(dataframe, cols, i, ">", pivot)

        filt_info.append((dataframe, cols, i, ">", pivot))
#         print(f"{cols[i]}>{pivot}")
    else:
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

def agent_selection_component(subdomain_analysis, observation, agent_1_path, agent_2_path):

    #
    subdomain_winners_reward = [subdomain[0] for subdomain in subdomain_analysis]
    subdomain_winner = [subdomain[2] for subdomain in subdomain_analysis]
    subdomain_conditions = [subdomain[1][0] for subdomain in subdomain_analysis]

    #
    agent_1_points = 0
    agent_2_points = 0

    for i in range(len(subdomain_conditions)):

        if subdomain_winner[i] == "agent_1":
            agent_1_points += 1

        elif subdomain_winner[i] == "agent_2":
            agent_2_points += 1

        else:
            raise Exception("ASC malfunction: Invalid Agent specified")

    print(f"Agent 1 had {agent_1_points} points\nAgent 2 had {agent_2_points} points")

    if agent_1_points >= agent_2_points:
        return agent_1_path

    else:
        return agent_2_path

def superior_agent_in_subdomain(df_agent_1, df_agent_2, num_checks):

    """
    This function compares 2 agents in N subdomains and lets you know which agent is best.

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
        filt, filt_conditions = get_random_filters_given_columns(df_agent_2)

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

def ASC_neat_rl(subdomain_analysis, observation, neat_agent_path, rl_agent_path):

    #
    subdomain_winners_reward = [subdomain[0] for subdomain in subdomain_analysis]
    subdomain_winner = [subdomain[2] for subdomain in subdomain_analysis]
    subdomain_conditions = [subdomain[1][0] for subdomain in subdomain_analysis]

    #
    neat_agent_points = 0
    rl_agent_points = 0

    for i in range(len(subdomain_conditions)):

        if subdomain_winner[i] == "agent_1":
            neat_agent_points += 1

        elif subdomain_winner[i] == "agent_2":
            rl_agent_points += 1

        else:
            raise Exception("ASC malfunction: Invalid Agent specified")

    print(f"The neat agent had {neat_agent_points} points\nThe rl agent had {rl_agent_points} points")

    if neat_agent_points >= rl_agent_points:
        return neat_agent_path, "neat"

    else:
        return rl_agent_path, "rl"

#########################
# SUBDOMAIN METHODS END #
#########################

if __name__ == '__main__':
    # neat_values = get_collumn_from_csv(
    #     file="data/neat/csvs/data_neat.csv",
    #     chosen_col=0,
    #     show_graph=True
    # )
    #
    # i = 0
    # for val in neat_values:
    #     if val == 1:
    #         i+=1
    # print(i)

    arr1 = get_collumn_from_csv("/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_1/data_neat.csv", 1)
    arr2 = get_collumn_from_csv("/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_2/data_neat.csv", 1)
    arr3 = get_collumn_from_csv("/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_3/data_neat.csv", 1)
    arr23 = get_collumn_from_csv("/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_2_neat_3/data_neat.csv", 1)

    # plt.xlabel("run")
    # plt.ylabel("Reward")
    # plt.title("Reward/Batch")
    # get_rlearn_graph(arr, 100_000)
    # plt.show()

    print(f"Mean for 1 is:     {np.mean(arr1)}")
    print(f"Mean for 2 is:     {np.mean(arr2)}")
    print(f"Mean for 3 is:     {np.mean(arr3)}")
    print(f"Mean for 23 is:    {np.mean(arr23)}")
    # print(setup_csv(2,2))
    print(get_rlearn_graph(get_collumn_from_csv(
        "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/data/rlearn/csvs/data_rlearn.csv", 1), 784*1))

    # print(get_rlearn_graph(get_collumn_from_csv("/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/data_rlearn.csv", 1),784))
    # plt.plot([1, 2, 3], [5, 7, 4])
    # plt.show()
