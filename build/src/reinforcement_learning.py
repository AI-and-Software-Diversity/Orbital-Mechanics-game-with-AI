import gym
from gym import spaces
# import numpy as np
import game
import numpy as np
from game import *
import pygame
from helpers import *
from bodies import *

class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}






    def __init__(self):
        super(CustomEnv, self).__init__()

        # The possible decisions the agent can make
        # x/y Momentum of each of the 3 planets
        N_PLANETS = 3 # N_PLANETS = len(game.planets)

        self.action_space = spaces.Box(low=-100, high=100, shape=(N_PLANETS, 2), dtype=np.float64)
        # var num_planets
        # The things that the model knows before input

        # For now,  star x/y pos, window h/w
        N_DISCRETE_ACTIONS = 4
        self.observation_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # This may get very complicated in future

    def step(self, action):

        info = {}
        self.observation, self.reward, self.done, info = None
        return self.observation, self.reward, self.done, info

    def reset(self):
        """
        This is where we get the observation
        So: star x/y pos, window h/w
        """

        # For us: just the observation_space
        self.planets_in_motion = False
        self.have_displayed_score = False
        self.start_time = 0
        self.cumulative_age = 0
        self.score = 0
        self.screen = pygame.display.set_mode((getWidth(), getHeight()))
        self.running = True

        # setting up bg
        self.bg = pygame.image.load("../assets/gamebg1.png")
        self.pygame.display.set_icon(self.bg)

        # menu buttons
        self.star = Star(self.screen, getWidth() / 2, getHeight() / 2, 40)
        self.planets = []
        self.stars = [self.star]
        self.clicks = 0

        self.observation = [self.stars[0].x, self.stars[0].y, getHeight(), getWidth()]
        return self.observation  # reward, done, info can't be included



















