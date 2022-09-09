import stable_baselines3
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.logger import configure
import logging
import time
# from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import *
import data_handler
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
    # env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, vec_env_cls=DummyVecEnv)

    # neat 1
    path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/rl_1"
    agent_1_path = f"{path}/model10-0809(15:49)"
    filepath_data = f"{path}/data_rlearn.csv"
    filepath_setup = f"{path}/setup_rlearn.csv"
    df_rl = helpers.create_dataframe(filepath_data, filepath_setup)

    filt, filter_conditions = helpers.get_random_filters_given_columns(df_rl)
    helpers.average_reward_given_filters(df_rl, filt)

    # neat2
    path_2 = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/rl_2"
    agent_2_path = f"{path_2}/model15-0809(15:51).zip"
    filepath_data_2 = f"{path_2}/data_rlearn.csv"
    filepath_setup_2 = f"{path_2}/setup_rlearn.csv"
    df_rl_2 = helpers.create_dataframe(filepath_data_2, filepath_setup_2)

    model = PPO.load(agent_1_path)

    env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, vec_env_cls=DummyVecEnv)
    obs = env.reset()

    n_runs = 100
    for i in range(n_runs):

        while not done:
            action, _states = model.predict(obs, deterministic=False)
            obs, reward, done, info = env.step(action)

        done = False

        print(f"{i} Done. reward: {reward}")
        obs = env.reset()
        print(obs)

        # ============================================================================

        subdomain_analysis = helpers.superior_agent_in_subdomain(df_rl, df_rl_2, 100)
        best_agent_path = helpers.agent_selection_component(subdomain_analysis, obs, agent_1_path, agent_2_path)
        print(f"This run uses the agent location at: \n{best_agent_path}\n")

        # best_agent_path = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/data/rlearn/models/model24-1105(11:40).zip"
        model = PPO.load(best_agent_path)

        # ============================================================================

    env.close()
    print(f"\n\nThat took {round((helpers.current_time() - start_time) / 60, 2)}m")
