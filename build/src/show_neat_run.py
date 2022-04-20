import os
import pickle
import neat
from OrbitEnvNoGFX import OrbitEnv
from OrbitEnv import OrbitEnv

"""
give credit to sentdex and gh library
"""
# model_name = ""
# model_folder = ""

model_folder = ""
# model_folder = "NeuroEvolution/models"
# model_name = ""
model_name = "../../data/neat/models/neat-checkpoint-3"

with open(f'data/neat/models/winner1648952884.8555834', 'rb') as f:
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
# setattr(env.collector, "file_to_use", f"data_neat")
# setattr(env.collector, "model_type", f"neat")
observation = env.reset()

done = False
for i in range(100):
    while not done:
        action = net.activate(observation)

        observation, reward, done, info = env.step(action)
        print(f"Done. reward: {reward}")
    done = False
    env.reset()