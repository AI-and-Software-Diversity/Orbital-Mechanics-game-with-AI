from pygame.locals import *
import sys
from helpers import *
from bodies import *

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
            pygame.event.wait()
            play_human()

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
        if rbutton.collidepoint(mx, my) and clicked:
            menu_template()

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



def play_human():

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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    star = Star(screen, WIDTH/2, HEIGHT/2, 40)
    planets = []
    stars = [star]
    clicks = 0

    print("\n")
    logging.info(f"STARTING")

    while running:

        # set the age of each planet that is "active"
        for pnt in planets:
            if pnt.alive:
                pnt.age = (current_time() - pnt.birthtime).__round__(2)

        # logging.info(current_time_s)
        mx, my = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        CLICKED = False

        # sun eats planets
        for pnt in planets:
            if euclidian_distance(star, pnt) <= star.r * 1.2:
                # cumulative_age += pnt.age
                logging.info(f"current cml: {cumulative_age}")
                pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
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
            # setattr(body, "force", 0)

        # calculate gravity
        for body1 in (planets + stars):
            for body2 in (planets + stars):
                # if body not in stars:
                #     pass
                if body1 != body2:
                    body1.force += law_of_gravitation(body2, body1)

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
                logging.info("*CLICK*")
                CLICKED = True

            ####################
            # PLACING PLANETS ##
            ####################
            # pygame.event.wait()
            #p1
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                planet1 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                logging.info(f"P1 POS {mx, my}")

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 0:
                clicks += 1
                planet1_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P1M: {planet1_momentum}")
                setattr(planet1, "momentum", planet1_momentum)

            #p2
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 1:
                planet2 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                logging.info(f"P2 POS {mx, my}")

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 1:
                clicks += 1
                planet2_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P2M: {planet2_momentum}")
                setattr(planet2, "momentum", planet2_momentum)

            #p3
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 2:
                planet3 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                planets_in_motion = True
                start_time = current_time()
                logging.info(f"P3 POS {mx, my}")

                planets.append(planet1)
                planets.append(planet2)
                planets.append(planet3)



            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 2:
                planet3_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P3M: {planet3_momentum}")

                setattr(planet3, "momentum", planet3_momentum)
                for pnt in planets:
                    pnt.active = True
                clicks += 1

            ########################
            # PLACING PLANETS END ##
            ########################


            # example click code
            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("example")

        # calculate the score
        # if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score and cumulative_age > 200:
        #     # cumulative_age = sum([pnt.age for pnt in planets])
        #     logging.info(f"Final Score = {(current_time() - start_time).__round__(2)}")
        #     have_displayed_score = True
        if not have_displayed_score and cumulative_age > 200:
            # cumulative_age = sum([pnt.age for pnt in planets])
            score = current_time() - start_time
            logging.info(f"Final Score = {score}")
            have_displayed_score = True
            running = False

        # off screen
        for pnt in planets:
            if ((pnt.x <= pnt.r) or (pnt.x >= WIDTH) or (pnt.y <= pnt.r) or (pnt.y >= HEIGHT)) and pnt.alive == True:
                # cumulative_age += pnt.age
                logging.info(f"current cml: {cumulative_age}")
                pnt.destroy(deathmsg="blasting off again...")

        # updating cml score
        cumulative_age = sum([pnt.age for pnt in planets])

        # ending game
        if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score:
            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)

def play_NEAT():
    pass

def play_r_learning():
    pass
# human player
def human_template():

    planets_in_motion = False
    have_displayed_score = False
    start_time = 0
    cumulative_age = 0
    score = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    star = Star(screen, WIDTH / 2, HEIGHT / 2, 40)
    planets = []
    stars = [star]
    clicks = 0

    print("\n")
    logging.info(f"STARTING")

    while running:

        # set the age of each planet that is "active"
        for pnt in planets:
            if pnt.alive:
                pnt.age = (current_time() - pnt.birthtime).__round__(2)

        # logging.info(current_time_s)
        mx, my = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        CLICKED = False

        # sun eats planets
        for pnt in planets:
            if euclidian_distance(star, pnt) <= star.r * 1.2:
                # cumulative_age += pnt.age
                logging.info(f"current cml: {cumulative_age}")
                pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
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
            # setattr(body, "force", 0)

        # calculate gravity
        for body1 in (planets + stars):
            for body2 in (planets + stars):
                # if body not in stars:
                #     pass
                if body1 != body2:
                    body1.force += law_of_gravitation(body2, body1)

        # move and draw planets
        for body in planets:
            if body.active:  # and body.mass != 0:
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
                logging.info("*CLICK*")
                CLICKED = True

            ####################
            # PLACING PLANETS ##
            ####################
            # p1
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                planet1 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                logging.info(f"P1 POS {mx, my}")

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 0:
                clicks += 1
                planet1_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P1M: {planet1_momentum}")
                setattr(planet1, "momentum", planet1_momentum)

            # p2
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 1:
                planet2 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                logging.info(f"P2 POS {mx, my}")

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 1:
                clicks += 1
                planet2_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P2M: {planet2_momentum}")
                setattr(planet2, "momentum", planet2_momentum)

            # p3
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 2:
                planet3 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                planets_in_motion = True
                start_time = current_time()
                logging.info(f"P3 POS {mx, my}")

                planets.append(planet1)
                planets.append(planet2)
                planets.append(planet3)



            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 2:
                planet3_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P3M: {planet3_momentum}")

                setattr(planet3, "momentum", planet3_momentum)
                for pnt in planets:
                    pnt.active = True
                clicks += 1

            ########################
            # PLACING PLANETS END ##
            ########################

            # example click code
            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("example")

        # calculate the score
        # if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score and cumulative_age > 200:
        #     # cumulative_age = sum([pnt.age for pnt in planets])
        #     logging.info(f"Final Score = {(current_time() - start_time).__round__(2)}")
        #     have_displayed_score = True
        if not have_displayed_score and cumulative_age > 200:
            # cumulative_age = sum([pnt.age for pnt in planets])
            score = current_time() - start_time
            logging.info(f"Final Score = {score}")
            have_displayed_score = True
            running = False

        # off screen
        for pnt in planets:
            if ((pnt.x <= pnt.r) or (pnt.x >= WIDTH) or (pnt.y <= pnt.r) or (
                    pnt.y >= HEIGHT)) and pnt.alive == True:
                # cumulative_age += pnt.age
                logging.info(f"current cml: {cumulative_age}")
                pnt.destroy(deathmsg="blasting off again...")

        # updating cml score
        cumulative_age = sum([pnt.age for pnt in planets])

        # ending game
        if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score:
            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)

# incomplete for now
def ai_template():

    planets_in_motion = False
    have_displayed_score = False
    start_time = 0
    cumulative_age = 0
    score = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    star = Star(screen, WIDTH / 2, HEIGHT / 2, 40)
    planets = []
    stars = [star]
    clicks = 0

    print("\n")
    logging.info(f"STARTING")

    while running:

        # set the age of each planet that is "active"
        for pnt in planets:
            if pnt.alive:
                pnt.age = (current_time() - pnt.birthtime).__round__(2)

        # logging.info(current_time_s)
        mx, my = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        CLICKED = False

        # sun eats planets
        for pnt in planets:
            if euclidian_distance(star, pnt) <= star.r * 1.2:
                # cumulative_age += pnt.age
                logging.info(f"current cml: {cumulative_age}")
                pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
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
            # setattr(body, "force", 0)

        # calculate gravity
        for body1 in (planets + stars):
            for body2 in (planets + stars):
                # if body not in stars:
                #     pass
                if body1 != body2:
                    body1.force += law_of_gravitation(body2, body1)

        # move and draw planets
        for body in planets:
            if body.active:  # and body.mass != 0:
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
                logging.info("*CLICK*")
                CLICKED = True

            ####################
            # PLACING PLANETS ##
            ####################
            # p1
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                planet1 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                logging.info(f"P1 POS {mx, my}")

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 0:
                clicks += 1
                planet1_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P1M: {planet1_momentum}")
                setattr(planet1, "momentum", planet1_momentum)

            # p2
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 1:
                planet2 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                logging.info(f"P2 POS {mx, my}")

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 1:
                clicks += 1
                planet2_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P2M: {planet2_momentum}")
                setattr(planet2, "momentum", planet2_momentum)

            # p3
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 2:
                planet3 = Planet(screen, mx, my, 10, [0, 0], [0, 0])
                prev_x, prev_y = mx, my
                planets_in_motion = True
                start_time = current_time()
                logging.info(f"P3 POS {mx, my}")

                planets.append(planet1)
                planets.append(planet2)
                planets.append(planet3)



            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 2:
                planet3_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                logging.info(f"P3M: {planet3_momentum}")

                setattr(planet3, "momentum", planet3_momentum)
                for pnt in planets:
                    pnt.active = True
                clicks += 1

            ########################
            # PLACING PLANETS END ##
            ########################

            # example click code
            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("example")

        # calculate the score
        # if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score and cumulative_age > 200:
        #     # cumulative_age = sum([pnt.age for pnt in planets])
        #     logging.info(f"Final Score = {(current_time() - start_time).__round__(2)}")
        #     have_displayed_score = True
        if not have_displayed_score and cumulative_age > 200:
            # cumulative_age = sum([pnt.age for pnt in planets])
            score = current_time() - start_time
            logging.info(f"Final Score = {score}")
            have_displayed_score = True
            running = False

        # off screen
        for pnt in planets:
            if ((pnt.x <= pnt.r) or (pnt.x >= WIDTH) or (pnt.y <= pnt.r) or (
                    pnt.y >= HEIGHT)) and pnt.alive == True:
                # cumulative_age += pnt.age
                logging.info(f"current cml: {cumulative_age}")
                pnt.destroy(deathmsg="blasting off again...")

        # updating cml score
        cumulative_age = sum([pnt.age for pnt in planets])

        # ending game
        if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score:
            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)

def menu_template():


    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../data/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    # (x, y), (l, w)
    llbutton = pygame.Rect((WIDTH/5, HEIGHT / 2), (30, 10))
    lbutton = pygame.Rect((2*WIDTH/5, HEIGHT / 2), (30, 10))
    rbutton = pygame.Rect((3*WIDTH/5, HEIGHT / 2), (30, 10))
    rrbutton = pygame.Rect((4*WIDTH/5, HEIGHT / 2), (30, 10))

    while running:

        mx, my = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))

        # TITLE AND BUTTONS

        text_box("WIP", 50, screen, -200 + (WIDTH / 2), -200 + (HEIGHT / 2))

        text_box("PLACEHOLDER 1", 10, screen, WIDTH / 5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), llbutton)

        if llbutton.collidepoint(mx, my) and clicked:
            logging.debug("llbutton")

        text_box("PLACEHOLDER 2", 10, screen, 2 * WIDTH / 5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), lbutton)
        if lbutton.collidepoint(mx, my) and clicked:
            logging.debug("lbutton")

        text_box("PLACEHOLDER 3", 10, screen, 3 * WIDTH / 5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), rbutton)
        if rbutton.collidepoint(mx, my) and clicked:
            logging.debug("rbutton")

        text_box("PLACEHOLDER 4", 10, screen, 4 * WIDTH / 5, 30 + HEIGHT / 2)
        pygame.draw.rect(screen, (255, 255, 255), rrbutton)
        if rrbutton.collidepoint(mx, my) and clicked:
            logging.debug("rrbutton")

        clicked = False

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

            # if llbutton.collidepoint(mx, my) and CLICKED:
            #     print("example")

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                logging.debug("*click*")
                clicked = True

        # ending game
        condition = False
        if condition:
            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)

WIDTH = 1400
HEIGHT = 800

if __name__ == '__main__':

    fmt = '[%(levelname)s] %(asctime)s - %(message)s '
    # l1 = logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)

    # logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=fmt)
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    FPS = 144
    CLOCK = pygame.time.Clock()

    main_menu()

