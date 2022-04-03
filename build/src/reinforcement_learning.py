from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
import logging
import time
# from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import *
import data_handler
# import OrbitEnv
from OrbitEnv import OrbitEnv
from OrbitEnvNoGFX import OrbitEnv

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
    env = make_vec_env(OrbitEnv, n_envs=data_handler.GLBVARS.n_envs, seed=2, vec_env_cls=SubprocVecEnv)
    filepath = 'data/rlearn/models'
    # cb = ModelCheckpoint(filepath, monitor='accuracy')

    # decide what kind of model you want to preview
    # use_saved_model, train_new_model = True, False
    use_saved_model, train_new_model = False, True
    # see_sample_run = True
    see_sample_run = False

    #################
    # Train a model #
    #################
    if train_new_model:

        model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath, n_steps=4)

        # we only need one step to make the initial decisions (position and velocity of planets) so keep at 1
        steps = 1
        # training loop

        i = 1
        # i = -1

        while i > -1:

            model.learn(total_timesteps=1, reset_num_timesteps=False)
            model.save(f"{filepath}/model{i}")
            print(f"Jut saved model{i}")
            i += 1

    ###################################
    # load a previously trained model #
    ###################################

    if use_saved_model:
        model = PPO.load('data/rlearn/models/model714')

    #################################################
    # Use a model that has just been loaded/trained #
    #################################################

    env = OrbitEnv(mode="rlearn")
    # setattr(env.collector, "file_to_use", f"data_rlearn")
    # setattr(env.collector, "model_type", f"rlearn")
    obs = env.reset()

    if see_sample_run:
        # show 3 sample runs with the chosen model
        for i in range(100):

            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)

            if done:
                print(f"Done. reward: {reward}")
                obs = env.reset()

        env.close()


