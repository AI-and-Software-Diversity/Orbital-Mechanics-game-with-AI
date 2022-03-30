#!/bin/bash
#SBATCH -D /users/adbg285/HPCWORKSNOW/buildrl
#SBATCH --job-name rlearning_orbit
#SBATCH --partition=gengpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --mem=64MB
#SBATCH --time=24:00:00
#SBATCH -e results/%x_%j.e
#SBATCH -o results/%x_%j.o

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

#Modules required
#This is an example you need to select the modules your code needs.

module load libs/nvidia-cuda/11.2.0/bin

#Run your script.
python3 src/reinforcement_learning.py