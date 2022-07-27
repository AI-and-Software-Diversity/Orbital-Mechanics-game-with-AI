"""
give credit to sentdex and gh library
"""

import multiprocessing
import os
import pickle
# from datetime import time
import time
import neat
import numpy as np
import gym
hpc = True

from OrbitEnv import OrbitEnv
from OrbitEnvNoGFX import OrbitEnv


runs_per_net = 3
env = OrbitEnv(mode="neat")

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):

        observation = env.reset()
        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        done = False
        while not done:

            action = net.activate(observation)
            observation, reward, done, info = env.step(action)

            fitness += reward

        fitnesses.append(fitness)

    # The genome's fitness is its mean performance across all runs.
    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)

    path_to_models = "data/neat/models"

    pop = neat.Population(config)
    callbacks = neat.Checkpointer(generation_interval=1, filename_prefix=f"{path_to_models}/neat-checkpoint-")
    stats = neat.StatisticsReporter()

    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    # pop.add_reporter(neat.Checkpointer(True))
    # pop.add_reporter(callbacks)

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open(f'{path_to_models}/winner{time.strftime("%m%d%H%M")}', 'wb') as f:
        pickle.dump(winner, f)

    stats.save()
    print(winner)

def continue_from_checkpoint(checkpoint_name, n_runs=0):



    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)

    pop = neat.Population(config)
    cb = neat.Checkpointer(generation_interval=2)
    # checkpoint_name = "neat-checkpoint-9 zipped"
    # checkpoint_name = "neat-checkpoint-19 zipp"
    pop = cb.restore_checkpoint(checkpoint_name)
    pop.add_reporter(neat.StdOutReporter(True))
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    # To train according to config specs
    if n_runs < 1:
        winner = pop.run(pe.evaluate)
    else:
        winner = pop.run(pe.evaluate, n_runs)

    # Save the winner.
    with open("data/neat/models/"+checkpoint_name+"-checkpoint", 'wb') as f:
        pickle.dump(winner, f)

    print(winner)



if __name__ == '__main__':
    run()
