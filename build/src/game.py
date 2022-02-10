import pygame
from pygame.locals import *
import sys
import numpy as np
import scipy
import scipy.constants
import math

WIDTH = 1400
HEIGHT = 800
FPS = 144
CLOCK = pygame.time.Clock()

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
    F_12 = G(m_1 * m_2/r^2)
    https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

    The specific method used was the Euler-Cromer method
    https://www.youtube.com/watch?v=rPkJtpVJwSw&list=PLdCdV2GBGyXOOutOEKggaZo1rCHtUYh-A

    Which followed this tutorial
    https://www.youtube.com/watch?v=4ycpvtIio-o&list=PLdCdV2GBGyXOExPW4u8H88S5mwrx_8vWK&index=2
    """

    # F = (100 * body1.mass * body2.mass) / np.linalg.norm((np.array([body1.x, body1.y])-np.array([body2.x, body2.y]))) ** 2
    # direction_vector = np.array([-body2.x, body2.y]) - np.array([-body1.x, body1.y])
    # if direction_vector[1] == 0:
    #     tangent = 0
    # else:
    #     tangent = math.tan(direction_vector[0]/direction_vector[1])
    # if tangent == 0:
    #     angle = 0
    # else:
    #     angle = math.atan(tangent)
    # F_vector = F*math.sin(angle), F*math.cos(angle)

    G = 1000
    r_vec = np.array([body1.x, body1.y])-np.array([body2.x, body2.y])
    r_mag = np.linalg.norm((np.array([body1.x, body1.y])-np.array([body2.x, body2.y])))
    r_hat = r_vec/r_mag
    F_mag = G * body1.mass * body2.mass / r_mag**2
    F_vector = F_mag * r_hat
    print("===========================")
    print(body1.mass)
    print(body2.mass)
    print(r_mag)
    print(r_mag**2)
    print(F_vector)
    print("===========================")
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
                print("*click*")
                clicked = True



            # update the bg
            pygame.display.update()

        CLOCK.tick(FPS)


class Planet:

    def __init__(self, screen, x, y, r, velocity, force):
        print("initialising a planet")
        self.dt = 0.000001 # step size
        self.x = x
        self.y = y
        self.r = r
        # self. mass = 3.3e+24 * r
        self. mass = r
        self.velocity = velocity
        self.acceleration = force
        self.screen = screen
        self.force = force
        self.momentum = [0, 0]
        # surface, color, center, radius
        self.rd, self.gn, self.bu = np.random.randint(0, 254), np.random.randint(0, 254), np.random.randint(0, 254)

    def draw(self):
        """
        draw a planet
        """
        # print("drawing a planet")
        pygame.draw.circle(self.screen, (self.rd, self.gn, self.bu), (self.x, self.y), self.r)

    def move(self):
        """
        move a planet
        """

        print(self.x, self.y)

        # Euler-Cromer method to new position:

        # First calculate the force on the body using the newtonian ...
        # done already in game loop

        # Then update momentum using the force*stepsize
        print("self.momentum:  {}".format(self.momentum))
        print("self.force:  {}".format(self.force))
        self.momentum[0] = self.momentum[0] + self.force[0] * self.dt
        self.momentum[1] = self.momentum[1] + self.force[1] * self.dt

        # Finally, update the position using the momentum
        self.x = self.x + self.momentum[0]/(self.mass * self.dt)
        self.y = self.y + self.momentum[1]/(self.mass * self.dt)

        # print("Pos:  {},{}".format(self.x, self.y))
        # print("Accl:  {},{}".format(self.acceleration[0], self.acceleration[1]))
        # print("V:  {},{}".format(self.velocity[0], self.velocity[1]))


    def destroy(self):
        """
        destroy any planet that goes offscreen
        """
        if np.linalg.norm(self.velocity) > 0:
            print("boom...")

        self.r, self.x, self.y, self.velocity, self.momentum = 0, -200, -200, [0, 0], [0, 0]


def play_human():

    """
    Play the game (for humans)
    """

    print("a human is starting...")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # window title

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")

    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    # llbutton = pygame.Rect((-200 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # lbutton = pygame.Rect((-100 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # mbutton = pygame.Rect((WIDTH / 2, HEIGHT / 2), (30, 10))
    # rbutton = pygame.Rect((100 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # rrbutton = pygame.Rect((200 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # planet = Planet(screen, 20, 20, 20, [122,25], [1, 1])
    planet = Planet(screen, 30, 30, 10, [0, 30], [0, 30])
    # star = Star(screen, WIDTH/4, HEIGHT/5, 20)
    star = Star(screen, WIDTH/2, HEIGHT/2, 20)




    while running:
        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        planet.move()
        planet.draw()
        CLICKED = False

        # walls
        # rl
        # if WIDTH - planet.x == planet.r or planet.x - planet.r <= 0:
        #     print("side wall")
        #     planet.velocity[0] = -1 * planet.velocity[0]
        #
        # #t b
        # if HEIGHT - planet.y == planet.r or planet.y + planet.r <= 0:
        #     print("vert wall")
        #     planet.velocity[1] = -1 * planet.velocity[1]


        # offscreen checker
        # if planet.x > 200 and planet:
        #     pass
        # l r
        if (planet.x <= planet.r) or (planet.x >= WIDTH):
            planet.destroy()
        # t b
        if (planet.y <= planet.r) or (planet.y >= HEIGHT):
            planet.destroy()

        # force controller

        # planet.force = get_force_vector_from_gravity(star, planet)
        planet.force = law_of_gravitation(star, planet)

        # planet star collision


        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # pygame.display.set_caption("spooky outer space")
                running = False



            # mouseclick logic + menu traversal
            mx, my = pygame.mouse.get_pos()

            if event.type == MOUSEBUTTONDOWN:
                CLICKED = True

            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("ll button")
            #
            # if lbutton.collidepoint(mx, my) and CLICKED:
            #     print("l button")
            #
            # if mbutton.collidepoint(mx, my) and CLICKED:
            #     print("m button")
            #
            # if rbutton.collidepoint(mx, my) and CLICKED:
            #     print("r button")
            #
            # if rrbutton.collidepoint(mx, my) and CLICKED:
            #     print("rr button")




        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)


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


main_menu()
