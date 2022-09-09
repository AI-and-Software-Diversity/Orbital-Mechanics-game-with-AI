import os
import sys

import helpers


class Collector:

    def __init__(self, file_to_use, model_type, csv):
        """
        This class allows you to write towards different CSVs.

        csv: Determines what type of csv you write to
        model_type: chooses the location of the CSV
        """
        self.file_to_use = file_to_use
        self.model_type = model_type

        if csv == "setup":
            self.csv_format = helpers.setup_csv(GLBVARS.n_planets, GLBVARS.n_stars)

        elif csv == "pred":
            self.csv_format = helpers.pred_csv(GLBVARS.n_planets)

        elif csv == "data":
            self.csv_format = "was succesful, reward, actual steps, target steps, runs completed"

        else:
            raise Exception("ERROR: Your csv type has not been specified correctly.")

        # ADDING THE DATA FORMAT SPECIFIED TO EMPTY CSV
        with open(f"data/{self.model_type}/csvs/{self.file_to_use}.csv", "w", newline="\n" ) as file:
            file.write(self.csv_format)

    def add_to_csv(self, data_to_add):

        """
        This method writes information from a python list to a csv.

        Reference: https://www.youtube.com/watch?v=MWYRGLKMzAQ
        """

        # ADDING THE NEW DATA

        one_line = ""
        for var in data_to_add:
            one_line += str(var) + ","
        one_line = one_line[0:-1]

        with open(f"data/{self.model_type}/csvs/{self.file_to_use}.csv", "a", newline="") as file:
            file.write("\n" + one_line)


class DataGenrator:
    """
    Well create an instantiable objects whose parameters will be used as variables that can be used to train the model.

    Every parameter will be callable with a get method

    Every parameter will have a default argument to encourage the user to only specify certain parameters when
    they want to train.

    """
    # everything from the last 2 must come from the write to csv method.


    def __init__(self, n_planets, n_stars, planet_mom_scalar, planet_rad, star_x_pos, star_y_pos,
                 star_rad, width, height, target_game_time, total_steps, n_envs, planet_mom_minimum,
                 position_scalar, timestep,
                 min_distance_stars=0, max_distance_stars=100000000000):
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
        self.planet_mom_minimum = planet_mom_minimum
        self.position_scalar = position_scalar
        self.timestep = timestep

# This instance will be used repeatedly in the Env classes
size = 5600
restriction_x = 250
restriction_y = 350

# This instance will be used repeatedly in the Env classes
GLBVARS = DataGenrator(
    n_planets=1,
    n_stars=2,
    planet_mom_scalar=600,
    planet_mom_minimum = 750,

    planet_rad=[10, 20],
    star_x_pos=[restriction_x, size - restriction_x],
    star_y_pos=[restriction_y, int(size / 1.75) - restriction_y],
    star_rad=[200, 250],
    width=size,
    height=size / 1.75,
    target_game_time=123456,
    total_steps=1600,
    n_envs=10,
    min_distance_stars=0,
    position_scalar=0.95,
    timestep=5,
    max_distance_stars=1000000000000000000
)


# GLBVARS = DataGenrator(
#     n_planets=1,
#     n_stars=3,
#     # planet_mom_scalar=0.00005,
#     planet_mom_scalar=600,
#     planet_mom_minimum = 750,
#     planet_rad=[10, 20],
#     star_x_pos=[restriction_x, size - restriction_x],
#     star_y_pos=[restriction_y, int(size / 1.75) - restriction_y],
#     star_rad=[200, 250],
#     width=size,
#     height=size / 1.75,
#     target_game_time=123456,
#     total_steps=1600,
#     n_envs=1,
#     min_distance_stars = 1800,
#     max_distance_stars= 1000000000000000000,
#     position_scalar=0.95,
#     timestep = 5,
# )
