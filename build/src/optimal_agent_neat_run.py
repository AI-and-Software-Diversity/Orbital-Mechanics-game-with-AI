import os
import pickle
import neat
import helpers
# from OrbitEnvNoGFX import OrbitEnv
from OrbitEnv import OrbitEnv


"""
Code to implement neuro evolution comes from the Neat-python library as well as the Sentdex youtube channel.
This file was edited from the code in neuro_evolution.py

https://github.com/CodeReclaimers/neat-python/tree/master/examples
https://www.youtube.com/watch?v=ZC0gMhYhwW0
"""

# Get the observation
env = OrbitEnv(mode="neat")
observation = env.reset()


# Specify what model you choose
model_folder = "data/neat/models"
model_name = "winner04251728"


string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/data/neat/models/winner07260118"
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



done = False
start_time = helpers.current_time()

# This loop is copied from the reinforcement_learning.py file. Which comes from another tutorial
num_loops = 10_000
num_loops = 2
for i in range(num_loops):
    while not done:
        action = net.activate(observation)

        observation, reward, done, info = env.step(action)
        # print(f"{i} Done. reward: {reward}")
    done = False
    # reset. we now how tthe initial conditions
    env.reset()
    # observation, reward, done, info = env.step(action)

print(f"that was {num_loops} loops.")
print(f"\n\nThat took {(helpers.current_time() - start_time)/60}m")

