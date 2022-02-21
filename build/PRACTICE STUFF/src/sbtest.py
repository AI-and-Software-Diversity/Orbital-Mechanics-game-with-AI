import gym

from stable_baselines3 import PPO, A2C

env = gym.make("CartPole-v1")

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=60_000)

obs = env.reset()
for i in range(10_000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
        print("CLOSING")

env.close()