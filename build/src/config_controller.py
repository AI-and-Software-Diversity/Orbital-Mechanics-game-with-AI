import data_handler

with open(file="src/config", mode="a") as config_file:
    string = f"num_outputs = {4 * data_handler.GLBVARS.n_planets}"
    config_file.write(string)

print("config updated.")