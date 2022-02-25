import gym
from gym.spaces import Box, Tuple, Discrete
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy

actions_space = Tuple((
    # planet x/y Momentum
    Box(low=-1, high=1, shape=(6,)),
    # planet x Pos
    Box(low=0, high=700, shape=(3,)),
    # planet y Pos
    Box(low=0, high=700, shape=(3,))
    )).sample()

print(actions_space)
print("")
print(actions_space[0])
print(actions_space[1])
print(actions_space[2])