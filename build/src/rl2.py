from gym import spaces
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from data_handler import Collector
import logging
import gym
import pygame
import numpy as np
import data_handler
import helpers
import bodies
import time
from tensorflow.keras.callbacks import ModelCheckpoint
from stable_baselines3 import *

"""
The training loop in this file in the main function was copied from the stable_baselines3 api:
*LINK*

The structure of the main CustomEnv class comes from the stable_baselines3 api:
I learnt how to train my model with reinforcement learning using the stable_baselines3 api:
*LINK*

I learnt how to create my own stable_baselines3 CustomEnv, and how to implement callbacks
following a tutorial series online by "Sentdex" on youtube
*LINK*

I got some help with vectorization for optimaisation:
https://www.youtube.com/watch?v=nxWginnBklU
https://youtu.be/nxWginnBklU
https://youtu.be/EEUXKG97YRw
https://www.youtube.com/watch?v=HN5d490_KKk 
"""


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    metadata = {'render.modes': ['human']}

    def __init__(self):
        print("instatiating--------------")
        # self.runs_completed = -1
        super(CustomEnv, self).__init__()

        # The possible decisions the agent can make
        # planet x/y Momentum, planet x/y Pos

        self.action_space = spaces.Box(low=-1, high=1, shape=(4*data_handler.GLBVARS.n_planets,), dtype=np.float32)
        # 4 * n_planets
        # planet_N_x_position, planet_N_y_position, planet_N_x_momentum, planet_N_y_momentum # possibly planet_N_mass

        self.runs_completed = 0

        # self.collector = data_handler.Collector(f"{time.time().real}")
        self.collector = Collector(f"rl2")

        # The things that the model knows before input
        # For now,  star x/y pos, p1 x/y pos, p2 x/y pos, p3 x/y pos, p1m, p2m, p3m
        N_DISCRETE_ACTIONS = 4 * data_handler.GLBVARS.n_stars + 5 * data_handler.GLBVARS.n_planets + 2
        N_DISCRETE_ACTIONS = 4 * data_handler.GLBVARS.n_stars + 2
        self.observation_space = spaces.Box(low=0, high=data_handler.GLBVARS.width, shape=(N_DISCRETE_ACTIONS,))

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
                    pnt.age = (helpers.current_time() - pnt.birthtime).__round__(2)

            # self.mx, self.my = pygame.mouse.get_pos()

            self.screen.blit(self.bg, (0, 0))

            helpers.text_box(f"Reinforcement Learning", 15, self.screen, -600 + (data_handler.GLBVARS.width / 2),
                             -350 + (data_handler.GLBVARS.height / 2))
            helpers.text_box(f"Runs Completed: {self.runs_completed} ({data_handler.GLBVARS.n_envs})", 15, self.screen,
                             -200 + (data_handler.GLBVARS.width / 2), -350 + (data_handler.GLBVARS.height / 2))
            helpers.text_box(f"CA: {self.cumulative_age.__round__(2)}/{data_handler.GLBVARS.target_game_time}", 15,
                             self.screen, 500 + (data_handler.GLBVARS.width / 2),
                             -350 + (data_handler.GLBVARS.height / 2))

            for star in self.stars:
                star.draw()

            self.CLICKED = False

            # handle star-planet crash
            for star in self.stars:
                for pnt in self.planets:
                    if helpers.euclidian_distance(star, pnt) <= star.r * 1.2:
                        # cumulative_age += pnt.age
                        if np.abs(time.time().real - self.start_time) < 1.2:
                            self.reward -= 4
                            pnt.destroy(deathmsg="SHOT INTO DEATH")
                        else:
                            pnt.destroy(deathmsg="eaten by sun")

            # handle planet-planet crash
            for pnt1 in self.planets:
                for pnt2 in self.planets:
                    if helpers.euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
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
                        body1.force += helpers.law_of_gravitation(body2, body1)

            # move and draw planets
            for body in self.planets:
                if body.active:  # and body.mass != 0:
                    body.draw()
                    body.move()

            # setup actions of the agent
            if self.started == 0:

                position_scalar = 0.95
                momentum_scalar = data_handler.GLBVARS.planet_mom_scaler
                width = data_handler.GLBVARS.width
                height = data_handler.GLBVARS.height

                # decide the position of of planet
                print(action)
                planet_num = 0
                for i in range(0, 4*data_handler.GLBVARS.n_planets,4):
                    self.planets.append(
                        bodies.Planet(
                            self.screen,
                            position_scalar * np.abs(action[i]) * width,
                            position_scalar * np.abs(action[i+1]) * height,
                            data_handler.GLBVARS.planet_mass[planet_num]
                        )
                    )

                    # decide the momentum of the planet
                    momentum = np.array(
                        [action[i+2] * momentum_scalar,
                         action[i+3] * momentum_scalar]
                    )

                    setattr(self.planets[planet_num], "momentum", momentum)
                    print(f"MOMENTUM={momentum}]")

                    planet_num += 1

                for pnt in self.planets:
                    pnt.active = True

                self.start_time = helpers.current_time()
                self.planets_in_motion = True
                # i += 4
                self.started += 1


            # setup actions of the agent
            # if self.started == 0:
            #
            #     self.position_scalar = 0.95
            #     width = data_handler.GLBVARS.width
            #     height = data_handler.GLBVARS.height
            #
            #     self.planet1 = bodies.Planet(self.screen,
            #                                  self.position_scalar * np.abs(action[0]) * width,
            #                                  self.position_scalar * np.abs(action[1]) * height,
            #                                  10)
            #     logging.info(
            #         f"P1POS:{self.position_scalar * np.abs(action[0]) * width, self.position_scalar * np.abs(action[1]) * height}")
            #
            #     self.planet2 = bodies.Planet(self.screen,
            #                                  self.position_scalar * np.abs(action[2]) * width,
            #                                  self.position_scalar * np.abs(action[3]) * height, 10)
            #     logging.info(
            #         f"P2POS:{self.position_scalar * np.abs(action[2]) * width, self.position_scalar * np.abs(action[3]) * height}")
            #
            #     self.planet3 = bodies.Planet(self.screen,
            #                                  self.position_scalar * np.abs(action[4]) * width,
            #                                  self.position_scalar * np.abs(action[5]) * height, 10)
            #     logging.info(
            #         f"P3POS:{self.position_scalar * np.abs(action[4]) * width, self.position_scalar * np.abs(action[5]) * height}")
            #
            #     # self.momentum_scalar = 0.0001
            #     self.momentum_scalar = 0.00005
            #
            #     self.planet1_momentum = np.array([action[6] * self.momentum_scalar, action[7] * self.momentum_scalar])
            #     logging.info(f"P1M:{action[6] * self.momentum_scalar, action[7] * self.momentum_scalar}")
            #     setattr(self.planet1, "momentum", self.planet1_momentum)
            #
            #     self.planet2_momentum = np.array([action[8] * self.momentum_scalar, action[9] * self.momentum_scalar])
            #     logging.info(f"P2M:{action[8] * self.momentum_scalar, action[9] * self.momentum_scalar}")
            #     setattr(self.planet2, "momentum", self.planet2_momentum)
            #
            #     self.planet3_momentum = np.array([action[10] * self.momentum_scalar, action[11] * self.momentum_scalar])
            #     logging.info(f"P3M:{action[10] * self.momentum_scalar, action[11] * self.momentum_scalar}")
            #     setattr(self.planet3, "momentum", self.planet3_momentum)
            #
            #     # Using Tuples, but doesnt work...
            #     # self.planet1 = Planet(self.screen, action[1][0], action[2][0], 10)
            #     # self.planet2 = Planet(self.screen, action[1][1], action[2][1], 10)
            #     # self.planet3 = Planet(self.screen, action[1][2], action[2][2], 10)
            #
            #     # self.planet1_momentum = np.array(action[0][0], action[0][1])
            #     # self.planet2_momentum = np.array(action[0][2], action[0][3])
            #     # self.planet3_momentum = np.array(action[0][4], action[0][5])
            #
            #     self.planets.append(self.planet1)
            #     self.planets.append(self.planet2)
            #     self.planets.append(self.planet3)
            #
            #     self.planet1.active = True
            #     self.planet2.active = True
            #     self.planet3.active = True
            #     # pnt.active = True for pnt in self.planets
            #
            #     self.start_time = helpers.current_time()
            #     self.planets_in_motion = True
            #     self.started += 1

                #    Handle completing the game successfully.
            if not self.have_displayed_score and self.cumulative_age > data_handler.GLBVARS.target_game_time:
                # cumulative_age = sum([pnt.age for pnt in planets])
                self.score = helpers.current_time() - self.start_time
                logging.info(f"SCORE :::   {self.score}")
                self.have_displayed_score = True
                self.reward += 50 + (len([pnt for pnt in self.planets if pnt.alive == True]) * 50) + (
                            50 / self.score + 1)
                self.running = False
                print(f"SUCCESS, SCORE: {self.reward}")
                self.collector.add_to_csv([self.runs_completed, self.cumulative_age])
                self.done = True

            # PLANET GOES OFF SCREEN
            for pnt in self.planets:
                # u d l r
                if ((pnt.y < 0) or (pnt.y > data_handler.GLBVARS.height)
                    or (pnt.x < 0) or (pnt.x > data_handler.GLBVARS.width)) and pnt.alive == True:

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
            self.reward += (self.cumulative_age / 10)

            # ending game (failure)
            if helpers.all_planets_destroyed(self.planets) and self.planets_in_motion and not self.have_displayed_score:
                logging.debug("FAILED")
                self.running = False
                # self.reward -= 150
                self.running = False
                print(f"FAILED, SCORE: {self.reward}")
                self.collector.add_to_csv([self.runs_completed, self.cumulative_age])
                self.done = True

            # update the bg
            pygame.display.update()

            # TODO remove all game.'s
            self.CLOCK.tick(self.FPS)

        # TODO SETUP THE OBSERVATION
        star_info = data_handler.GLBVARS.star_x_pos + data_handler.GLBVARS.star_y_pos \
                    + data_handler.GLBVARS.star_mass + data_handler.GLBVARS.star_rad

        # planet_info = [data_handler.GLBVARS. + data_handler.GLBVARS. + data_handler.GLBVARS.]
        planet_info = [self.planet1.x, self.planet1.y,
                       self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
                       self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
                       self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
                       self.planet1.r,
                       self.planet2.r,
                       self.planet3.r]

        other_info = [data_handler.GLBVARS.width, data_handler.GLBVARS.height]
        # observation_list = star_info + planet_info + other_info
        observation_list = star_info + other_info

        self.observation = np.array(observation_list)
        # 4*stars + 5*planets + 2

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
        self.screen = pygame.display.set_mode((data_handler.GLBVARS.width, data_handler.GLBVARS.height))
        self.running = True
        self.reward = 0
        self.reward_scalar = 1

        self.FPS = 144
        self.CLOCK = pygame.time.Clock()

        # setting up bg
        self.bg = pygame.image.load("../assets/gamebg1.png")
        pygame.display.set_icon(self.bg)
        self.stars = []
        # menu buttons
        for i in range(data_handler.GLBVARS.n_stars):
            self.stars.append(bodies.Star(self.screen,
                                          data_handler.GLBVARS.star_x_pos[i],
                                          data_handler.GLBVARS.star_y_pos[i],
                                          40))
        # self.star =

        self.planets = []


        self.clicks = 0

        # new observation space
        self.planet1_momentum = np.array([0, 0])
        self.planet2_momentum = np.array([0, 0])
        self.planet3_momentum = np.array([0, 0])

        self.planet1 = bodies.Planet(r=10)
        self.planet2 = bodies.Planet(r=10)
        self.planet3 = bodies.Planet(r=10)

        self.planet1.x = 0
        self.planet1.y = 0
        self.planet2.x = 0
        self.planet2.y = 0
        self.planet3.x = 0
        self.planet3.y = 0


        star_info = data_handler.GLBVARS.star_x_pos + data_handler.GLBVARS.star_y_pos \
                    + data_handler.GLBVARS.star_mass + data_handler.GLBVARS.star_rad

        # planet_info = [data_handler.GLBVARS. + data_handler.GLBVARS. + data_handler.GLBVARS.]
        # planet_info = [pnt.x and pnt.y for pnt in self.planets] + []
        # print("========================================")
        # print([pnt.x and pnt.y for pnt in self.planets])
        # print([pnt.x for pnt in self.planets])
        # print("========================================")
        planet_info = [self.planet1.x, self.planet1.y,
            self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
            self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
            self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
            self.planet1.r,
            self.planet2.r,
            self.planet3.r]

        other_info = [data_handler.GLBVARS.width, data_handler.GLBVARS.height]
        # observation_list = star_info + planet_info + other_info
        observation_list = star_info + other_info

        self.observation = np.array(observation_list)

        # self.observation = np.array([
        #     self.stars[0].x, self.stars[0].y,
        #     self.planet1.x, self.planet1.y,
        #     self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
        #     self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
        #     self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
        #     self.planet1.r,
        #     self.planet2.r,
        #     self.planet3.r,
        #     self.stars[0].mass,
        #     self.stars[0].r,
        #     data_handler.GLBVARS.width, data_handler.GLBVARS.height
        # ])

        return self.observation  # reward, done, info can't be included


"""
Remember to reference Sentdex and documentation here (stable_baselines3, gym)
"""
if __name__ == '__main__':

    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    logging.basicConfig(level=logging.INFO, format=fmt)
    # logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)

    start_time = time.time().real

    # env = VecEnv("CustomEnv")
    # env = CustomEnv()
    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
    env = make_vec_env(CustomEnv, n_envs=data_handler.GLBVARS.n_envs, seed=2, vec_env_cls=SubprocVecEnv)
    filepath = "models"
    cb = ModelCheckpoint(filepath, monitor='accuracy')

    #################
    # Train a model #
    #################

    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath, n_steps=128, n_epochs=4)#n_envs=2), n_epochs=2
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=filepath, n_steps=128)

    # we only need one step to make the initial decisions (position and velocity of planets) so keep at 1
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
