from gym import spaces
from data_handler import Collector
import logging
import gym
import pygame
import numpy as np
import data_handler
import helpers
import bodies
import time
import random

"""
The structure of the main OrbitEnv class comes from the stable_baselines3 api:
I learnt how to train my model with reinforcement learning using the stable_baselines3 api:
*LINK*

I learnt how to create my own gym custom environment following a tutorial series online by "Sentdex" on youtube
*LINK*

I got some help with vectorization for optimisation:
https://www.youtube.com/watch?v=nxWginnBklU
https://youtu.be/nxWginnBklU
https://youtu.be/EEUXKG97YRw
https://www.youtube.com/watch?v=HN5d490_KKk 
"""

class OrbitEnv(gym.Env):

    """Custom Environment that follows gym interface"""

    metadata = {'render.modes': ['human']}

    def __init__(self, mode=None):

        super(OrbitEnv, self).__init__()

        # The possible decisions the agent can make
        # planet x/y Momentum, planet x/y Pos

        N_DISCRETE_ACTIONS = 4 * data_handler.GLBVARS.n_planets
        self.action_space = spaces.Box(low=-1, high=1, shape=(N_DISCRETE_ACTIONS,), dtype=np.float32)
        # 4 * n_planets
        # planet_N_x_position, planet_N_y_position, planet_N_x_momentum, planet_N_y_momentum # possibly planet_N_mass

        self.runs_completed = 0

        if mode == "neat":
            self.collector = Collector(f"data_neat", "neat")

        # if mode == "rlearn":
        else:
            self.collector = Collector(f"data_rlearn", "rlearn")


        # The things that the model knows before input
        # For now,  star x/y pos, p1 x/y pos, p2 x/y pos, p3 x/y pos, p1m, p2m, p3m
        N_DISCRETE_OBSERVATIONS = 3 * data_handler.GLBVARS.n_stars + 1 * data_handler.GLBVARS.n_planets + 2
        self.observation_space = spaces.Box(low=0, high=data_handler.GLBVARS.width, shape=(N_DISCRETE_OBSERVATIONS,))

    def step(self, action):
        # print("step called")
        # self.runs_completed += 1
        self.started = 0
        self.time_started = time.time().real
        self.runs_completed += 1

        while self.running:

            # set the age of each planet that is "active"
            for pnt in self.planets:
                if pnt.alive:
                    pnt.age = (helpers.current_time() - pnt.birthtime).__round__(2)

            self.CLICKED = False

            # handle star-planet crash
            for star in self.stars:
                for pnt in self.planets:
                    if helpers.euclidian_distance(star, pnt) <= star.r * 1.2:
                        # cumulative_age += pnt.age
                        if self.cumulative_timesteps < 150:
                            self.reward -= 40
                            pnt.destroy(deathmsg="SHOT INTO DEATH")
                        else:
                            pnt.destroy(deathmsg="eaten by sun")

            # handle planet-planet crash
            for pnt1 in self.planets:
                for pnt2 in self.planets:
                    if helpers.euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:

                        n = np.random.randint(0, 2)

                        # PUNISH IF TOO SOON
                        if self.cumulative_timesteps < 150:
                            self.reward -= 60

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
                    body.move()

            # setup actions of the agent
            if self.started == 0:

                position_scalar = 0.95
                momentum_scalar = data_handler.GLBVARS.planet_mom_scaler
                width = data_handler.GLBVARS.width
                height = data_handler.GLBVARS.height

                # decide the position of of planet
                planet_num = 0
                for i in range(0, 4 * data_handler.GLBVARS.n_planets, 4):
                    self.planets.append(
                        bodies.Planet(
                            x=position_scalar * np.abs(action[i]) * width,
                            y=position_scalar * np.abs(action[i+1]) * height,
                            r=self.planet_masses[planet_num],
                            screen=None
                        )
                    )


                    # decide the momentum of the planet
                    momentum = np.array(
                        [action[i+2] * momentum_scalar,
                         action[i+3] * momentum_scalar]
                    )

                    setattr(self.planets[planet_num], "momentum", momentum)

                    planet_num += 1

                for pnt in self.planets:
                    pnt.active = True

                self.start_time = helpers.current_time()
                self.planets_in_motion = True
                # i += 4
                self.started += 1

            n_planets_alive = len([pnt for pnt in self.planets if pnt.alive == True])
            self.cumulative_steps += 1

            # ending game (success)
            if not self.have_displayed_score and self.cumulative_steps > data_handler.GLBVARS.total_steps:
                # self.score = helpers.current_time() - self.start_time
                self.have_displayed_score = True
                self.reward += 100 + (n_planets_alive * 50)
                # print(f"SUCCESS, REWARD: {self.reward}, CS: {self.cumulative_steps}")
                self.running = False
                self.collector.add_to_csv([1,
                                           self.reward,
                                           self.cumulative_steps,
                                           data_handler.GLBVARS.total_steps,
                                           self.runs_completed])
                self.done = True

            # PLANET GOES OFF SCREEN
            for pnt in self.planets:
                # u d l r
                if ((pnt.y < 0) or (pnt.y > data_handler.GLBVARS.height)
                    or (pnt.x < 0) or (pnt.x > data_handler.GLBVARS.width)) and pnt.alive == True:

                    # Big punishment if planets are killed too soon
                    if self.cumulative_timesteps < 150:
                        self.reward -= 200
                        pnt.destroy(deathmsg="SHOT INTO DEATH")
                    else:
                        pnt.destroy(deathmsg="blasting off again...")

            # updating cml age
            self.cumulative_age = sum([pnt.age for pnt in self.planets])


            # Passive reward condition:
            # An increasing amount proportional to the length of time of the run.
            # increase the reward every 5s

            interval = 40
            self.n_loops_passed += 1
            if self.n_loops_passed >= interval:
                self.n_loops_passed = 0
                self.reward += 4 * n_planets_alive

            # ending game (failure)
            if helpers.all_planets_destroyed(self.planets) and self.planets_in_motion and not self.have_displayed_score:
                # print(f"FAILURE, REWARD: {self.reward}, CS: {self.cumulative_steps}")
                self.running = False
                # test with off for story in disso
                self.reward -= 80
                self.running = False
                # print(f"FAILED, SCORE: {self.reward}")
                self.collector.add_to_csv([0,
                                           self.reward,
                                           self.cumulative_steps,
                                           data_handler.GLBVARS.total_steps,
                                           self.runs_completed])

                self.done = True

        star_info = [star.x for star in self.stars] + [star.y for star in self.stars] + [star.r for star in self.stars]
        planet_info = list(self.planet_masses)

        other_info = [data_handler.GLBVARS.width, data_handler.GLBVARS.height]
        observation_list = star_info + planet_info + other_info
        # print("------------step-----------")
        # print(star_info)
        # print(planet_info)
        # print(other_info)
        # print("------------step-----------")

        self.observation = np.array(observation_list)

        info = {}

        return self.observation, self.reward, self.done, info

    def reset(self):
        """
        This is where we get the observation
        So: star x/y pos, window h/w
        """
        # print("reset called")
        self.done = False
        self.n_loops_passed = 0
        self.cumulative_steps = 0
        # For us: just the observation_space
        self.planets_in_motion = False
        self.have_displayed_score = False
        self.start_time = time.time().real
        self.cumulative_age = 0
        self.score = 0
        self.running = True
        self.reward = 0
        self.reward_scalar = 1
        self.reward_tracker = 0


        self.FPS = 144
        self.CLOCK = pygame.time.Clock()

        # setting up bg
        self.stars = []

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # choosing the positions of all stars
        star_xs = []
        star_ys = []

        while True:
            starsWithValidPositions = 0
            star_xs.clear()
            star_ys.clear()
            for i in range(data_handler.GLBVARS.n_stars):
                # generate n points
                star_xs.append(random.randint(data_handler.GLBVARS.star_x_pos[0], data_handler.GLBVARS.star_x_pos[1]))
                star_ys.append(random.randint(data_handler.GLBVARS.star_y_pos[0], data_handler.GLBVARS.star_y_pos[1]))

            # checking if points are suitable.....

            # specify min/max distance
            mids = data_handler.GLBVARS.min_distance_stars
            mads = data_handler.GLBVARS.max_distance_stars

            # check suitability
            for i in range(len(star_xs)-1):
                for j in range(i+1, len(star_xs)):
                    distance = np.linalg.norm(np.array([star_xs[i], star_ys[i]]) - np.array([star_xs[j], star_ys[j]]) )
                    if distance > mids and distance < mads:
                        starsWithValidPositions += 1

            if starsWithValidPositions == data_handler.GLBVARS.n_stars:
                break

        # creating starts
        for i in range(data_handler.GLBVARS.n_stars):

            self.stars.append(
                bodies.Star(
                    self.screen,
                    star_xs[i],
                    star_ys[i],
                    np.random.randint(
                        data_handler.GLBVARS.star_rad[0],
                        data_handler.GLBVARS.star_rad[1]))
            )




        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        self.planet_masses = np.random.randint(data_handler.GLBVARS.planet_mass[0],
                                               data_handler.GLBVARS.planet_mass[1],
                                               size=(data_handler.GLBVARS.n_planets,))
        self.planets = []

        self.clicks = 0

        # new observation space
        star_info = [star.x for star in self.stars] + [star.y for star in self.stars] + [star.r for star in self.stars]
        planet_info = list(self.planet_masses)
        other_info = [data_handler.GLBVARS.width, data_handler.GLBVARS.height]

        observation_list = star_info + planet_info + other_info

        # print("------------reset-----------")
        # print(star_info)
        # print(planet_info)
        # print(other_info)
        # print("------------reset-----------")

        self.observation = np.array(observation_list)
        print("="*70)
        print(self.observation)
        print("="*70)

        return self.observation  # reward, done, info can't be included