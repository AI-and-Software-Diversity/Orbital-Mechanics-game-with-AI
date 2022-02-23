#!/bin/bash
SBATCH -D /users/adbg285/hpc/Orbital-Mechanics-game-with-AI/build/PRACTICE STUFF/src    # Working directory
SBATCH --job-name my-gputest                      # Job name
SBATCH --partition=gengpu                         # Select the correct partition.
SBATCH --nodes=1                                  # Run on 1 nodes (each node has 48 cores)
SBATCH --ntasks-per-node=8                        # Use 8 cores, most of the procesing happens on the GPU
SBATCH --mem=24MB                                 # Expected ammount CPU RAM needed (Not GPU Memory)
SBATCH --time=00:10:00                            # Expected ammount of time to run Time limit hrs:min:sec
SBATCH --gres=gpu:1                               # Use one gpu.
SBATCH -e results/%x_%j.e                         # Standard output and error log [%j is replaced with the jobid]
SBATCH -o results/%x_%j.o
