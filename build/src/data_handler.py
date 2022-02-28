# import game
import os
import numpy as np

class Collector:

    def __init__(self, file_to_use):
        self.file_to_use = file_to_use

        self.csv_format =  "[xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...," +\
                            "StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, " +\
                            "avgSpeedP1...,avgAgeP,avgAgeP1..,StepSizeP,bigG]"

        # ADDING THE DATA FORMAT SPECIFIED TO EMPTY CSV
        if not os.path.isfile(f"../data/{self.file_to_use}.csv"):
            with open(f"../data/{self.file_to_use}.csv", "a", newline="\n" ) as file:
                file.write(self.csv_format)

    def add_to_csv(self, data_to_add):
        """
        Reference:
                https://www.youtube.com/watch?v=MWYRGLKMzAQ

        Order: [xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...,
                StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, avgSpeedP1...,
                avgAgeP,avgAgeP1..,StepSizeP,bigG]

        Be sure to use setattr() if you want to use a different default file format...
        """

        # ADDING THE NEW DATA
        print("MEWWWWWWWWWWWWWWWW")
        one_line = ""
        for var in data_to_add:
            one_line += var + ","

        with open(f"../data/{self.file_to_use}.csv", "a", newline="\n") as file:
            file.write(data_to_add + "\n")
collector = Collector(f"ghgd")
collector.add_to_csv("1")

class DataGenrator:
    """
    Well create an instanciable objects whose paramets will be used as varibales that can be used to train the mondel.

    Every parameter will be callable with a get method

    Every parameter will have a default argument to encourage the user to only specify certain parameters when
    they want to train.

    """

    order="[xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...," + \
    "StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, " + \
    "avgSpeedP1...,avgAgeP,avgAgeP1..,StepSizeP,bigG]"

    def __init__(self, WIDTH, HEIGHT, *args, **kwargs):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.args = args
        self.kwargs = kwargs



    # self.stars[0].x, self.stars[0].y, self.planet1.x, self.planet1.y,
    # self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
    # self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
    # self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
    # self.planet1.r,
    # self.planet2.r,
    # self.planet3.r,
    # self.stars[0].mass,
    # game.getWidth(), game.getHeight()

    def getWidth(self):
        return self.WIDTH


    # ...
