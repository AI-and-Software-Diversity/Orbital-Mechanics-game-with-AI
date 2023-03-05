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

from OrbitEnvNoGFX import OrbitEnv
# from OrbitEnv import OrbitEnv

"""
I learnt how to implement this file mainly using Sentdex's youtube tutorial and the stable baselines 
documentation.


https://www.youtube.com/watch?v=XbWhJdQgi7E&list=PLQVvvaa0QuDf0O2DWwLZBfJeYY-JOeZB1&index=1
https://stable-baselines3.readthedocs.io/en/master/guide/examples.html


"""

if __name__ == '__main__':
    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    logging.basicConfig(level=logging.INFO, format=fmt)
    start_time = time.time().real
    print(f"{time.strftime('%d%m(%H:%M)')}")
    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
    env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, vec_env_cls=DummyVecEnv)
    filepath = 'data/rlearn/models'

    # What would you like to do?
    # use_saved_model, train_new_model = True, False
    use_saved_model, train_new_model = False, True

    # see_sample_run = True
    see_sample_run = False


    #################
    # Train a model #
    #################
    if train_new_model:

        # train a new model (PPO or A2C)
        # model = PPO("MlpPolicy", env, verbose=1, n_steps=784, learning_rate=3e-5)
        # model = A2C("MlpPolicy", env, verbose=1, n_steps=784)

        custom_objects = {'lr_schedule': lambda _: None, 'clip_range': lambda _: 0.2}

        # train a model from a checkpoint
        model = PPO.load(path='data/rlearn/models/model134-2802(18:39).zip',
                         env=OrbitEnv(mode="rlearn"),
                         custom_objects=custom_objects)

        # we only need one step to make the initial decisions (position and velocity of planets) so keep at 1
        steps = 1

        # training loop

        i = 1
        while i > -1:
            model.learn(total_timesteps=1, reset_num_timesteps=False)
            timestamp = time.strftime("%d%m(%H:%M)")

            if i % 2 == 0:
                # break
                model.save(
                    f"{filepath}/model{i}-{timestamp}"
                )
                print(f"Jut saved model{i}-{timestamp}")

            i += 1

    ###################################
    # load a previously trained model #
    ###################################

    if use_saved_model:

        # string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/RESEARCH_DATA/2S1P/rl_1/model10-0809(15:49)"
        string = "data/rlearn/models/model134-2802(18:39)"
        from stable_baselines3.common import base_class

        custom_objects = {'lr_schedule': lambda _: None, 'clip_range': lambda _: None}

        # string = "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/model62-2502(22:31)"
        model = PPO.load(path=string, custom_objects=custom_objects)
        # print("yelp")
        # model = PPO.load(path=string)
        # model = PPO.load(path='/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/PRESENTATION_DATA/different_methods/model35-2302(01:25)',
        #                  env=OrbitEnv(mode="rlearn"))

    #################################################
    # Use a model that has just been loaded/trained #
    #################################################

    env = OrbitEnv(mode="rlearn")
    obs = env.reset()

    if see_sample_run:
        start_time = helpers.current_time()

        # https: // stable - baselines3.readthedocs.io / en / master / guide / examples.html
        n_runs = 1000
        for i in range(n_runs):

            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)

            if done:
                print(f"{i} Done. reward: {reward}")
                obs = env.reset()

        env.close()
        print(np.mean(helpers.get_collumn_from_csv(
            "/home/javonne/Uni/Orbital-Mechanics-game-with-AI/build/data/rlearn/csvs/data_rlearn.csv", 1)))
        print(f"\n\nThat took {(helpers.current_time() - start_time)/60}m")

        print()