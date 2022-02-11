
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

class Planet:

    def __init__(self, screen, x, y, r, velocity, force):
        print("initialising a planet")
        self.dt = 0.000001 # step size
        self.x = x
        self.y = y
        self.r = r
        self. mass = r
        self.velocity = velocity
        self.acceleration = force
        self.screen = screen
        self.force = force
        self.momentum = [0, 0]
        self.rd, self.gn, self.bu = np.random.randint(0, 254), np.random.randint(0, 254), np.random.randint(0, 254)

    def draw(self):
        pygame.draw.circle(self.screen, (self.rd, self.gn, self.bu), (self.x, self.y), self.r)


def main_menu():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    llbutton = pygame.Rect((WIDTH/2, HEIGHT / 2), (30, 10))

    while True:

        mx, my = pygame.mouse.get_pos()

        screen.fill((0,0,0))

        pygame.draw.rect(screen, (255, 255, 255), llbutton)

        if llbutton.collidepoint(mx, my) and clicked:
            print("--")
            pygame.event.wait(100)
            print("---")

            play_human()

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # mouseclick logic + menu traversal
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

            pygame.display.update()

        CLOCK.tick(FPS)

def play_human():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)
    star = Star(screen, WIDTH/2, HEIGHT/2, 40)
    planet1exists = False
    clicks = 0
    print("clicks{}".format(clicks))
    planet1 = None

    while running:

        screen.fill((0, 0, 0))
        planet1_net_force = 0
        star.draw()

        if planet1exists:
            planet1_net_force += 0

        if planet1exists:
            planet1.force = planet1_net_force
            planet1.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.set_caption("spooky outer space")
                running = False

            mx, my = pygame.mouse.get_pos()

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                planet1 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                planet1exists = True
                print("clicks {}".format(clicks))
                print("planet1exists = True")
                clicks += 1

        pygame.display.update()

        CLOCK.tick(FPS)

class Star:

    def __init__(self, screen, x, y, r):

        self.x = x
        self.y = y
        self.r = r
        self.mass = r
        self.screen = screen
        self.rd, self.gn, self.bu = 14,100,49

    def draw(self):
        pygame.draw.circle(self.screen, (39, 176, 144), (self.x, self.y), self.r)

main_menu()
