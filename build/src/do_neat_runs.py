import os
import pickle
import neat
import helpers
from OrbitEnvNoGFX import OrbitEnv
# from OrbitEnv import OrbitEnv


"""
Code to implement neuro evolution comes from the Neat-python library as well as the Sentdex youtube channel.
This file was edited from the code in neuro_evolution.py

https://github.com/CodeReclaimers/neat-python/tree/master/examples
https://www.youtube.com/watch?v=ZC0gMhYhwW0
"""

# model_folder = "data/neat/models"
# model_name = "winner04251728"


# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_1/winner08281650"
# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_2/winner08281656"
# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_3/winner08281737"

# 25/1000
# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/winner04032321"
# 58/1000
# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/winner04032314"
# 49/1000
# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/winner04030437"


# 150/1000
string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/winner04032324"
# 195/1000
# string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/winner04040105"

with open(f'{string}', 'rb') as f:
    agent = pickle.load(f)


# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

net = neat.nn.FeedForwardNetwork.create(agent, config)

env = OrbitEnv(mode="neat")
observation = env.reset()

done = False
start_time = helpers.current_time()

# This loop is copied from the do_reinforcement_learning_runs.py file. Which comes from another tutorial
num_loops = 1000
for i in range(num_loops):
    while not done:
        action = net.activate(observation)

        observation, reward, done, info = env.step(action)
        # print(f"{i} Done. reward: {reward}")
    done = False
    env.reset()

print(f"that was {num_loops} loops.")
print(f"\n\nThat took {(helpers.current_time() - start_time)/60}m")
import numpy as np

# print(np.mean(helpers.get_collumn_from_csv(
#     "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/data/neat/csvs/data_neat.csv", 1)))
from collections import Counter

print(())

results = Counter(helpers.get_collumn_from_csv(
    "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/data/neat/csvs/data_neat.csv", 0))

print(results[1])










