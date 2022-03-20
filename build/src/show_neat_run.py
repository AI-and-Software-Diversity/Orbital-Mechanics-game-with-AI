import os
import pickle
import neat
import numpy as np
# load the winner
from OrbitEnv import OrbitEnv

"""
give credit to sentdex and gh library
"""
# model_name = ""
# model_folder = ""

model_folder = ""
# model_folder = "NeuroEvolution/models"
# model_name = ""
model_name = "neat-checkpoint-8-checkpoint"

with open(f'{model_name}', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)

env = OrbitEnv()
observation = env.reset()

done = False

while not done:
    action = net.activate(observation)
    observation, reward, done, info = env.step(action)
    # env.render()