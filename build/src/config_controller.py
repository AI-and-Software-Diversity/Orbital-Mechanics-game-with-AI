import data_handler

# updates the config file with the correct number of inputs
with open(file="src/config", mode="a") as config_file:
    string = f"num_outputs = {4 * data_handler.GLBVARS.n_planets}"
    config_file.write(string)

print("config updated.")