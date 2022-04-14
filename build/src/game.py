from pygame.locals import *
import sys
import time
import bodies
import helpers
import pygame
import logging
import numpy as np
import data_handler


def main_menu():

    """
    https://www.youtube.com/watch?v=1_H7InPMjaY
    https://www.youtube.com/watch?v=a5JWrd7Y_14&t=936s
    Used to create basic game window

    https://www.youtube.com/watch?v=0RryiSjpJn0
    used to help implement main menus
    """
    pygame.init()

    screen = pygame.display.set_mode((data_handler.GLBVARS.width, data_handler.GLBVARS.height))
    # running = True

    # window title
    pygame.display.set_caption("spooky outer space")

    # setting up bg
    bg = pygame.image.load("assets/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)

    llbutton = pygame.Rect((data_handler.GLBVARS.width / 5, data_handler.GLBVARS.height / 2), (30, 10))
    lbutton = pygame.Rect((2 * data_handler.GLBVARS.width / 5, data_handler.GLBVARS.height / 2), (30, 10))
    mbutton = pygame.Rect((3 * data_handler.GLBVARS.width / 5, data_handler.GLBVARS.height / 2), (30, 10))
    rbutton = pygame.Rect((4 * data_handler.GLBVARS.width / 5, data_handler.GLBVARS.height / 2), (30, 10))

    clicked = None
    frame_count = 0

    test_time = time.time().real
    while True:

        if frame_count == FPS:
            frame_count = 0
        else:
            frame_count += 1


        mx, my = pygame.mouse.get_pos()

        # setting up backup background as well as image bg
        screen.blit(bg, (0, 0))

        helpers.text_box("main menu", 50, screen, -200 + (data_handler.GLBVARS.width / 2), -200 + (
                    data_handler.GLBVARS.height / 2))

        helpers.text_box("play (human)", 10, screen, data_handler.GLBVARS.width / 5, 30 + data_handler.GLBVARS.height / 2)
        pygame.draw.rect(screen, (255, 255, 255), llbutton)

        if llbutton.collidepoint(mx, my) and clicked:
            pygame.event.wait()
            # pygame.event.wait()
            # level_1_human()
            # pygame.event.wait()
            menu_template(level_1_human, helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet)

        helpers.text_box("play (NEAT AI)", 10, screen, 2 * data_handler.GLBVARS.width / 5, 30 + data_handler.GLBVARS.height / 2)
        pygame.draw.rect(screen, (255, 255, 255), lbutton)
        if lbutton.collidepoint(mx, my) and clicked:
            pygame.event.wait()
            menu_template(helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet)
            # play_NEAT()

        helpers.text_box("play (RLearn AI)", 10, screen, 3 * data_handler.GLBVARS.width / 5, 30 + data_handler.GLBVARS.height / 2)
        pygame.draw.rect(screen, (255, 255, 255), mbutton)
        # print("playin")
        if mbutton.collidepoint(mx, my) and clicked:
            pygame.event.wait()
            menu_template(helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet)
            # print("m button")
            # play_r_learning()

        helpers.text_box("highscores", 10, screen, 4 * data_handler.GLBVARS.width / 5, 30 + data_handler.GLBVARS.height / 2)
        pygame.draw.rect(screen, (255, 255, 255), rbutton)

        # pygame.event.poll()
        if rbutton.collidepoint(mx, my) and clicked:
            pygame.event.wait()
            menu_template(helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet, helpers.not_created_yet)

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
                logging.debug("*click*")
                clicked = True



            # update the bg
            pygame.display.update()

        CLOCK.tick(FPS)

def level_1_human():

    """
    Play the game (for humans)
    """

    logging.debug("a human is starting...")
    planets_in_motion = False
    have_displayed_score = False
    start_time = 0
    cumulative_age = 0
    score = 0
    # logging.info(f"sum age = {cumulative_age}")
    # clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((data_handler.GLBVARS.width, data_handler.GLBVARS.height))
    running = True

    # setting up bg
    bg = pygame.image.load("assets/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    # star = Star(screen, WIDTH/2, HEIGHT/2, 40)
    planets = []
    num_stars = 1
    stars = []
    for i in range(num_stars):
        stars.append(bodies.Star(screen,
                                 np.random.randint(data_handler.GLBVARS.star_x_pos[0], data_handler.GLBVARS.star_x_pos[1]),
                                 np.random.randint(data_handler.GLBVARS.star_y_pos[0], data_handler.GLBVARS.star_y_pos[1]),
                                 np.random.randint(data_handler.GLBVARS.star_rad[0], data_handler.GLBVARS.star_rad[1])))
    clicks = 0
    clks = 0
    planets_placed = 0
    peas = []
    print("\n")
    logging.info(f"STARTING")

    while running:

        # set the age of each planet that is "active"
        for pnt in planets:
            if pnt.alive:
                pnt.age = (helpers.current_time() - pnt.birthtime).__round__(2)

        # logging.info(helpers.current_time_s)
        mx, my = pygame.mouse.get_pos()
        screen.fill(color=(0,0,0))
        screen.blit(bg, (0, 0))

        helpers.text_box("human player", 15, screen, -50 + (data_handler.GLBVARS.width / 2), -350 + (
                    data_handler.GLBVARS.height / 2))

        helpers.text_box(f"CA: {cumulative_age.__round__(2)}/{data_handler.GLBVARS.target_game_time}", 15,
                         screen, 500 + (data_handler.GLBVARS.width / 2),
                         -350 + (data_handler.GLBVARS.height / 2))

        for star in stars:
            star.draw()

        CLICKED = False

        # sun eats planets
        for pnt in planets:
            for star in stars:
                if helpers.euclidian_distance(star, pnt) <= star.r * 1.2:
                    # cumulative_age += pnt.age
                    logging.info(f"current cml: {cumulative_age}")
                    pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if helpers.euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
                    # logging.info("collision")
                    n = np.random.randint(0, 2)
                    if n == 1:
                        # cumulative_age += pnt.age
                        logging.info(f"current cml: {cumulative_age}")
                        pnt1.destroy(deathmsg="multi-planet collision")
                    else:
                        # cumulative_age += pnt.age
                        logging.info(f"current cml: {cumulative_age}")
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
        for body in (planets + stars):
            body.force = 0

        # calculate gravity
        for body1 in (planets + stars):
            for body2 in (planets + stars):
                if body1 != body2:
                    body1.force += helpers.law_of_gravitation(body2, body1)

        # move and draw planets
        for body in planets:
            if body.active:# and body.mass != 0:
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
                running = False

            # creating planets

            if (event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP) and event.button == 1:
                CLICKED = True

            ####################
            # PLACING PLANETS ##
            ####################


            # planets with a loop TODO add this to rlearn
            num_planets = 3
            if ((event.type == MOUSEBUTTONDOWN and event.button == 1) or (event.type == MOUSEBUTTONUP and event.button == 1)) and (clks < 2*num_planets):
                print(F"clikcs: {clks}")
                # mouse down
                if clks % 2 == 0:
                    print("mouse down")
                    prev_x, prev_y = mx, my
                    logging.info(f"P{clks} POS {mx, my}")
                    print("=======")
                    print(len(peas))
                    print(clks)
                    print("=======")
                    planets_placed += 1
                    clks += 1

                # mouse up
                elif clks % 2 == 1:
                    peas.append(bodies.Planet(screen, mx, my, 10))
                    planet_momentum = helpers.scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                    logging.info(f"P{clks}M: {planet_momentum}")


                    setattr(peas[planets_placed-1], "momentum", planet_momentum)
                    clks += 1

            if clks == 2*num_planets:
                print("setting active")
                for pnt in planets:
                    pnt.active = True
                clks += 1

            planets = peas


        # calculate the score
        if not have_displayed_score and cumulative_age > data_handler.GLBVARS.target_game_time:
            # cumulative_age = sum([pnt.age for pnt in planets])
            score = helpers.current_time() - start_time
            logging.info(f"Final Score = {score}")
            have_displayed_score = True
            running = False

        # # off screen
        # for pnt in planets:
        #     # u d l r
        #     if ((pnt.y < 0) or (pnt.y > data_handler.VARS.height)
        #         or (pnt.x < 0) or (pnt.x > data_handler.VARS.width)) and pnt.alive == True:
        #
        #         # cumulative_age += pnt.age
        #         if np.abs(time.time().real - start_time) < 1.2:
        #             pnt.destroy(deathmsg="SHOT INTO DEATH")
        #         else:
        #             pnt.destroy(deathmsg="blasting off again...")
        for pnt in planets:
            print("off screen")
            # u d l r
            if ((pnt.y < 0) or (pnt.y > data_handler.GLBVARS.height)
                or (pnt.x < 0) or (pnt.x > data_handler.GLBVARS.width)) and pnt.alive == True:

                pnt.destroy(deathmsg="SHOT INTO DEATH")

        # updating cml score
        # print([pnt.alive for pnt in planets])
        if len([pnt.alive for pnt in planets]) > 0:
            cumulative_age = sum([pnt.age for pnt in planets])

        # ending game
        if helpers.all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score:
            print("failure")

            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)


# def menu_template(function_1, function_2, function_3, function_4):
#
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     running = True
#
#     # setting up bg
#     bg = pygame.image.load("assets/gamebg1.png")
#     pygame.display.set_icon(bg)
#
#     # menu buttons
#     # (x, y), (l, w)
#     llbutton = pygame.Rect((WIDTH/5, HEIGHT / 2), (30, 10))
#     lbutton = pygame.Rect((2*WIDTH/5, HEIGHT / 2), (30, 10))
#     rbutton = pygame.Rect((3*WIDTH/5, HEIGHT / 2), (30, 10))
#     rrbutton = pygame.Rect((4*WIDTH/5, HEIGHT / 2), (30, 10))
#
#     clicked = None
#
#     while running:
#
#         mx, my = pygame.mouse.get_pos()
#         screen.blit(bg, (0, 0))
#
#         # TITLE AND BUTTONS
#
#         helpers.text_box("Level Selector", 50, screen, -350 + (WIDTH / 2), -200 + (HEIGHT / 2))
#
#         helpers.text_box("LEVEL 1", 10, screen, WIDTH / 5, 30 + HEIGHT / 2)
#         pygame.draw.rect(screen, (255, 255, 255), llbutton)
#
#         if llbutton.collidepoint(mx, my) and clicked:
#             pygame.event.wait()
#             function_1()
#             logging.debug("llbutton")
#
#         helpers.text_box("LEVEL 2", 10, screen, 2 * WIDTH / 5, 30 + HEIGHT / 2)
#         pygame.draw.rect(screen, (255, 255, 255), lbutton)
#         if lbutton.collidepoint(mx, my) and clicked:
#             pygame.event.wait()
#             function_2()
#             logging.debug("lbutton")
#
#         helpers.text_box("LEVEL 3", 10, screen, 3 * WIDTH / 5, 30 + HEIGHT / 2)
#         pygame.draw.rect(screen, (255, 255, 255), rbutton)
#         if rbutton.collidepoint(mx, my) and clicked:
#             pygame.event.wait()
#             function_3()
#             logging.debug("rbutton")
#
#         helpers.text_box("LEVEL 4", 10, screen, 4 * WIDTH / 5, 30 + HEIGHT / 2)
#         pygame.draw.rect(screen, (255, 255, 255), rrbutton)
#         if rrbutton.collidepoint(mx, my) and clicked:
#             # if at start first event is clicking the button, we enter this thing and bug out
#             pygame.event.wait()
#             function_4()
#             logging.debug("rrbutton")
#
#         clicked = False
#
#         # an event is some interaction with the engine. eg mouseclick
#         for event in pygame.event.get():
#             # BUG: the window launches, and the event loop is entered after the first mousedown. Then
#
#             # quit logic
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#             # back to main menu
#             if event.type == KEYDOWN and event.key == K_ESCAPE:
#                 running = False
#
#             # if llbutton.collidepoint(mx, my) and CLICKED:
#             #     print("example")
#
#             if event.type == MOUSEBUTTONDOWN and event.button == 1:
#                 # logging.debug("*click*")
#                 clicked = True
#
#         # ending game
#         condition = False
#         if condition:
#             running = False
#
#         # update the bg
#         pygame.display.update()
#
#         CLOCK.tick(FPS)



if __name__ == '__main__':


    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    # l1 = logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)

    # logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    FPS = 144
    CLOCK = pygame.time.Clock()


    # main_menu()
    level_1_human()

