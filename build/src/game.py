import pygame
from pygame.locals import *
import sys
import numpy as np
import math
import logging
from datetime import datetime

def euclidian_distance(body1, body2):


    distance = np.abs(np.linalg.norm(
        np.array([body1.x, body1.y]) - np.array([body2.x, body2.y])
    ))
    return distance


def text_box(str, font, screen, x, y):
    """
    https://www.fontspace.com/press-start-2p-font-f11591

    :param str:
    :param font:
    :param screen:
    :param x:
    :param y:
    :return:
    """

    font = pygame.font.Font('../data/fonts/PressStart2P-vaV7.ttf', font)
    text = font.render(str, True, (255,255,255))
    screen.blit(text, (x, y))


def get_force_vector_from_gravity(body1, body2):
    """
    We calculate the force of body 1 applies on body 2 on each body newtonian mechanics
    F_12 = G(m_1 * m_2/r^2)
    https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

    """
    # 1 calculate the force between the bodies
    F = (100 * body1.mass * body2.mass) / np.linalg.norm((np.array([body1.x, body1.y])-np.array([body2.x, body2.y]))) ** 2
    # print(F)

    # 2 calculate the angle of the force
    # reversed
    # direction_vector = np.array([body1.x, body1.y]) - np.array([body2.x, body2.y])

    direction_vector = np.array([-body2.x, body2.y]) - np.array([-body1.x, body1.y])
    # print(direction_vector)

    # convert the force to a vector
    # tangent = math.tan(direction_vector[0]
    #                    /direction_vector[1])

    if direction_vector[1] == 0:
        tangent = 0
    else:
        tangent = math.tan(direction_vector[0]/direction_vector[1])


    if tangent == 0:
        angle = 0
    else:
        angle = math.atan(tangent)

    F_vector = F*math.sin(angle), F*math.cos(angle)
    # print(F_vector)

    print("===========================")
    print(F_vector)
    print("===========================")
    return F_vector


def law_of_gravitation(body1, body2):

    """
    We calculate the force of body 1 applies on body 2 on each body newtonian mechanics
    The pull body1 applies to body2
    F_12 = G(m_1 * m_2/r^2)
    https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

    The specific method used was the Euler-Cromer method
    https://www.youtube.com/watch?v=rPkJtpVJwSw&list=PLdCdV2GBGyXOOutOEKggaZo1rCHtUYh-A

    Which followed this tutorial
    https://www.youtube.com/watch?v=4ycpvtIio-o&list=PLdCdV2GBGyXOExPW4u8H88S5mwrx_8vWK&index=2
    """

    if body1 == body2:
        raise Exception("The bodies can not be the same")

    G = 400
    r_vec = np.array([body1.x, body1.y])-np.array([body2.x, body2.y])
    r_mag = np.linalg.norm((np.array([body1.x, body1.y])-np.array([body2.x, body2.y])))
    r_hat = r_vec/r_mag

    try:
        F_mag = G * body1.mass * body2.mass / r_mag**2
    except ZeroDivisionError as err:
        logging.error(err)

    F_vector = F_mag * r_hat

    return F_vector


def main_menu():

    """
    https://www.youtube.com/watch?v=1_H7InPMjaY
    https://www.youtube.com/watch?v=a5JWrd7Y_14&t=936s
    Used to create basic game window

    https://www.youtube.com/watch?v=0RryiSjpJn0
    used to help implement main menus
    """

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # running = True

    # window title
    pygame.display.set_caption("spooky outer space")

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)

    llbutton = pygame.Rect((WIDTH/5, HEIGHT / 2), (30, 10))
    lbutton = pygame.Rect((2*WIDTH/5, HEIGHT / 2), (30, 10))
    mbutton = pygame.Rect((3*WIDTH/5, HEIGHT / 2), (30, 10))
    rbutton = pygame.Rect((4*WIDTH/5, HEIGHT / 2), (30, 10))

    while True:

        mx, my = pygame.mouse.get_pos()

        # setting up backup background as well as image bg
        screen.blit(bg, (0, 0))

        text_box("main menu", 50, screen, -200 + (WIDTH/2), -200+(HEIGHT/2))

        text_box("play (human)", 10, screen, WIDTH/5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), llbutton)

        if llbutton.collidepoint(mx, my) and clicked:
            pygame.event.wait()
            play_human()
            print("ll button")

        text_box("play (NEAT AI)", 10, screen, 2*WIDTH/5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), lbutton)
        if lbutton.collidepoint(mx, my) and clicked:
            play_NEAT()
            print("l button")

        text_box("play (RLearn AI)", 10, screen, 3*WIDTH/5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), mbutton)
        # print("playin")
        if mbutton.collidepoint(mx, my) and clicked:
            print("m button")
            play_r_learning()

        text_box("highscores", 10, screen, 4*WIDTH/5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), rbutton)

        clicked = False
        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():
            # print("test")
            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # mouseclick logic + menu traversal

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                logging.info("*click*")
                clicked = True



            # update the bg
            pygame.display.update()

        CLOCK.tick(FPS)


class Planet:

    def __init__(self, screen, x, y, r, velocity, force):

        logging.info("initialising a planet")
        self.active = False
        self.alive = True
        self.dt = 0.000001 # step size
        self.x = x # xPos
        self.y = y # yPos
        self.r = r # Radius
        self. mass = r
        self.velocity = velocity
        self.acceleration = force
        self.screen = screen
        self.force = force
        self.momentum = [0.0001, 0]
        self.age = 0 # how long a planet lasts for before being destroyed, initially 0
        # surface, color, center, radius
        self.rd, self.gn, self.bu = np.random.randint(0, 254), np.random.randint(0, 254), np.random.randint(0, 254)
        self.birthtime = 0 # time utc when planet was launched initially set when ALL planets are fired
    def draw(self):
        """
        draw a planet
        """
        # print("drawing a planet")
        pygame.draw.circle(self.screen, (self.rd, self.gn, self.bu), (self.x, self.y), self.r)
        # iterate the age by 0.1

    def move(self):
        """
        move a planet
        """

        # print(self.x, self.y)

        # Euler-Cromer method to new position:

        # First calculate the force on the body using the newtonian ...
        # done already in game loop

        # Then update momentum using the force*stepsize
        # print("self.momentum:  {}".format(self.momentum))
        # print("self.force:  {}".format(self.force))
        self.momentum[0] = self.momentum[0] + self.force[0] * self.dt
        self.momentum[1] = self.momentum[1] + self.force[1] * self.dt

        # Finally, update the position using the momentum
        self.x = self.x + self.momentum[0] / (self.mass * self.dt)
        self.y = self.y + self.momentum[1] / (self.mass * self.dt)

        # l r t b
        # if ((self.x <= self.r) or (self.x >= WIDTH)) and np.linalg.norm(self.velocity) == 0:
        # if ((self.x <= self.r) or (self.x >= WIDTH) or (self.y <= self.r) or (self.y >= HEIGHT)) and np.linalg.norm(self.velocity) == 0 and self.alive == True:
        if ((self.x <= self.r) or (self.x >= WIDTH) or (self.y <= self.r) or (self.y >= HEIGHT)) and self.alive == True:
            planets.remove(self)
            self.destroy(deathmsg="blasting off again...")

        # print("Pos:  {},{}".format(self.x, self.y))
        # print("Accl:  {},{}".format(self.acceleration[0], self.acceleration[1]))
        # print("V:  {},{}".format(self.velocity[0], self.velocity[1]))

    def destroy(self, deathmsg="--------"):
        """
        destroy any planet that goes offscreen
        """
        logging.debug(deathmsg)
        self.deathtime = datetime.utcnow()
        self.age = (self.deathtime - self.birthtime)
        self.age = self.age.total_seconds()
        x, y = np.random.randint(200, 300), np.random.randint(200, 300)
        self.r, self.x, self.y, self.velocity, self.momentum, self.alive = 0, -x, -y, [0, 0], [0, 0], False
        logging.info(f"SCORE: {self.age}s")
        # if np.linalg.norm(self.velocity) > 0:


def play_human():

    """
    Play the game (for humans)
    """


    logging.info("a human is starting...")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # A var to indicate if an agent has placed the first planet.
    started_placement = False

    # menu buttons
    # (x, y), (l, w)
    star = Star(screen, WIDTH/2, HEIGHT/2, 40)

    # planets = []
    stars = [star]

    clicks = 0
    logging.info(f"clicks {clicks}")

    while running:

        mx, my = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        # print(SCORE)

        star.draw()
        CLICKED = False

        # sun eats planets
        for pnt in planets:
            if euclidian_distance(star, pnt) <= star.r * 1.2:
                # logging.info("yum")
                planets.remove(pnt)
                pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
                    print("")
                    # logging.info("collision")
                    n = np.random.randint(0, 2)
                    if n == 1:
                        planets.remove(pnt1)
                        pnt1.destroy(deathmsg="multi-planet collision")
                    else:
                        planets.remove(pnt2)
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
        for body in (planets + stars):
            body.force = 0
            # setattr(body, "force", 0)

        # update gravity for all bodies
        for body1 in (planets + stars):
            for body2 in (planets + stars):
                # if body not in stars:
                #     pass
                if body1 != body2:
                    body1.force += law_of_gravitation(body2, body1)


        #########################
        #### MOVE PLANETS     ###
        #########################
        for body in planets:
            if body.active:
                body.draw()
                body.move()

        # planet star collision
        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():
            # BUG: the window launches, and the event loop is entered after the first mousedown. Then

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # pygame.display.set_caption("spooky outer space")
                running = False

            # mouseclick logic + menu traversal

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                CLICKED = True

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                started_placement = True
                CLICKED = True
                clicks += 1
                logging.info("clicks {}".format(clicks))
                planet1 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                planets.append(planet1)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 1:
                clicks += 1
                logging.info("clicks {}".format(clicks))
                planet2 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                planets.append(planet2)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 2:
                clicks += 1
                logging.info("clicks {}".format(clicks))
                planet3 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                planets.append(planet3)
                logging.debug(f"ALL PLANETS HAVE BECOME ACTIVE (STARTED MOVING)")
                for pnt in planets:
                    pnt.active = True
                    pnt.birthtime = datetime.utcnow()

            # example click code
            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("example")

        # scores_shown = 0
        # if scores_shown == 0 and all_planets_destroyed(planets) and all_planets_active(planets) and CLICKED == True:
        #     # SCORE = sum([pnt.age for pnt in planets if pnt.alive == False])
        #     SCORE = sum([pnt.age for pnt in planets])
        #     logging.info(f"Final Score= {SCORE}")
        #     scores_shown = 1

        # text_box(f"score = {SCORE}", 15, screen, WIDTH - (WIDTH - 50), -350 + (HEIGHT / 2))
        scores_shown = 0
        if scores_shown == 0 and all_planets_destroyed(planets) and all_planets_active(planets):# and started_placement:
            # SCORE = sum([pnt.age for pnt in planets if pnt.alive == False])
            SCORE = sum([pnt.age for pnt in planets])


            # logging.info(f"Final Score= {SCORE}")
            scores_shown = 1

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)

def all_planets_destroyed(pnts):
    if len([pnt for pnt in pnts if pnt.alive == False]) == len([pnt for pnt in pnts]):
        return True
    return False

def all_planets_active(pnts):
    if len([pnt for pnt in pnts if pnt.active == True]) == len([pnt for pnt in pnts]):
        return True
    return False

def play_NEAT():
    # stuff happens when function is intially run

    # imperatives
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # during gameplay but not events
    while running:

        clicked = False

        # display
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        text_box("NEAT AI player", 15, screen, - 50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # pygame.display.set_caption("spooky solar system")
                running = False

            # mouseclick logic
            mx, my = pygame.mouse.get_pos()

            # menu traversal
            if event.type == MOUSEBUTTONDOWN:
                clicked = True

            # example event action
            # if button.collidepoint(mx, my) and clicked:
            #     print("button clicked")





            # update the bg
            pygame.display.update()

        # refresh rate
        clock.tick(FPS)


def play_r_learning():
    # stuff happens when function is intially run

    # imperatives
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # during gameplay but not events
    while running:

        clicked = False

        # display
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        text_box("reinforcement learning player", 15, screen, -250 + (WIDTH / 2), -350 + (HEIGHT / 2))

        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # pygame.display.set_caption("spooky solar system")
                running = False

            # mouseclick logic
            mx, my = pygame.mouse.get_pos()

            # menu traversal
            if event.type == MOUSEBUTTONDOWN:
                clicked = True

            # example event action
            # if button.collidepoint(mx, my) and clicked:
            #     print("button clicked")





            # update the bg
            pygame.display.update()

        # refresh rate
        clock.tick(FPS)


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
        self.rd, self.gn, self.bu = np.random.randint(0,254), np.random.randint(0,254), np.random.randint(0,254)

    def draw(self):
        pygame.draw.circle(self.screen, (39, 176, 144), (self.x, self.y), self.r)
        # screen.blit(pygame.image.load("../data/s10.png"), (self.x, self.y))
        # pygame.image.load("../data/sun1.png")
        # screen.blit(screen, (self.x,self.y))


def window_template():
    # stuff happens when function is intially run

    # imperatives
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # during gameplay but not events
    while running:

        clicked = False

        # display
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        text_box("template window", 50, screen, -59 + (WIDTH / 2), -200 + (HEIGHT / 2))

        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # pygame.display.set_caption("spooky solar system")
                running = False

            # mouseclick logic
            mx, my = pygame.mouse.get_pos()

            # menu traversal
            if event.type == MOUSEBUTTONDOWN:
                clicked = True

            # example event action
            # if button.collidepoint(mx, my) and clicked:
            #     print("button clicked")

            # update the bg
            pygame.display.update()

        # refresh rate
        clock.tick(FPS)


if __name__ == '__main__':
    SCORE = 0
    planets = []
    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    # logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    WIDTH = 1400
    HEIGHT = 800
    FPS = 144
    CLOCK = pygame.time.Clock()

    main_menu()

