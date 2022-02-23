#!/bin/bash
SBATCH -D /users/adbg285/hpc/Orbital-Mechanics-game-with-AI/build/PRACTICE STUFF/src  # Working directory
SBATCH --job-name=my_fluent                 # Job name
SBATCH --mail-type=END,FAIL                 # Mail events (NONE, BEGIN, END, FAIL, ALL)
SBATCH --mail-user=email@city.ac.uk         # Where to send mail
SBATCH --exclusive                          # Exclusive use of nodes
SBATCH --nodes=2                            # Run on 2 nodes (each node has 48 cores)
SBATCH --ntasks-per-node=48                 # Use all the cores on each node
SBATCH --mem=0                              # Expected memory usage (0 means use all available memory)
SBATCH --time=00:30:00                      # Time limit hrs:min:sec
SBATCH --output=myfluent_test_%j.out        # Standard output and error log [%j is replaced with the jobid]
SBATCH --error=myfluent_test_%j.error

# enable modules
source /opt/flight/etc/setup.sh
flight env activate gridware

# remove any unwanted modules
module purge

# Modules required
module load fluent

srun hostname  | sort > hosts.$SLURM_JOB_ID

# Command line to run task
fluent 3ddp -g -t$SLURM_NTASKS -mpi=intel -ssh -cnf=hosts.$SLURM_JOB_ID -i example_1_fluent_input.txt