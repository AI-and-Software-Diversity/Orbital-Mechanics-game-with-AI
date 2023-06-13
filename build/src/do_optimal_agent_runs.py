import stable_baselines3
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.logger import configure
import logging
import time
# from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import *
import data_handler
import os
import pickle
import neat
import helpers
from OrbitEnvNoGFX import OrbitEnv
# from OrbitEnv import OrbitEnv

if __name__ == '__main__':
    done = False
    start_time = time.time().real
    print(f"{time.strftime('%d%m(%H:%M)')}")
    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
    env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, vec_env_cls=DummyVecEnv)
    obs = env.reset()

    # neat agent
    # path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_1"
    agent_1_path = f"/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/winner04040105"

    filepath_data = 'data/neat/csvs/data_neat.csv'
    filepath_setup = 'data/neat/csvs/setup_neat.csv'
    df_neat = helpers.create_dataframe(filepath_data, filepath_setup)

    # rl agent
    # path_2 = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/rl_2"
    agent_2_path = f"data/rlearn/models (copy)/model18920-2703(04:46)"
    filepath_data_2 = f'data/rlearn/csvs/data_rlearn.csv'
    filepath_setup_2 = f'data/rlearn/csvs/data_setup.csv'
    df_rl = helpers.create_dataframe(filepath_data_2, filepath_setup_2)

    filt, filter_conditions = helpers.get_random_filters_given_columns(df_neat)
    # helpers.average_reward_given_filters(df_neat, filt)
    custom_objects = {'lr_schedule': lambda _: None, 'clip_range': lambda _: None}

    model = PPO.load(agent_2_path, custom_objects=custom_objects)
    done = False

    subdomain_analysis = helpers.superior_agent_in_subdomain_old(df_neat, df_rl, 100)
    # best_agent_path, agent_type = helpers.ASC_neat_rl(subdomain_analysis, obs, agent_1_path, agent_2_path)
    print(subdomain_analysis[0])
#
#     n_runs = 10
#     for i in range(n_runs):
#
#         while not done:
#             action, _states = model.predict(obs, deterministic=True)
#             obs, reward, done, info = env.step(action)
#
#         done = False
#
#         print(f"{i} Done. reward: {reward}")
#         obs = env.reset()
#         print(obs)
#
#         # ============================================================================
#         subdomain_analysis = helpers.superior_agent_in_subdomain_old(df_neat, df_rl, 100)
#         best_agent_path, agent_type = helpers.ASC_neat_rl(subdomain_analysis, obs, agent_1_path, agent_2_path)
#
#         print(f"This run uses the agent location at: \n{best_agent_path}\n")
#
#         if agent_type == "neat":
#             print(f"This run uses the agent location at: \n{best_agent_path}\n")
#
#             with open(f'{best_agent_path}', 'rb') as f:
#                 agent = pickle.load(f)
#
#             # Load the config file, which is assumed to live in
#             # the same directory as this script.
#             local_dir = os.path.dirname(__file__)
#             config_path = os.path.join(local_dir, 'config')
#             config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                                  config_path)
#
#             net = neat.nn.FeedForwardNetwork.create(agent, config)
#
#         elif agent_type == "rl":
#             custom_objects = {'lr_schedule': lambda _: None, 'clip_range': lambda _: None}
#             model = PPO.load(best_agent_path)
#             # model = PPO.load(agent_2_path, env=OrbitEnv(mode="rlearn"))
#         # ============================================================================
#
#     env.close()
#     print(f"\n\nThat took {round((helpers.current_time() - start_time) / 60, 2)}m")
# #