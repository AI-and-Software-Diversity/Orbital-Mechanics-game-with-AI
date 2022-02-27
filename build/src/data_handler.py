import game
import numpy as np

class Collector:

    def __init__(self, file_to_use):
        self.file_to_use = file_to_use

    def add_to_csv(self, data_to_add):
        """
        Reference:
                https://www.youtube.com/watch?v=MWYRGLKMzAQ

        Order: [xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...,
                StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, avgSpeedP1...,
                avgAgeP,avgAgeP1..,StepSizeP,bigG]

        """
        now = "terst"
        with open(f"../data/{self.file_to_use}.csv", "a", newline="\n") as file:
            file.write(data_to_add )
        # add(data_to_add)

# Collector.add_to_csv([["score",7], ["time",19])
import time
collector = Collector(f"{time.strftime('%m.%d_%H:%M:%S')}")
collector.add_to_csv("pls")
collector.add_to_csv("===============")


#         add(data_to_add)
#
# Collector.add_to_csv([["score",7], ["time",19])


class DataGenrator:
    """
    Well create an instanciable objects whose paramets will be used as varibales that can be used to train the mondel.

    Every parameter will be callable with a get method

    Every parameter will have a default argument to encourage the user to only specify certain parameters when
    they want to train.

    """
    def __init__(self, WIDTH, HEIGHT, *args, **kwargs):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.args = args
        self.kwargs = kwargs



    def getWidth(self):
        return self.WIDTH


    # ...
