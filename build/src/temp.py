def level_1_human():

    """
    Play the game (for humans)
    """

    while running:

        # set the age of each planet that is "active"
        for pnt in planets:
            if pnt.alive:
                pnt.age = (current_time() - pnt.birthtime).__round__(2)

        mx, my = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        CLICKED = False

        # sun eats planets
        for pnt in planets:
            if euclidian_distance(star, pnt) <= star.r * 1.2:
                # cumulative_age += pnt.age
                pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
                    n = np.random.randint(0, 2)
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
                CLICKED = True

            ####################
            # PLACING PLANETS ##
            ####################
            # pygame.event.wait()
            #p1
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                clicks += 1
                planet1 = Planet(screen, mx, my, 10)
                prev_x, prev_y = mx, my

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 1:
                clicks += 1
                planet1_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                setattr(planet1, "momentum", planet1_momentum)

            #p2
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 2:
                clicks += 1
                planet2 = Planet(screen, mx, my, 10)
                prev_x, prev_y = mx, my

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 3:
                clicks += 1
                planet2_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                setattr(planet2, "momentum", planet2_momentum)

            #p3
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 4:
                clicks += 1
                planet3 = Planet(screen, mx, my, 10)
                prev_x, prev_y = mx, my
                planets_in_motion = True
                start_time = current_time()

                planets.append(planet1)
                planets.append(planet2)
                planets.append(planet3)



            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 5:
                planet3_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)

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
        #     have_displayed_score = True
        if not have_displayed_score and cumulative_age > 20:
            # cumulative_age = sum([pnt.age for pnt in planets])
            score = current_time() - start_time
            have_displayed_score = True
            running = False

        # off screen
        for pnt in planets:
            if ((pnt.x <= pnt.r) or (pnt.x >= WIDTH) or (pnt.y <= pnt.r) or (pnt.y >= HEIGHT)) and pnt.alive == True:
                # cumulative_age += pnt.age
                pnt.destroy(deathmsg="blasting off again...")

        # updating cml score
        cumulative_age = sum([pnt.age for pnt in planets])

        # ending game
        if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score:
            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)


def level_1_human():

    """
    Play the game (for humans)
    """

    planets_in_motion = False
    have_displayed_score = False
    start_time = 0
    cumulative_age = 0
    score = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    # setting up bg
    bg = pygame.image.load("../assets/gamebg1.png")
    pygame.display.set_icon(bg)

    # menu buttons
    star = Star(screen, WIDTH/2, HEIGHT/2, 40)
    planets = []
    stars = [star]
    clicks = 0

    while running:

        # set the age of each planet that is "active"
        for pnt in planets:
            if pnt.alive:
                pnt.age = (current_time() - pnt.birthtime).__round__(2)

        mx, my = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))

        text_box("human player", 15, screen, -50 + (WIDTH / 2), -350 + (HEIGHT / 2))

        star.draw()
        CLICKED = False

        # sun eats planets
        for pnt in planets:
            if euclidian_distance(star, pnt) <= star.r * 1.2:
                # cumulative_age += pnt.age
                pnt.destroy(deathmsg="eaten by sun")

        # planet clash
        for pnt1 in planets:
            for pnt2 in planets:
                if euclidian_distance(pnt1, pnt2) < (pnt1.r * 2.3 or pnt2.r * 2.3) and pnt1 != pnt2:
                    n = np.random.randint(0, 2)
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
                CLICKED = True

            ####################
            # PLACING PLANETS ##
            ####################
            # pygame.event.wait()
            #p1
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 0:
                clicks += 1
                planet1 = Planet(screen, mx, my, 10)
                prev_x, prev_y = mx, my

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 1:
                clicks += 1
                planet1_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                setattr(planet1, "momentum", planet1_momentum)

            #p2
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 2:
                clicks += 1
                planet2 = Planet(screen, mx, my, 10)
                prev_x, prev_y = mx, my

            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 3:
                clicks += 1
                planet2_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)
                setattr(planet2, "momentum", planet2_momentum)

            #p3
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and clicks == 4:
                clicks += 1
                planet3 = Planet(screen, mx, my, 10)
                prev_x, prev_y = mx, my
                planets_in_motion = True
                start_time = current_time()

                planets.append(planet1)
                planets.append(planet2)
                planets.append(planet3)



            elif event.type == MOUSEBUTTONUP and event.button == 1 and clicks == 5:
                planet3_momentum = scale_vectors((prev_x, prev_y), (mx, my), 0.2)

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
        #     have_displayed_score = True
        if not have_displayed_score and cumulative_age > 20:
            # cumulative_age = sum([pnt.age for pnt in planets])
            score = current_time() - start_time
            have_displayed_score = True
            running = False

        # off screen
        for pnt in planets:
            if ((pnt.x <= pnt.r) or (pnt.x >= WIDTH) or (pnt.y <= pnt.r) or (pnt.y >= HEIGHT)) and pnt.alive == True:
                # cumulative_age += pnt.age
                pnt.destroy(deathmsg="blasting off again...")

        # updating cml score
        cumulative_age = sum([pnt.age for pnt in planets])

        # ending game
        if all_planets_destroyed(planets) and planets_in_motion and not have_displayed_score:
            running = False

        # update the bg
        pygame.display.update()

        CLOCK.tick(FPS)