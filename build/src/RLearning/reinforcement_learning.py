from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
import logging
from build.src.Game import data_handler
import time
from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import *
from build.src.Envs.OrbitEnv import OrbitEnv
"""
The training loop in this file in the main function was copied from the stable_baselines3 api:
*LINK*

I learnt how to implement callbacks following a tutorial series online by "Sentdex" on youtube
*LINK*

Remember to reference Sentdex and documentation here (stable_baselines3, gym)
"""

if __name__ == '__main__':

    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    logging.basicConfig(level=logging.INFO, format=fmt)
    start_time = time.time().real

    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
    env = make_vec_env(OrbitEnv, n_envs=data_handler.VARS.n_envs, seed=2, vec_env_cls=SubprocVecEnv)
    filepath = '../../data/rlearn/models'
    cb = ModelCheckpoint(filepath, monitor='accuracy')

    #################
    # Train a model #
    #################

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath, n_steps=256)

    # we only need one step to make the initial decisions (position and velocity of planets) so keep at 1
    steps = 1
    # training loop
    i = 1
    # comment to train
    # i = -1
    while i > -1:

        model.learn(total_timesteps=1, reset_num_timesteps=False, tb_log_name="PPO_POWER")
        model.save(f"{filepath}/model{i}")
        print(f"Jut saved model{i}")
        i += 1

    ###################################
    # load a previously trained model #
    ###################################

    # model = PPO.load(f"{filepath}/26022022/model-01:38:45-2.zip")
    model = PPO.load('../../data/rlearn/models/model.zip')


    #################################################
    # Use a model that has just been loaded/trained #
    #################################################

    env = OrbitEnv()
    obs = env.reset()
    for i in range(20):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        # env.render()
        if done:
            obs = env.reset()
            print("CLOSING")

    env.close()

    print(f"that took {time.time().real - start_time} seconds, and we expected about >55 seconds")
