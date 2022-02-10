import pygame
from pygame.locals import *
import sys
import numpy as np

WIDTH = 1400
HEIGHT = 800
FPS = 90
CLOCK = pygame.time.Clock()

"""
https://www.youtube.com/watch?v=1_H7InPMjaY
https://www.youtube.com/watch?v=a5JWrd7Y_14&t=936s
Used to create basic game window

https://www.youtube.com/watch?v=0RryiSjpJn0
used to help implement main menus
"""

def text_box(str, font, screen, x, y):
    #https://www.fontspace.com/press-start-2p-font-f11591
    font = pygame.font.Font('../data/fonts/PressStart2P-vaV7.ttf', font)
    text = font.render(str, True, (255,255,255))
    screen.blit(text, (x, y))


def main_menu():

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
                print("event.type == pygame.QUIT")
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


def play_human():
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
    planet = Planet(screen, 20, 20, 20, 1)
    star = Star(screen, 50, 50, 11)

    while running:
        print("1")
        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        planet.move()
        planet.draw()
        CLICKED = False

        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():
            print("2")

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

"""
https://www.youtube.com/watch?v=G8MYGDf_9ho
https://www.pygame.org/docs/ref/draw.html?highlight=circl#pygame.draw.circle

used to create circles with hitboxes
"""


class Star:
    def __init__(self, screen, x, y, r):

        self.x = x
        self.y = y
        self.r = r
        self.mass = r
        self.screen = screen
        # surface, color, center, radius
        self.rd, self.gn, self.bu = np.random.randint(0,254), np.random.randint(0,254), np.random.randint(0,254)

    def draw(self):
        pygame.draw.circle(self.screen, (39, 176, 144), (self.x, self.y), self.r)
        # screen.blit(pygame.image.load("../data/s10.png"), (self.x, self.y))
        # pygame.image.load("../data/sun1.png")
        # screen.blit(screen, (self.x,self.y))


class Planet:

    def __init__(self, screen, x, y, r, force):
        print("initialising a planet")
        self.x = x
        self.y = y
        self.r = r
        self.mass = r
        self.force = force
        self.screen = screen
        # surface, color, center, radius
        self.rd, self.gn, self.bu = np.random.randint(0,254), np.random.randint(0,254), np.random.randint(0,254)

    def draw(self):
        # print("drawing a planet")
        pygame.draw.circle(self.screen, (self.rd, self.gn, self.bu), (self.x, self.y), self.r)

    def move(self):
        # print("moving a planet")
        self.x = self.x + self.force
        self.y = self.y + self.force


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
