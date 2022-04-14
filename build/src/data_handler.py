import os

class Collector:

    def __init__(self, file_to_use, model_type):
        self.file_to_use = file_to_use
        self.model_type = model_type

        # self.csv_format =  "[xPosS1..,yPosS1..,xPosP1...,yPosP1...,xMomP1..,yMomP1..,H,W,TargetTimeGame,MassP1...,MassS1...," +\
        #                     "StepSizeP,num_planets,num_stars, Score,OptimalScore,FinalScore%DistanceFromOptimalScore, " +\
        #                     "avgSpeedP1...,avgAgeP,avgAgeP1..,StepSizeP,bigG]"

        self.csv_format = "was succesful, reward, actual steps, target steps, runs completed"

        # # ADDING THE DATA FORMAT SPECIFIED TO EMPTY CSV
        # # if not os.path.isfile(f"data/{self.model_type}/csvs/{self.file_to_use}.csv"):
        with open(f"data/{self.model_type}/csvs/{self.file_to_use}.csv", "w", newline="\n" ) as file:
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

        # # ADDING THE DATA FORMAT SPECIFIED TO EMPTY CSV
        # with open(f"data/{self.model_type}/csvs/{self.file_to_use}.csv", "w", newline="\n" ) as file:
        #     file.write(self.csv_format)

        # ADDING THE NEW DATA
        one_line = ""
        for var in data_to_add:
            one_line += str(var) + ","
        one_line = one_line[0:-1]
        with open(f"data/{self.model_type}/csvs/{self.file_to_use}.csv", "a", newline="") as file:
            file.write("\n"+ one_line)

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
                 star_rad, width, height, target_game_time, total_steps, n_envs, min_distance_stars,
                 max_distance_stars):
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
        self.total_steps = total_steps
        self.n_envs = n_envs
        self.min_distance_stars = min_distance_stars
        self.max_distance_stars = max_distance_stars

size = 1600
restriction_x = 200
restriction_y = 150

# GLBVARS = DataGenrator(
#     n_planets=3,
#     n_stars=1,
#     planet_mom_scalar=0.00005,
#     planet_rad=[9, 12],
#     star_x_pos=[restriction_x, size - restriction_x],
#     star_y_pos=[restriction_y, int(size / 1.75) - restriction_y],
#     star_rad=[65, 80],
#     width=size,
#     height=size / 1.75,
#     target_game_time=50,
#     total_steps=2300,
#     n_envs=1
# )

GLBVARS = DataGenrator(
    n_planets=1,
    n_stars=3,
    planet_mom_scalar=0.00005,
    planet_rad=[6, 9],
    star_x_pos=[restriction_x, size - restriction_x],
    star_y_pos=[restriction_y, int(size / 1.75) - restriction_y],
    star_rad=[40, 55],
    width=size,
    height=size / 1.75,
    target_game_time=50,
    total_steps=2300,
    n_envs=1,
    min_distance_stars = 400,
    max_distance_stars=600
)
