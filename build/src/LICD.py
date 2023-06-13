import numpy as np
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

    # = competence variation ==========================================================================================

    # # ppo agent 1
    # agent_1_path = f"PRESENTATION_DATA/competence_variation/master/1Amodel84-2303(04:14).zip"
    # filepath_data = f"PRESENTATION_DATA/competence_variation/master/1A/data_rlearn.csv"
    # filepath_setup = f"PRESENTATION_DATA/competence_variation/master/1A/setup_rlearn.csv"
    # df_rl = helpers.create_dataframe(filepath_data, filepath_setup)
    #
    # # ppo agent
    # agent_2_path = f"PRESENTATION_DATA/competence_variation/master/2Amodel87-2403(14:36).zip"
    # filepath_data_2 = f'PRESENTATION_DATA/competence_variation/master/2A/data_rlearn.csv'
    # filepath_setup_2 = f'PRESENTATION_DATA/competence_variation/master/2A/setup_rlearn.csv'
    # df_rl_2 = helpers.create_dataframe(filepath_data_2, filepath_setup_2)
    # print(f"CHECKPOINT"*20)

    # # ppo agent 2
    agent_3_path = f"PRESENTATION_DATA/competence_variation/master/1Bmodel114-2303(12:30).zip"
    filepath_data_3 = f"PRESENTATION_DATA/competence_variation/master/1B/data_rlearn.csv"
    filepath_setup_3 = f"PRESENTATION_DATA/competence_variation/master/1B/setup_rlearn.csv"
    df_rl_3 = helpers.create_dataframe(filepath_data_3, filepath_setup_3)
    # # ppo agent
    agent_4_path = f"PRESENTATION_DATA/competence_variation/master/2Bmodel156-2503(10:49).zip"
    filepath_data_4 = f'PRESENTATION_DATA/competence_variation/master/2B/data_rlearn.csv'
    filepath_setup_4 = f'PRESENTATION_DATA/competence_variation/master/2B/setup_rlearn.csv'
    df_rl_4 = helpers.create_dataframe(filepath_data_4, filepath_setup_4)
    # print(f"CHECKPOINT"*20)
    # # ============================================================================================




    # = different method neat stuff ===========================================================================================
    agent_1_path = f"build/PRESENTATION_DATA/different_methods/winner04032324"
    filepath_data_neat = 'PRESENTATION_DATA/different_methods/324data_neat.csv'
    filepath_setup_neat = 'PRESENTATION_DATA/different_methods/324setup_neat.csv'
    df_neat = helpers.create_dataframe(filepath_data_neat, filepath_setup_neat)

    agent_2_path = f"PRESENTATION_DATA/different_methods/winner04040105"
    filepath_data_neat_2 = 'PRESENTATION_DATA/different_methods/105data_neat.csv'
    filepath_setup_neat_2 = 'PRESENTATION_DATA/different_methods/105setup_neat.csv'
    df_neat_2 = helpers.create_dataframe(filepath_data_neat_2, filepath_setup_neat_2)
    # = ppo stuff ===========================================================================================

    # ============================================================================================

    # = neat ============================================================================================
    # filt, filter_conditions = helpers.get_random_filters_given_columns(df_neat)
    # print(helpers.benefits_from_diversity(df_neat, df_neat_2, 500))
    # =============================================================================================


    # = PPO ============================================================================================
    # filt, filter_conditions = helpers.get_random_filters_given_columns(df_rl_2)
    # # helpers.average_reward_given_filters(df_rl, filt)
    # custom_objects = {'lr_schedule': lambda _: None, 'clip_range': lambda _: None}
    #
    # model = PPO.load(agent_2_path, custom_objects=custom_objects)
    # done = False
    #
    # subdomain_analysis = helpers.average_difference_in_subdomain(df_rl, df_rl_2, 500)
    # print(subdomain_analysis)

    # difftype
    # print(helpers.benefits_from_diversity(df_rl_3, df_rl_4, 2000))
    # print(helpers.benefits_from_diversity(df_neat, df_neat_2, 2000))

    a = helpers.benefits_from_diversity(df_rl_3, df_neat, 2000)
    # print(a[2])
    b = helpers.benefits_from_diversity(df_rl_3, df_neat_2, 2000)
    c = helpers.benefits_from_diversity(df_rl_4, df_neat, 2000)
    d = helpers.benefits_from_diversity(df_rl_4, df_neat_2, 2000)

    print(f"The average is {np.mean([a[2],b[2],c[2],d[2]])} ({a[2]},{b[2]},{c[2]},{d[2]})")


    # Comp var (incompetent \n competent)
    # print(helpers.benefits_from_diversity(df_rl, df_rl_1, 500))
    # print(helpers.benefits_from_diversity(df_rl_3, df_rl_4, 500))
    # =============================================================================================
