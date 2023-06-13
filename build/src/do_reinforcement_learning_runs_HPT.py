import optuna
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
import numpy as np
from stable_baselines3.common.evaluation import evaluate_policy
from OrbitEnvNoGFX import OrbitEnv
# from OrbitEnv import OrbitEnv
from _collections_abc import Mapping
"""
I learnt how to implement this file mainly using Sentdex's youtube tutorial and the stable baselines 
documentation.


https://www.youtube.com/watch?v=XbWhJdQgi7E&list=PLQVvvaa0QuDf0O2DWwLZBfJeYY-JOeZB1&index=1
https://stable-baselines3.readthedocs.io/en/master/guide/examples.html


"""

if __name__ == '__main__':


    """https://github.com/nicknochnack/StreetFighterRL/blob/41c4d1d38f1913c073b2b2be19b383a4a1795a79/StreetFighter-Tutorial.ipynb"""


    LOG_DIR = './logs/'
    OPT_DIR = './opt/'
    filepath = 'data/rlearn/models'

    SAVE_PATH = os.path.join(OPT_DIR, 'trial_{}_best_model'.format(1))

    # Run a training loop and return mean reward
    def optimize_agent(trial):
        try:
            model_params = optimize_ppo(trial)

            # Create environment
            env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, vec_env_cls=DummyVecEnv)

            # Create algo
            model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=LOG_DIR, **model_params)
            model.learn(total_timesteps=1, reset_num_timesteps=False)

            # i = 1
            # while i > -1:
            #     model.learn(total_timesteps=1, reset_num_timesteps=False)
            #     timestamp = time.strftime("%d%m(%H:%M)")
            #
            #     if i % 2 == 0:
            #         # break
            #         model.save(
            #             f"{filepath}/model{i}-{timestamp}"
            #         )
            #         print(f"Jut saved model{i}-{timestamp}")
            #     i += 1

            # Evaluate model
            mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=1)
            env.close()

            SAVE_PATH = os.path.join(OPT_DIR, 'trial_{}_best_model'.format(trial.number))
            model.save(SAVE_PATH)

            return mean_reward

        except Exception as e:
            # print(e)
            return -1000

    def optimize_ppo(trial):
        return {
            'n_steps':data_handler.GLBVARS.total_steps,
            # 'n_steps':2,
            'gamma':trial.suggest_float('gamma', 0.7, 0.9999),
            'learning_rate':trial.suggest_float('learning_rate', 1e-8, 1e-4),
            'clip_range':trial.suggest_float('clip_range', 0.1, 0.4),
            'ent_coef': trial.suggest_float('ent_coef', 1e-2, 3e-1),
            'gae_lambda':trial.suggest_float('gae_lambda', 0.85, 0.99)

        }

    # Creating the experiment
    study = optuna.create_study(direction='maximize')
    study.optimize(optimize_agent, n_trials=20, n_jobs=1)

    print(f"Best params:\n{study.best_params}\n\n\n Best trial:\n{study.best_trial}\n\n\nBest value: {study.best_value}")
