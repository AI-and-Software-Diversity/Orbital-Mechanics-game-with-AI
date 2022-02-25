import gym
import p3 as p3
import started as started
from gym import spaces
# import numpy as np
from gym.spaces import Box, Discrete

import game
import numpy as np
from game import *
import pygame
from helpers import *
from bodies import *

class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    # font = pygame.font.Font('../assets/fonts/PressStart2P-vaV7.ttf', font)


    def __init__(self):
        super(CustomEnv, self).__init__()

        # The possible decisions the agent can make
        # planet x/y Momentum, planet x/y Pos
        N_PLANETS = 3 # N_PLANETS = len(game.planets)

        self.action_space = spaces.Box(low=-1, high=1, shape=(12,), dtype=np.float32)
        # p1x, p1y, p2x, p2y, p3x, p3y p1xm, p1ym, p2xm, p2ym, p3xm, p3ym




        # The things that the model knows before input
        # For now,  star x/y pos, window h/w
        N_DISCRETE_ACTIONS = 4
        self.observation_space = spaces.Box(low=0, high=getWidth(), shape=(N_DISCRETE_ACTIONS,), dtype=np.float32)

        # This may get very complicated in future

    def step(self, action):

        self.started = 0

        while self.running:

            # set the age of each planet that is "active"
            for pnt in self.planets:
                if pnt.alive:
                    pnt.age = (current_time() - pnt.birthtime).__round__(2)

            # self.mx, self.my = pygame.mouse.get_pos()

            self.screen.blit(self.bg, (0, 0))

            # text_box("human player", 15, self.screen, -50 + (getWidth() / 2), -350 + (getHeight() / 2))

            self.star.draw()
            self.CLICKED = False

            # sun eats planets
            for pnt in self.planets:
                if euclidian_distance(self.star, pnt) <= self.star.r * 1.2:
                    # cumulative_age += pnt.age
                    pnt.destroy(deathmsg="eaten by sun")
                    self.reward -= 10

            # planet clash
            for pnt1 in self.planets:
                for pnt2 in self.planets:
                    if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
                        n = np.random.randint(0, 2)
                        self.reward -= 10
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


            #setup actions...

            if self.started == 0:

                self.planet1 = Planet(self.screen, np.abs(action[0]) * getWidth(), np.abs(action[1]) * getHeight(), 10)
                self.planet2 = Planet(self.screen, np.abs(action[2]) * getWidth(), np.abs(action[3]) * getHeight(), 10)
                self.planet3 = Planet(self.screen, np.abs(action[4]) * getWidth(), np.abs(action[5]) * getHeight(), 10)

                self.planet1_momentum = np.array(action[6], action[7])
                self.planet2_momentum = np.array(action[8], action[9])
                self.planet3_momentum = np.array(action[10], action[11])

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
            # planet star collision
            # an event is some interaction with the engine. eg mouseclick
            # for event in pygame.event.get():
            #     # BUG: the window launches, and the event loop is entered after the first mousedown. Then
            #
            #     # quit logic
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            #
            #     # back to main menu
            #     if event.type == KEYDOWN and event.key == K_ESCAPE:
            #         self.running = False
            #
            #     # creating planets
            #
            #     if (event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP) and event.button == 1:
            #         self.CLICKED = True
            #
            #     ####################
            #     # PLACING PLANETS ##
            #     ####################
            #     # pygame.event.wait()
            #     # p1
            #     if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.clicks == 0:
            #         self.clicks += 1
            #         self.planet1 = Planet(self.screen, self.mx, self.my, 10)
            #         self.prev_x, self.prev_y = self.mx, self.my
            #
            #     elif event.type == MOUSEBUTTONUP and event.button == 1 and self.clicks == 1:
            #         self.clicks += 1
            #         self.planet1_momentum = np.array(action[0][1])
            #         setattr(self.planet1, "momentum", self.planet1_momentum)
            #
            #     # p2
            #     elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.clicks == 2:
            #         self.clicks += 1
            #         self.planet2 = Planet(self.screen, self.mx, self.my, 10)
            #         self.prev_x, self.prev_y = self.mx, self.my
            #
            #     elif event.type == MOUSEBUTTONUP and event.button == 1 and self.clicks == 3:
            #         self.clicks += 1
            #         self.planet2_momentum = action[1][1]
            #         setattr(self.planet2, "momentum", self.planet2_momentum)
            #
            #     # p3
            #     elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.clicks == 4:
            #         self.clicks += 1
            #         self.planet3 = Planet(self.screen, self.mx, self.my, 10)
            #         self.prev_x, self.prev_y = self.mx, self.my
            #         self.planets_in_motion = True
            #         self.start_time = current_time()
            #
            #         self.planets.append(self.planet1)
            #         self.planets.append(self.planet2)
            #         self.planets.append(self.planet3)
            #
            #
            #
            #     elif event.type == MOUSEBUTTONUP and event.button == 1 and self.clicks == 5:
            #         self.planet3_momentum = np.array(action[2][1])
            #         # self.planet3_momentum = scale_vectors((self.prev_x, self.prev_y), (self.mx, self.my), 0.2)
            #
            #         setattr(self.planet3, "momentum", self.planet3_momentum)
            #         for pnt in self.planets:
            #             pnt.active = True
            #         self.clicks += 1
            #
            #     ########################
            #     # PLACING PLANETS END ##
            #     ########################
            #
            #     # example click code
            #     # if llbutton.collidepoint(mx, my) and CLICKED:
            #     #     print("example")

            # calculate the score
            # if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score and cumulative_age > 200:
            #     # cumulative_age = sum([pnt.age for pnt in planets])
            #     have_displayed_score = True

            if not self.have_displayed_score and self.cumulative_age > 20:
                # cumulative_age = sum([pnt.age for pnt in planets])
                self.score = current_time() - self.start_time
                self.have_displayed_score = True
                self.reward += 100
                self.done = True
                self.running = False

            # off screen
            for pnt in self.planets:
                if ((pnt.x <= pnt.r) or (pnt.x >= getWidth()) or (pnt.y <= pnt.r) or (
                        pnt.y >= getHeight())) and pnt.alive == True:
                    # cumulative_age += pnt.age
                    self.reward -= 10
                    pnt.destroy(deathmsg="blasting off again...")

            # updating cml score
            self.cumulative_age = sum([pnt.age for pnt in self.planets])
            self.reward += self.cumulative_age / 10

            # ending game (failure)
            if all_planets_destroyed(self.planets) and self.planets_in_motion and not self.have_displayed_score:
                logging.debug("failure")
                self.running = False
                self.done = True
                self.running = False
                self.reward -= 100

            # update the bg
            pygame.display.update()

            # TODO remove all game.'s
            self.CLOCK.tick(self.FPS)



        # TODO SETUP THE OBSERVATION
        # For now,  star x/y pos, window h/w
        self.observation = np.array([self.star.x, self.star.y, getHeight(), getWidth()])

        info = {}


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
        self.reward = -100

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

        # self.observation = [self.stars[0].x, self.stars[0].y, getHeight(), getWidth()]
        self.observation = np.array([self.stars[0].x, self.stars[0].y, getHeight(), getWidth()])
        return self.observation  # reward, done, info can't be included

fmt = '[%(levelname)s] %(asctime)s - %(message)s '
# l1 = logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)

# logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)
logging.basicConfig(level=logging.DEBUG, format=fmt)

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

"""
Remember to reference Sentdex and documentation here (stable_baselines3, gym)
"""
start_time = time.time().real
env = CustomEnv()

filepath="TESTCALLBACK"
cb = ModelCheckpoint(filepath, monitor='accuracy')

#################
# Train a model #
#################
print("======")

# MlpPolicy, MultiInputPolicy

model = PPO("MlpPolicy", env, verbose=0)
# model = PPO("MultiInputPolicy", env, verbose=1)
steps = 10_000
print("======")
for i in range(3):
    model.learn(total_timesteps=steps)
    if i % 1 == 0:
        print(f"{steps*i} steps")
        # model.save(f"{filepath}/model{time.time().__round__(0)}")

###################################
# load a previously trained model #
###################################

# model = PPO.load(f"{filepath}/goodmodel")

#################################################
# Use a model that has just been loaded/trained #
#################################################

print("step 2")

obs = env.reset()
for i in range(1_000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
        print("CLOSING")


env.close()

print(f"that took {time.time().real - start_time} seconds, and we expected about >55 seconds")




