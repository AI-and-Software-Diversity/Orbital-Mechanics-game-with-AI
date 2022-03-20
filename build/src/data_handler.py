import os
import random


class Collector:

    def __init__(self, file_to_use):
        self.file_to_use = file_to_use

        # self.csv_format =  "[xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...," +\
        #                     "StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, " +\
        #                     "avgSpeedP1...,avgAgeP,avgAgeP1..,StepSizeP,bigG]"
        self.csv_format = "was succesful, reward, actual ca, target ca, runs completed"
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
        one_line = ""
        for var in data_to_add:
            one_line += str(var) + ","
        one_line = one_line[0:-1]
        with open(f"../data/{self.file_to_use}.csv", "a", newline="\n") as file:
            file.write(one_line + "\n")

# collector = Collector(f"ghgd")
# var1 = "1"
# var2 = 2
# var3 = 3
# collector.add_to_csv([var1, var2])

class DataGenrator:
    """
    Well create an instanciable objects whose paramets will be used as varibales that can be used to train the mondel.

    Every parameter will be callable with a get method

    Every parameter will have a default argument to encourage the user to only specify certain parameters when
    they want to train.

    """

    order="[xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...," + \
    "StepSizeP,num_planets,num_stars, Score,OptimalScore," + \
    "FinalScore%DistanceFromOptimalScore, " + \
    "avgSpeedP1...,avgAgeP,avgAgeP1..,StepSizeP,bigG]"
    # everything from the last 2 must come from the write to csv method.

    # def __init__(self, xPosS1, yPosS1, xPosP1, xPosP2, xPosP3, yPosP1, yPosP2, yPosP3, xMomP1, xMomP2, xMomP3, yMomP1, yMomP2, yMomP3, WIDTH, HEIGHT, target_game_time, massS1, massP1, massP2, massP3):

    def __init__(self, n_planets, n_stars, planet_mom_scalar, planet_rad, star_x_pos, star_y_pos,
                 star_rad, width, height, target_game_time, n_envs):
        self.width = width
        self.height = height
        self.n_planets = n_planets
        self.n_stars = n_stars
        self.optimal_game_time = target_game_time / n_planets
        self.planet_mom_scaler = planet_mom_scalar
        self.planet_mass = planet_rad
        self.star_x_pos = star_x_pos
        self.star_y_pos = star_y_pos
        self.star_rad = star_rad
        self.target_game_time = target_game_time
        self.n_envs = n_envs



    # self.stars[0].x, self.stars[0].y, self.planet1.x, self.planet1.y,
    # self.planet2.x, self.planet2.y, self.planet3.x, self.planet3.y,
    # self.planet1_momentum[0], self.planet1_momentum[1], self.planet2_momentum[0],
    # self.planet2_momentum[1], self.planet3_momentum[0], self.planet3_momentum[1],
    # self.planet1.r,
    # self.planet2.r,
    # self.planet3.r,
    # self.stars[0].mass,
    # game.getWidth(), game.getHeight()


GLBVARS = DataGenrator(
    n_planets=3,
    n_stars=1,
    planet_mom_scalar=0.00005,
    planet_rad=[5, 15],
    star_x_pos=[100, 1300],
    star_y_pos=[100, 700],
    star_rad=[30, 60],
    width=1400,
    height=800,
    target_game_time=8,
    n_envs=1
)

VARS = DataGenrator(
    n_planets=3,
    n_stars=1,
    planet_mom_scalar=0.00005,
    planet_rad=[5, 15],
    star_x_pos=[600, 700],
    star_y_pos=[300, 400],
    star_rad=[30, 60],
    width=1400,
    height=800,
    target_game_time=20,
    n_envs=1
)

VARS = DataGenrator(
    n_planets=3,
    n_stars=1,
    planet_mom_scalar=0.00005,
    planet_rad=[5, 15],
    star_x_pos=[600, 700],
    star_y_pos=[300, 400],
    star_rad=[30, 60],
    width=1400,
    height=800,
    target_game_time=20,
    n_envs=1
)


# GLBVARS = DataGenrator(
#     n_planets=3,
#     n_stars=2,
#     planet_mom_scalar = 0.00005,
#     planet_rad = [10, 10, 10],
#     # star_x_pos = [getWidth()/2],
#     # star_y_pos = [getHeight()/2],
#     star_x_pos = [1400/2, 900],
#     star_y_pos = [800/2, 500],
#     star_mass = [40, 50],
#     star_rad=[40, 50],
#     width = 1400,
#     height = 800,
#     target_game_time = 10,
#     n_envs=1
# )
