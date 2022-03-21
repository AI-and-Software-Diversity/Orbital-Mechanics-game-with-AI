import numpy as np
import pygame
import logging
import time

def euclidian_distance(body1, body2):

    distance = np.abs(np.linalg.norm(
        np.array([body1.x, body1.y]) - np.array([body2.x, body2.y])
    ))

    return distance

def text_box(str, font_size, screen, x, y):
    """
    https://www.fontspace.com/press-start-2p-font-f11591

    :param str:
    :param font:
    :param screen:
    :param x:
    :param y:
    :return:
    """

    font = pygame.font.Font('../../assets/PressStart2P-vaV7.ttf', font_size)
    text = font.render(str, True, (255,255,255))
    screen.blit(text, (x, y))

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
    if body1.mass != 0 and body2.mass != 0:
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
    else:
        return 0

def current_time():
    # return time.time().real
    return round(time.time().real, 2)

def all_planets_destroyed(pnts):
    if len([pnt for pnt in pnts if pnt.alive == False]) == len([pnt for pnt in pnts]):
        return True
    return False

def scale_vectors(vec1, vec2, factor):
    """
    :param vec1: The initial vector (point in space)
    :param vec2: The seconds vector (point in space)
    :return factor: The scaled difference between them (route from vex 2 to vec 1)
    """
    resultant_vec = (np.array(vec1) - np.array(vec2)) / 500000


    return (resultant_vec) * factor

def not_created_yet():
    print("THIS HAS NOT YET BEEN IMPLEMENTED")

if __name__ == '__main__':
    pass