import pygame
from pygame.locals import *
import sys

WIDTH = 852
HEIGHT = 480


"""
https://www.youtube.com/watch?v=1_H7InPMjaY
https://www.youtube.com/watch?v=a5JWrd7Y_14&t=936s
Used to create basic game window

https://www.youtube.com/watch?v=0RryiSjpJn0
used to help implement main menus
"""

def text_box(str, screen, x, y):
    font = pygame.font.Font('../data/fonts/Rowdies-Regular.ttf', 100)
    text = font.render(str, True, (222,255,222))
    screen.blit(text, (x, y))

def main_menu():

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # running = True

    # window title
    pygame.display.set_caption("spooky solar system")

    # setting up bg
    bg = pygame.image.load("../data/solarsystem.jpg")
    pygame.display.set_icon(bg)





    # menu buttons
    # (x, y), (l, w)
    llbutton = pygame.Rect((-200 + WIDTH / 2, HEIGHT / 2), (30, 10))
    lbutton = pygame.Rect((-100 + WIDTH / 2, HEIGHT / 2), (30, 10))
    mbutton = pygame.Rect((WIDTH / 2, HEIGHT / 2), (30, 10))
    rbutton = pygame.Rect((100 + WIDTH / 2, HEIGHT / 2), (30, 10))
    rrbutton = pygame.Rect((200 + WIDTH / 2, HEIGHT / 2), (30, 10))

    while True:



        CLICKED = False

        # setting up backup background as well as image bg
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))

        text_box("main menu", screen, -59 + (WIDTH/2), -200+(HEIGHT/2))

        pygame.draw.rect(screen, (255, 255, 255), llbutton)
        pygame.draw.rect(screen, (255, 255, 255), lbutton)
        pygame.draw.rect(screen, (255, 255, 255), mbutton)
        pygame.draw.rect(screen, (255, 255, 255), rbutton)
        pygame.draw.rect(screen, (255, 255, 255), rrbutton)

        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # mouseclick logic + menu traversal
            mx, my = pygame.mouse.get_pos()

            if event.type == MOUSEBUTTONDOWN:
                CLICKED = True

            if llbutton.collidepoint(mx, my) and CLICKED:
                print("ll button")
                menu1()

            if lbutton.collidepoint(mx, my) and CLICKED:
                print("l button")
                window_template()

            if mbutton.collidepoint(mx, my) and CLICKED:
                print("m button")

            if rbutton.collidepoint(mx, my) and CLICKED:
                print("r button")

            if rrbutton.collidepoint(mx, my) and CLICKED:
                print("rr button")

            # update the bg
            pygame.display.update()

        clock.tick(144)


def menu1():

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # window title

    # setting up bg
    bg = pygame.image.load("../data/solarsystem.jpg")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    # llbutton = pygame.Rect((-200 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # lbutton = pygame.Rect((-100 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # mbutton = pygame.Rect((WIDTH / 2, HEIGHT / 2), (30, 10))
    # rbutton = pygame.Rect((100 + WIDTH / 2, HEIGHT / 2), (30, 10))
    # rrbutton = pygame.Rect((200 + WIDTH / 2, HEIGHT / 2), (30, 10))

    while running:

        CLICKED = False

        # setting up backup background as well as image bg
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))

        text_box("menu 1", screen, -59 + (WIDTH / 2), -200 + (HEIGHT / 2))

        # pygame.draw.rect(screen, (255, 255, 255), llbutton)
        # pygame.draw.rect(screen, (255, 255, 255), lbutton)
        # pygame.draw.rect(screen, (255, 255, 255), mbutton)
        # pygame.draw.rect(screen, (255, 255, 255), rbutton)
        # pygame.draw.rect(screen, (255, 255, 255), rrbutton)

        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.set_caption("spooky solar system")
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
        clock.tick(144)


def window_template():

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True


    # setting up bg
    bg = pygame.image.load("../data/solarsystem.jpg")
    pygame.display.set_icon(bg)


    while running:

        CLICKED = False

        # setting up backup background as well as image bg
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))

        text_box("template window", screen, -59 + (WIDTH / 2), -200 + (HEIGHT / 2))


        # an event is some interaction with the engine. eg mouseclick
        for event in pygame.event.get():

            # quit logic
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back to main menu
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.set_caption("spooky solar system")
                running = False


            # mouseclick logic + menu traversal
            mx, my = pygame.mouse.get_pos()

            if event.type == MOUSEBUTTONDOWN:
                CLICKED = True

            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("ll button")





            # update the bg
            pygame.display.update()
        clock.tick(144)

main_menu()