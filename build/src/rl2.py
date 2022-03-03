import gym
import torch
from gym import spaces
# import numpy as np
from gym.spaces import Box, Discrete
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from data_handler import Collector

import game
import numpy as np
from game import *
import pygame
from helpers import *
from bodies import *
import stable_baselines3

import data_handler

"""
Add recognition to stable baselines api

And to sentdex tutorial
"""


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}




    def __init__(self):
        # self.runs_completed = -1
        super(CustomEnv, self).__init__()

        # The possible decisions the agent can make
        # planet x/y Momentum, planet x/y Pos

        self.action_space = spaces.Box(low=-1, high=1, shape=(12,), dtype=np.float32)
        # p1x, p1y, p2x, p2y, p3x, p3y p1xm, p1ym, p2xm, p2ym, p3xm, p3ym

        self.runs_completed = 0

        # self.collector = data_handler.Collector(f"{time.time().real}")
        self.collector = Collector(f"rl2")

        # The things that the model knows before input
        # For now,  star x/y pos, p1 x/y pos, p2 x/y pos, p3 x/y pos, p1m, p2m, p3m
        N_DISCRETE_ACTIONS = 3*data_handler.GLBVARS.n_stars + 5*data_handler.GLBVARS.n_planets + 2
        self.observation_space = spaces.Box(low=0, high=getWidth(), shape=(N_DISCRETE_ACTIONS,))



    def step(self, action):
        print("step called")
        # self.runs_completed += 1
        self.started = 0
        self.time_started = time.time().real
        # self.start_time = time.time().real
        self.runs_completed += 1
        pygame.init()
        while self.running:




            # set the age of each planet that is "active"
            for pnt in self.planets:
                if pnt.alive:
                    pnt.age = (current_time() - pnt.birthtime).__round__(2)

            # self.mx, self.my = pygame.mouse.get_pos()

            self.screen.blit(self.bg, (0, 0))

            text_box(f"Reinforcement Learning", 15, self.screen, -600 + (getWidth() / 2), -350 + (getHeight() / 2))
            text_box(f"Runs Completed: {self.runs_completed} ({data_handler.GLBVARS.n_envs})", 15, self.screen, -200 + (getWidth() / 2), -350 + (getHeight() / 2))
            text_box(f"CA: {self.cumulative_age.__round__(2)}", 15, self.screen, 500 + (getWidth() / 2), -350 + (getHeight() / 2))



            self.star.draw()
            self.CLICKED = False

            # handle star-planet crash
            for pnt in self.planets:
                if euclidian_distance(self.star, pnt) <= self.star.r * 1.2:
                    # cumulative_age += pnt.age
                    if np.abs(time.time().real - self.start_time) < 1.2:
                        self.reward -= 4
                        pnt.destroy(deathmsg="SHOT INTO DEATH")
                    else:
                        pnt.destroy(deathmsg="eaten by sun")


            # handle planet-planet crash
            for pnt1 in self.planets:
                for pnt2 in self.planets:
                    if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
                        n = np.random.randint(0, 2)
                        # PUNISH IF TOO SOON
                        if np.abs(time.time().real - self.start_time) < 1.2:
                            self.reward -= 4
                        if n == 1:
                            # cumulative_age += pnt.age
                            pnt1.destroy(deathmsg="multi-planet collision")
                        else:
                            # cumulative_age += pnt.age
                            pnt2.destroy(deathmsg="multi-planet collision")

            #########################
            #### CALCULATE FORCES ###
            #########################

            ################################################
            ## https://www.youtube.com/watch?v=OTJWGvibBfk #
            ## The previous tutorial taught me to add the  #
            ## fores to get a net fore. The exact .        #
            ## implementation is original                  #
            ################################################

            # net force calculator for bodies

            # motion step 1
            # set forces = 0 why?
            for body in (self.planets + self.stars):
                body.force = 0
                # setattr(body, "force", 0)

            # calculate gravity
            for body1 in (self.planets + self.stars):
                for body2 in (self.planets + self.stars):
                    # if body not in stars:
                    #     pass
                    if body1 != body2:
                        body1.force += law_of_gravitation(body2, body1)

            # move and draw planets
            for body in self.planets:
                if body.active:  # and body.mass != 0:
                    body.draw()
                    body.move()

            #setup actions of the agent
            if self.started == 0:

                self.position_scalar = 0.95

                self.planet1 = Planet(self.screen, self.position_scalar * np.abs(action[0]) * getWidth(), self.position_scalar * np.abs(action[1]) * getHeight(), 10)
                logging.info(f"P1POS:{self.position_scalar * np.abs(action[0]) * getWidth(), self.position_scalar * np.abs(action[1]) * getHeight()}")

                self.planet2 = Planet(self.screen, self.position_scalar * np.abs(action[2]) * getWidth(), self.position_scalar * np.abs(action[3]) * getHeight(), 10)
                logging.info(f"P2POS:{self.position_scalar * np.abs(action[2]) * getWidth(), self.position_scalar * np.abs(action[3]) * getHeight()}")

                self.planet3 = Planet(self.screen, self.position_scalar * np.abs(action[4]) * getWidth(), self.position_scalar * np.abs(action[5]) * getHeight(), 10)
                logging.info(f"P3POS:{self.position_scalar * np.abs(action[4]) * getWidth(), self.position_scalar * np.abs(action[5]) * getHeight()}")

                # self.momentum_scalar = 0.0001
                self.momentum_scalar = 0.00005
                self.planet1_momentum = np.array([action[6] * self.momentum_scalar, action[7] * self.momentum_scalar])
                logging.info(f"P1M:{action[6] * self.momentum_scalar, action[7] * self.momentum_scalar}")
                setattr(self.planet1, "momentum", self.planet1_momentum)

                self.planet2_momentum = np.array([action[8] * self.momentum_scalar, action[9] * self.momentum_scalar])
                logging.info(f"P2M:{action[8] * self.momentum_scalar, action[9] * self.momentum_scalar}")
                setattr(self.planet2, "momentum", self.planet2_momentum)

                self.planet3_momentum = np.array([action[10] * self.momentum_scalar, action[11] * self.momentum_scalar])
                logging.info(f"P3M:{action[10] * self.momentum_scalar, action[11] * self.momentum_scalar}")
                setattr(self.planet3, "momentum", self.planet3_momentum)

                # Using Tuples, but doesnt work...
                # self.planet1 = Planet(self.screen, action[1][0], action[2][0], 10)
                # self.planet2 = Planet(self.screen, action[1][1], action[2][1], 10)
                # self.planet3 = Planet(self.screen, action[1][2], action[2][2], 10)
                #
                # self.planet1_momentum = np.array(action[0][0], action[0][1])
                # self.planet2_momentum = np.array(action[0][2], action[0][3])
                # self.planet3_momentum = np.array(action[0][4], action[0][5])


                self.planets.append(self.planet1)
                self.planets.append(self.planet2)
                self.planets.append(self.planet3)

                self.planet1.active = True
                self.planet2.active = True
                self.planet3.active = True
                # pnt.active = True for pnt in self.planets

                self.start_time = current_time()
                self.planets_in_motion = True
                self.started += 1

            # Handle completing the game successfully.
            if not self.have_displayed_score and self.cumulative_age > 15:
                # cumulative_age = sum([pnt.age for pnt in planets])
                self.score = current_time() - self.start_time
                logging.info(f"{self.score}")
                self.have_displayed_score = True
                self.reward += 50 + (len([pnt for pnt in self.planets if pnt.alive == True]) * 50) + (50 / self.score + 1)
                self.running = False
                print(self.reward)
                self.collector.add_to_csv([self.runs_completed, self.cumulative_age])
                self.done = True

            # off screen
            for pnt in self.planets:
                if ((pnt.x <= pnt.r) or (pnt.x >= getWidth()) or (pnt.y <= pnt.r) or (
                        pnt.y >= getHeight())) and pnt.alive == True:
                    # cumulative_age += pnt.age
                    if np.abs(time.time().real - self.start_time) < 1.2:
                        self.reward -= 4
                        pnt.destroy(deathmsg="SHOT INTO DEATH")
                    else:
                        pnt.destroy(deathmsg="blasting off again...")

            # updating cml age
            self.cumulative_age = sum([pnt.age for pnt in self.planets])

            # Passive reward condition:
            # An increasing amount proportional to the length of time of the run.
            self.reward += (self.cumulative_age/10)

            # ending game (failure)
            if all_planets_destroyed(self.planets) and self.planets_in_motion and not self.have_displayed_score:
                logging.debug("FAILED")
                self.running = False
                # self.reward -= 150
                self.running = False
                print(self.reward)
                self.collector.add_to_csv([self.runs_completed, self.cumulative_age])
                self.done = True

            # update the bg
            pygame.display.update()

            # TODO remove all game.'s
            self.CLOCK.tick(self.FPS)


            #o = [pnt.y for pnt in self.planets]
        # TODO SETUP THE OBSERVATION
        # For now,  star x/y pos, window h/w
        # self.observation = np.array([self.star.x, self.star.y, getHeight(), getWidth()])
        self.observation = np.array([
            self.stars[0].x, self.stars[0].y, self.planet1.x, self.planet1.y,
            self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
            self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
            self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
            self.planet1.r,
            self.planet2.r,
            self.planet3.r,
            self.stars[0].mass,
            game.getWidth(), game.getHeight()
        ])
        # 3*stars + 5*planets + 2

        info = {}


        return self.observation, self.reward, self.done, info

    def reset(self):
        """
        This is where we get the observation
        So: star x/y pos, window h/w
        """
        print("reset called")
        self.done = False
        # pygame.init()
        # For us: just the observation_space
        self.planets_in_motion = False
        self.have_displayed_score = False
        self.start_time = time.time().real
        self.cumulative_age = 0
        self.score = 0
        self.screen = pygame.display.set_mode((getWidth(), getHeight()))
        self.running = True
        self.reward = 0
        self.reward_scalar = 1

        self.FPS = 144
        self.CLOCK = pygame.time.Clock()

        # setting up bg
        self.bg = pygame.image.load("../assets/gamebg1.png")
        pygame.display.set_icon(self.bg)

        # menu buttons
        self.star = Star(self.screen, getWidth() / 2, getHeight() / 2, 40)
        self.planets = []
        self.stars = [self.star]

        self.clicks = 0

        # new observation space
        self.planet1_momentum = np.array([0, 0])
        self.planet2_momentum = np.array([0, 0])
        self.planet3_momentum = np.array([0, 0])

        self.planet1 = Planet(r=10)
        self.planet2 = Planet(r=10)
        self.planet3 = Planet(r=10)

        self.planet1.x = 0
        self.planet1.y = 0
        self.planet2.x = 0
        self.planet2.y = 0
        self.planet3.x = 0
        self.planet3.y = 0

        self.observation = np.array([
            self.stars[0].x, self.stars[0].y, self.planet1.x, self.planet1.y,
            self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
            self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
            self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
            self.planet1.r,
            self.planet2.r,
            self.planet3.r,
            self.stars[0].mass,
            data_handler.GLBVARS.width, data_handler.GLBVARS.height
        ])

        return self.observation  # reward, done, info can't be included


fmt = '[%(levelname)s] %(asctime)s - %(message)s '
# l1 = logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)

# logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)
logging.basicConfig(level=logging.INFO, format=fmt)

#################
# TESTING START #
#################

# from stable_baselines3.common.env_checker import check_env
#
# env = CustomEnv()
# # It will check your custom environment and output additional warnings if needed
# check_env(env)


# env = CustomEnv()
# episodes = 50
#
# for episode in range(episodes):
# 	done = False
# 	obs = env.reset()
# 	while True:#not done:
# 		random_action = env.action_space.sample()
# 		print("action",random_action)
# 		obs, reward, done, info = env.step(random_action)
# 		print('reward',reward)

###############
# TESTING END #
###############



##################
# TRAINING START #
##################





import gym
import time
from tensorflow.keras.callbacks import ModelCheckpoint
# from stable_baselines3 import PPO, A2C, DQN, SAC
from stable_baselines3 import *
# from stable_baselines3.common.vec_env import VecEnv
# from stable_baselines3.common import vec_env
# from stable_baselines.ppo2 import PPO2

"""
Remember to reference Sentdex and documentation here (stable_baselines3, gym)
"""
if __name__ == '__main__':
    start_time = time.time().real

    # env = VecEnv("CustomEnv")
    # env = CustomEnv()
    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
    env = make_vec_env(CustomEnv, n_envs=data_handler.GLBVARS.n_envs, seed=2, vec_env_cls=SubprocVecEnv)
    filepath="models"
    cb = ModelCheckpoint(filepath, monitor='accuracy')

    #################
    # Train a model #
    #################

    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath, n_steps=128, n_epochs=4)#n_envs=2), n_epochs=2
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath, n_steps=128)

    # steps = 30_000
    steps = 1
    # training loop
    for i in range(1_000_000):
        print(f"training loop just looped. i={i}")

        # model.learn(total_timesteps=1, reset_num_timesteps=False, tb_log_name="PPO_POWER")
        # model.save(f"{filepath}/{time.strftime('%d%m')}/model")

        model.learn(total_timesteps=1, reset_num_timesteps=False, tb_log_name="PPO_POUR")
        model.save(f"{filepath}/{time.strftime('%d%m')}/model2")

    ###################################
    # load a previously trained model #
    ###################################

    # model = PPO.load(f"{filepath}/26022022/model-01:38:45-2.zip")
    # model = PPO.load(f"{filepath}/26022022/model-03:37:44-3.zip")

    #################################################
    # Use a model that has just been loaded/trained #
    #################################################

    print("step 2")

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




