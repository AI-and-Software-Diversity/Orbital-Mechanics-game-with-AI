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
    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    logging.basicConfig(level=logging.INFO, format=fmt)
    start_time = time.time().real
    print(f"{time.strftime('%d%m(%H:%M)')}")
    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
    env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, vec_env_cls=DummyVecEnv)
    obs = env.reset()
    filepath = 'data/rlearn/models'

    # neat1
    path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/neat_1"
    agent_1_path = f"{path}/winner08281650"
    filepath_data = f"{path}/data_neat.csv"
    filepath_setup = f"{path}/setup_neat.csv"
    df_neat = helpers.create_dataframe(filepath_data, filepath_setup)

    path_2 = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/rl_2"
    agent_2_path = f"{path_2}/model15-0809(15:51).zip"
    filepath_data_2 = f"{path}/data_rl.csv"
    filepath_setup_2 = f"{path}/setup_rl.csv"
    df_rl = helpers.create_dataframe(filepath_data, filepath_setup)

    filt, filter_conditions = helpers.get_random_filters_given_columns(df_neat)
    helpers.average_reward_given_filters(df_neat, filt)

    model = PPO.load(agent_2_path)

    n_runs = 10
    for i in range(n_runs):

        while not done:
            action, _states = model.predict(obs, deterministic=False)
            obs, reward, done, info = env.step(action)

        done = False

        print(f"{i} Done. reward: {reward}")
        obs = env.reset()
        print(obs)

        # ============================================================================
        subdomain_analysis = helpers.superior_agent_in_subdomain(df_neat, df_rl, 100)
        best_agent_path, agent_type = helpers.ASC_neat_rl(subdomain_analysis, obs, agent_1_path, agent_2_path)
        print(f"This run uses the agent location at: \n{best_agent_path}\n")

        if agent_type == "neat":
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

        elif agent_type == "rl":
            model = PPO.load(best_agent_path)
            # model = PPO.load(agent_2_path, env=OrbitEnv(mode="rlearn"))
        # ============================================================================

    env.close()
    print(f"\n\nThat took {round((helpers.current_time() - start_time) / 60, 2)}m")
