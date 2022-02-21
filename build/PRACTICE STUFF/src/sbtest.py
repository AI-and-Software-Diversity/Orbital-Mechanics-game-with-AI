import gym
import time
import tensorflow as tf
from stable_baselines3 import PPO, A2C

env = gym.make("CartPole-v1")
filepath="TESTCALLBACK"
cb = tf.keras.callbacks.ModelCheckpoint(
    filepath, monitor='accuracy'
)

model = PPO("MlpPolicy", env, verbose=1)
steps = 70_000
for i in range(steps):
    model.learn(total_timesteps=steps)
    if steps % 5000 == 0:
        print("check")
        model.save(f"{filepath}/model{time.time().__round__(0)}")

obs = env.reset()
# for i in range(10_000):
for i in range(10):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
        print("CLOSING")


env.close()