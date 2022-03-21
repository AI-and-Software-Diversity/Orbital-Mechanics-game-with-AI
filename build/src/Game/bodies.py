import numpy as np
import pygame
import logging
import build.src.Game.helpers as helpers

class Star:
    """
    https://www.youtube.com/watch?v=G8MYGDf_9ho
    https://www.pygame.org/docs/ref/draw.html?highlight=circl#pygame.draw.circle

    used to create circles with hitboxes
    """
    def __init__(self, screen, x, y, r):

        self.x = x
        self.y = y
        self.r = r
        # self.mass = 1e+21 * r
        self.mass = r
        self.screen = screen
        # surface, color, center, radius
        self.rd, self.gn, self.bu = np.random.randint(0, 254), np.random.randint(0, 254), np.random.randint(0, 254)

    def draw(self):
        pygame.draw.circle(self.screen, (39, 176, 144), (self.x, self.y), self.r)
        # screen.blit(pygame.image.load("../assets/s10.png"), (self.x, self.y))
        # pygame.image.load("../assets/sun1.png")
        # screen.blit(screen, (self.x,self.y))

class Planet:

    def __init__(self, screen=None, x=None, y=None, r=None, velocity=[0, 0], force=[0, 0], age=0):

        logging.debug(f"initialising a planet")
        self.active = False
        self.alive = True
        self.dt = 0.000001 # step size = 0.000001
        self.x = x
        self.y = y
        self.r = r
        self.mass = r
        self.velocity = velocity
        self.acceleration = force
        self.screen = screen
        self.force = force
        # self.momentum = [0.0001, 0]
        self.momentum = [0, 0]
        self.birthtime = helpers.current_time().__round__(2)
        self.age = (helpers.current_time() - self.birthtime).__round__(2)
        # surface, color, center, radius
        self.rd, self.gn, self.bu = np.random.randint(0, 254), np.random.randint(0, 254), np.random.randint(0, 254)

    def draw(self):
        """
        draw a planet
        """
        # print("drawing a planet")
        # text_box(f"{self.age}", 10, self.screen, self.x+10, self.y+10)
        # text_box(f"{self.age}", 10, self.screen, self.x+10, self.y+10)

        pygame.draw.circle(self.screen, (self.rd, self.gn, self.bu), (self.x, self.y), self.r)

    def move(self):
        """
        move a planet
        """

        # Euler-Cromer method to new position:

        # First calculate the force on the body using the newtonian ...
        # done already in game loop

        # Then update momentum using the force*stepsize
        if self.mass != 0:
            self.momentum[0] = self.momentum[0] + self.force[0] * self.dt
            self.momentum[1] = self.momentum[1] + self.force[1] * self.dt

            # Finally, update the position using the momentum
            self.x = self.x + self.momentum[0] / (self.mass * self.dt)
            self.y = self.y + self.momentum[1] / (self.mass * self.dt)


        # print("Pos:  {},{}".format(self.x, self.y))
        # print("Accl:  {},{}".format(self.acceleration[0], self.acceleration[1]))
        # print("V:  {},{}".format(self.velocity[0], self.velocity[1]))

    def destroy(self, deathmsg="PLACEHOLDEERDEATHMESSAGE"):
        """
        destroy any planet that goes offscreen
        """
        # logging.info(deathmsg)

        x, y = np.random.randint(200, 300), np.random.randint(200, 300)
        self.r, self.x, self.y, self.velocity, self.momentum, self.alive, self.mass = 0, -x, -y, [0, 0], [0, 0], False, 0

        # if np.linalg.norm(self.velocity) > 0:
