import os
import pickle
import neat
import helpers
from OrbitEnvNoGFX import OrbitEnv
# from OrbitEnv import OrbitEnv
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


if __name__ == "__main__":

    # neat1
    path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_1"
    agent_1_path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_1/winner08281650"
    filepath_data = f"{path}/data_neat.csv"
    filepath_setup = f"{path}/setup_neat.csv"
    df_neat = helpers.create_dataframe(filepath_data, filepath_setup)

    filt, filter_conditions = helpers.get_random_filters_given_columns(df_neat)
    helpers.average_reward_given_filters(df_neat, filt)

    # neat2
    path_2 = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_2"
    agent_2_path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_2/winner08281656"
    filepath_data_2 = f"{path_2}/data_neat.csv"
    filepath_setup_2 = f"{path_2}/setup_neat.csv"
    df_neat_2 = helpers.create_dataframe(filepath_data_2, filepath_setup_2)

    # neat3
    path_3 = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_3"
    agent_3_path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_3/winner08281737"
    filepath_data_3 = f"{path_3}/data_neat.csv"
    filepath_setup_3 = f"{path_3}/setup_neat.csv"
    df_neat_3 = helpers.create_dataframe(filepath_data_3, filepath_setup_3)

    # This loop is copied from the do_reinforcement_learning_runs.py file. Which comes from another tutorial
    num_loops = 10
    for i in range(num_loops):
        while not done:
            action = net.activate(observation)
            observation, reward, done, info = env.step(action)
            # print(f"{i} Done. reward: {reward}")

        done = False

        # env.reset() # reset. we now Know the initial conditions
        obs = env.reset() # reset. we now Know the initial conditions
        print(obs)
        # ============================================================================

        subdomain_analysis = helpers.superior_agent_in_subdomain(df_neat_2, df_neat_3, 100)
        best_agent_path = helpers.agent_selection_component(subdomain_analysis, obs, agent_2_path, agent_3_path)
        print(f"This run uses the agent location at: \n{best_agent_path}\n")

        with open(f'{best_agent_path}', 'rb') as f:
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

    print(f"\n\nThat took {round((helpers.current_time() - start_time)/60, 2)}m")
    print(f"that was {num_loops} loops.")

