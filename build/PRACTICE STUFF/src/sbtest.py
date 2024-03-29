import gym
import time
from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import PPO, A2C

"""
This code comes from this sentdex tutorial: 
https://www.youtube.com/watch?v=uKnjGn8fF70&list=PLQVvvaa0QuDf0O2DWwLZBfJeYY-JOeZB1&index=3
"""

start_time = time.time().real
env = gym.make("CartPole-v1")
filepath="trained_models"
cb = ModelCheckpoint(filepath, monitor='accuracy')

#################
# Train a model #
#################
time.strftime("%d/%m/%Y")
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath)
steps = 10_000
for i in range(10):
    model.learn(total_timesteps=20, reset_num_timesteps=False, tb_log_name="P0p")
    model.save(f"{filepath}/model")

# (venv) (base) javonne@javonne-desktop:~/Uni/Orbital-Mechanics-game-with-AI/build/PRACTICE STUFF/src$ tensorboard --logdir=trained_models
# TensorBoard 1.15.0 at http://javonne-desktop:6006/ (Press CTRL+C to quit)


###################################
# load a previously trained model #
###################################

# model = PPO.load(f"{filepath}/goodmodel")

#################################################
# Use a model that has just been loaded/trained #
#################################################

# print("step 2")

# obs = env.reset()
# for i in range(1_000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#         obs = env.reset()
#         print("CLOSING")
#
#
# env.close()

print(f"that took {time.time().real - start_time} seconds, and we expected about >55 seconds")