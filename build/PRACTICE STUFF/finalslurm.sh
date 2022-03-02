#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=4
#SBATCH --job-name=testing_hpc                 # Job name
#SBATCH --mail-type=END,FAIL                 # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=javonne.porter@city.ac.uk         # Where to send mail
#SBATCH --exclusive                          # Exclusive use of nodes
#SBATCH --ntasks-per-node=48                 # Use all the cores on each node
#SBATCH --mem=0                              # Expected memory usage (0 means use all available memory)
#SBATCH --output=myfluent_test_%j.out        # Standard output and error log [%j is replaced with the jobid]
#SBATCH --error=myfluent_test_%j.error

srun python3 src/sbtest.py --threads=4 5
