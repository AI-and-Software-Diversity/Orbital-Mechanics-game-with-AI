## readme (Orbital Diversity)

The purpose of this document is to explain how the codebase works at a deeper level. Note that the codebase has comments, this document is just a supplement to those as plain English is easier to understand than code comments. (TARGET AUDIENCE: Anyone working on the codebase)

## agents_and_data

This folder contains information about trained agents and their performance on the task. This is 
to help with organisation and make it easier to find key information when writing. 

## assets

This folder contains the assets important for the game. The only ones in use are the font files 
and the background files.

## data

The first layer of depth is a specific algorithm. For example NEAT or Reinforcement Learning. 
The contents of these folders (and any other that is added) are identical.

Firstly, `CSVs`. This folder contains 3 CSV files. They are `data_neat.csv`, `pred_neat.csv`, and `setup_neat.csv`. For a moment think of the Agents as if they are functions. Respectively, they take information about the game as input, use this input to predict an output, and get certain results from the predicted output. Now in context:

- `setup_neat.csv` - This contains the input. EG the positions of all of the planets and 
  their mass. 
- `pred_neat.csv` - This contains the output of the function. Namely, the position and 
  momentum of each planet.
- `data_neat.csv` - This contains the results that follow from the output and other generic 
  relevant information. EG the number of timesteps the agent lives for and, whether or not 
  the run was a success.

For each file, you can see the rest of the features tracked using the top CSV row.

There is also a folder called models. This is where all model checkpoints go. And if Tensorboard is being used for a reinforcement learning `model` (which is unnecessary if you use the data files + helper methods), models will be the log directory.

## Extras

There are 3 key files in this folder

- `HPC Instructions` - This folder contains instructions and commands that are useful for 
  the HPC node that City has. This node is vital, without it, models will likely take too long 
  to train.
- `setupNEAT.sh` - This is the bash file for training a NEAT agent.
- `setupRL.sh` - This is the bash file for training a Reinforcement learning agent.

The two bash files can be customised heavily.

## PRACTICE STUFF

This folder is only used for practice code. It may not be relevant at all to you.

## src

This is the most important folder. It contains the bulk of what was worked on throughout this 
project.

### bodies.py 

This contains the classes for the two bodies in the game. The star can be initialised and drawn 
in place. 

The planets can be initialised, drawn, moved, and finally destroyed. The movement follows the 
Euler-Cromer method. Editing the variable `dt` can change how the planets are affected by 
gravity. When a planet is destroyed, several of its parameters are changed. They result in the 
body being moved offscreen and it will not impact the game at all.

### config

This is the class that controls how NEAT agents learn. Briefly, the most important factors are 

- the number of inputs - Proportional to the number of stars
- The number of outputs - Proportional to the number of planets
- pop_size - The number of NEAT agents that will train simultaneously. Higher > Slower training
- fitness_criterion - Can be mean, max, or min.
- fitness_threshold - once the {fitness_criterion} reward in the population reaches this threshold training will 
- end and a winning agent (Genome) will be selected. EG if the fitness_criterion is max, once the maximum 
- fitness of any agent in the population reaches the fitness threshold, training will stop.
- The rest of the options can be read about in-depth here  

### config_controller.py

This will automatically calculate how many outputs are needed in the config file, and update the 
config file. A common error would be running this file too many times and having duplicate rows 
in the `config` file. Be sure to put the line it generates in the correct position. 

### helpers.py

This file contains functions that can be understood by looking at the comments and the function 
names. However, there are a few important notes:

```python
def get_rlearn_graph(data, timesteps):
```

This function can be used to plot good graphs of any information in the data CSVs. This function 
is why Tensorboard is useless. You populate it using an array that comes from (`def` 
`get_collumn_from_csv(file, chosen_col):` and the timesteps parameter is equal to the 
first value of `total_timesteps` you will see in the results output file. 

### randoms.py

This function is just for testing. It may be removed in the final version.

### game.py

Initially, the plan was to have the game be fully playable by human agents, which is what this file 
was for, but it is no longer beneficial to keep updated. Furthermore, the purpose of this project 
does not require a human playable version of the game, so this version of the game is not fully 
updated. It may be useful to have a human playable version in order to check for bugs.

### The environments

There are 2 files with Env in the name. These are the environments, or in context, they are 
where the actual gameplay functionality is stored in a way that AI agents can interact with them. 
If you know python you can get any information that you can think of from within this file. This is 
just a brief explanation to make the next file make more sense.

### data_handler.py

1. The `Collector` class.

   This class is how data is collected from the env classes. Using the add to CSV files, data 
   you put a python list of variables into the function, and after every run, whatever 
   information you specify in the list, will be written to a CSV.

2. The `DataGenerator` class.

   This class is like a settings file for the project. It has several parameters that control how 
   a run works. The instance of this class is named `GLBVARS`. Changing this single instance 
   can control the number of planets and stars, the size of the window, the min/max 
   distance between stars and more. Having the settings centralised like this means that 
   you have to do less work to change variables when you want to change the settings an 
   agent trains with.

### OrbitEnv.py

This is the location of the actual game. This file is quite long, but I will break it down slowly. 

This is the interface of a gym environment (used for custom envs):

```python
import gym
from gym import spaces

class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, arg1, arg2, ...):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(N_CHANNELS, HEIGHT, WIDTH), 
dtype=np.uint8)

    def step(self, action):
        ...
        return observation, reward, done, info
    def reset(self):
        ...
        return observation  # reward, done, info can't be included
    def render(self, mode='human'):
        ...
    def close (self):
        ...
```

This environment is the key to using both of the ML algorithms I will be using.

#### Constructor

In the constructor, there is an action space and an observation space. 

- The action space is responsible for the actions that the model takes. In our case, the 
  position and momentum of all planets. It is in the form of a list of floats that range from -1 
  to 1, but you can multiply this by a constant if you need a wider range (eg if we multiply 
  action[0] by 4, the effective range will be -4 to 4) 
- The observation space is the information that a model can observe. Including things like 
  the number of stars that exist. And the positions of each star.

Each method will vary depending on the settings of the run.

The action space list will be 

#planets x [Planet x position, Planet y position, Planet x momentum, Planet y momentum]

The observation space will be

#stars x [star x position], #stars x [star y position], #stars x [star mass], #planets x [planet mass], 
height, width

#### Reset method

The reset method is what runs before the core game loop. Think of this as the initialisation of 
the game. I initialise some variables at the start, and then I handle setting up the star positions. 
The role of the first while loop is to determine if the stars can be placed (The star's initial 
positions are restricted by the edge limits and the min/max distance between stars. These are 
set in the `data_handler.py` file). The next loop actually places these stars. After that, you 
return the observation (as a single array) which was described in the constructor section.  

#### Step method

The step method contains the core game loop. It obtains the action space from the code written 
in the constructor. This action is a python list, and the numbers in this list are what the AI uses 
to interact with our environment. The step method is run after the reset. During training, the AI 
will constantly be running both `reset` and then `step` cyclically.

The step method begins with the initialisation of variables, and then we enter the first loop. Most 
of the code in this loop is gameplay related (Within commented sub-loops and if-statements). 
The comments in the codebase explain what each sub-loop/if-statement does so that won't be 
discussed here. The other big part of this is handling rewards. 

The reward is the number that your AI wants to maximise. Ideally, you want a model’s reward to 
be high when it performs well, and low when it doesn't perform well, but there is no objective 
way to implement this. The reward is an actual python variable. You have to be able to use 
reasoning to decide when to add to a score, and when to subtract from it. 

The reward function in this environment works as follows:

1. Reward starts at 0.
2. When a planet dies (Collides with another body or goes offscreen), reward is penalised.
3. If a planet dies too soon, reward is reduced more harshly, this accelerates the time it takes for the AI to stop throwing planets off-screen immediately.
4. For every fixed number of timesteps, the reward is incremented. If more planets are alive, the value of the incrementation is higher, this is to encourage the model to keep as many planets active as possible at any given time.
5. If the agent manages to complete the objective (Enough active timesteps) the score is boosted substantially. We want success to be heavily incentivised.
6. If multiple planets are alive when the objective is completed, the final reward boost is multiplied.
7. If all planets die before the objective is completed, the reward is decremented. 

At the end of the step method, we return the updated observation, the reward, and a boolean 
variable `done` that specifies if the run is done. This information is going to be used by our agents 
in order to learn.

### OrbitEnvNoGFX.py

This is a clone of the OrbitEnv.py but altered in a way such that it doesn't require any graphics 
to be displayed. This is because when we train on the HPC node, There is no device to output 
graphics to. Furthermore, without loading graphics, the gameplay is no longer limited in terms of 
speed. A single successful run in the environment with graphics takes roughly 50s. But in this 
environment, it will take <1s. This massively speeds up training. 

Both environments may take one parameter, `mode`. This parameter is to control where we save 
model checkpoints and data files. 

It can be useful to train on your local machine and env with graphics. This can help you verify 
everything is working as expected. This use case is one of the main things that made the 
human playable version of the game obsolete.

#### render method

Instead of having two files for one environment, one could have put all of the code for graphics 
in the render file. This is ideal, but difficult to implement and it is not how the project is currently 
set up. The use of this render method would make things more clean and modular.

#### close method 

It is also possible to implement a close method. When training on a local machine this will result 
in the close button on the PyGame window working as expected. I chose not to implement this 
initially as I didn't want to accidentally cancel training. Currently, it isn't implemented because 
the stop button on IntelliJ is functional.



### neuro_evolution.py

This file is where we train AI agents to “solve” our environment using the NEAT algorithm. It is a 
lightweight algorithm that trains quite fast but is more likely to get subpar results.

 This file has 2 important functions. `def eval_genome(genome, config):`  is where the training 
loop takes place. If `runs_per_net` is 3, An agent will attempt the game 3 times, and the mean 
reward (or fitness in this case. Fitness = Reward) will be the reward this agent has. Increasing 
this number makes your averages more accurate but it will take longer. You may also choose to 
take the maximum, minimum or any combination of the 3 runs by altering the code.

In `def run():` training will loop following this pattern. You can alter the number of cores used to 
run and you can also choose to get preset information in this function. For example, The stdout 
is what displays the average population fitness in the output window.

When you change the number of stars and try to train without changing the config you may get 
an error that looks like `RuntimeError: Expected 10 inputs, got 9`. To fix this, simply 
change `num_inputs` in the `config` file from 10 to 9.  

### do_neat_runs.py

This is the file used to run a trained neat agent. To use this all you have to do is change the file 
path to the model you want to see

### do_reinforcement_learning_runs.py

This file is where we train AI agents to “solve” our environment using reinforcement learning. It 
is a slow but powerful algorithm. If RL agents struggle to perform, there is a good chance the 
reward function of the Env needs to be tuned.

The first important part of this file is a list of boolean variables that determine what takes place. 
`use_saved_model, train_new_model, see_sample_run` Are the variables. They do exactly 
what they say when set to true or false. If `train_new_model` is true we go into a training loop. 
This loop will save a checkpoint after a fixed number of steps, and go on forever, but in reality, it 
is usually interrupted by the 3 day GPU time limit on the HPC node. When this happens you 
keep `train_new_model` true. From here you use `model.load()` and use the file path of the 
checkpoint and the environment as parameters. This will allow you to continue training where 
you left off. The code can be seen in the `reinforcement_learning.py` file as a comment. 
Once you have a trained model, ensure `use_saved_model` and `see_sample_run` are true and 
update the file path to your model, and you will be able to see/get data on as many runs as you 
specify from the model of choice. 

### do_optimal_agent_runs.py

WIP

### do_optimal_agent_neat_runs.py

WIP

### do_optimal_agent_rl_runs.py

WIP

**NOTE** 

For the previous 3 files, changing the order of the imports of the Environments will 
determine which version of the env you use
