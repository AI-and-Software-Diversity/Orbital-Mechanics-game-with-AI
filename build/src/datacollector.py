import game
import numpy as np

class Collector:

    def add_to_csv(self, info):
        """
        Order: [xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...,
                StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, avgSpeedP1...,
                avgAgeP,avgAgeP1..,StepSizeP,bigG]

        """
        pass


class DataGenrator:

    def __init__(self, WIDTH, HEIGHT, *args, **kwargs):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.args = args
        self.kwargs = kwargs



    def getWidth(self):
        return self.WIDTH

    # ...
