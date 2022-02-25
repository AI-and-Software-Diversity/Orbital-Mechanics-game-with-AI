import gym
import time
from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import PPO, A2C

"""
Remember to reference Sentdex and documentation here (stable_baselines3, gym)
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
for i in range(3):
    model.learn(total_timesteps=steps)
    if i % 1 == 0:
        print("check")
        model.save(f"{filepath}/{time.strftime('%d%m%Y')}/model-{time.strftime('%X')}-{(1+i)*steps}")

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