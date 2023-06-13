import random
import data_handler

def generate_config(fitness_criterion, fitness_threshold, pop_size, reset_on_extinction, num_inputs, num_outputs):
    config = f"""
[NEAT]
fitness_criterion     = {fitness_criterion}
fitness_threshold     = {fitness_threshold}
pop_size              = {pop_size}
reset_on_extinction   = {reset_on_extinction}

[DefaultGenome]
num_inputs              = {num_inputs}
num_hidden              = {random.randint(0, 5)}
num_outputs             = {num_outputs}
initial_connection      = partial_direct {random.uniform(0, 1)}
feed_forward            = {random.choice([True, False])}
compatibility_disjoint_coefficient    = {random.uniform(0, 1)}
compatibility_weight_coefficient      = {random.uniform(0, 1)}
conn_add_prob           = {random.uniform(0, 0.6)}
conn_delete_prob        = {random.uniform(0, 0.6)}
node_add_prob           = {random.uniform(0, 0.6)}
node_delete_prob        = {random.uniform(0, 0.6)}
activation_default      = tanh
activation_options      = tanh
activation_mutate_rate  = {random.uniform(0, 1)}
aggregation_default     = sum
aggregation_options     = sum
aggregation_mutate_rate = {random.uniform(0, 1)}
bias_init_mean          = {random.uniform(0, 0.3)}
bias_init_stdev         = {random.uniform(0, 0.1)}
bias_replace_rate       = {random.uniform(0, 1)}
bias_mutate_rate        = {random.uniform(0, 1)}
bias_mutate_power       = {random.uniform(0, 1)}
bias_max_value          = {random.uniform(0, 1)}
bias_min_value          = {random.uniform(-1, 0)}
response_init_mean      = {random.uniform(0, 1)}
response_init_stdev     = {random.uniform(0, 1)}
response_replace_rate   = {random.uniform(0, 1)}
response_mutate_rate    = {random.uniform(0, 1)}
response_mutate_power   = {random.uniform(0, 1)}
response_max_value      = {random.uniform(0, 1)}
response_min_value      = {random.uniform(-1, 0)}

weight_max_value        = {random.uniform(0, 1)}
weight_min_value        = {random.uniform(-1, 0)}
weight_init_mean        = {random.uniform(-1, 1)}
weight_init_stdev       = {random.uniform(0, 1)}
weight_mutate_rate      = {random.uniform(0, 1)}
weight_replace_rate     = {random.uniform(0, 1)}
weight_mutate_power     = {random.uniform(0, 1)}
enabled_default         = {random.choice([True, False])}
enabled_mutate_rate     = {random.uniform(0, 1)}

[DefaultSpeciesSet]
compatibility_threshold = {random.uniform(2.4, 4)}

[DefaultStagnation]
species_fitness_func = mean
max_stagnation  = {random.randint(10, 100)}

[DefaultReproduction]
elitism            = {random.randint(50, 100)}
survival_threshold = {random.uniform(0, 0.2)}
"""
    return config


print(generate_config(
    fitness_criterion="mean",
    fitness_threshold=100,
    pop_size=300,
    reset_on_extinction="False",
    num_inputs=6,
    num_outputs=4 * data_handler.GLBVARS.n_planets
))