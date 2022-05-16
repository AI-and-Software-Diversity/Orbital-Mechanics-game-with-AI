#!/bin/bash
#SBATCH -D /users/adbg285/HPCWORKSNOW/buildneat
#SBATCH --job-name neat_orbit
#SBATCH --partition=nodes
#SBATCH --nodes=6
#SBATCH --ntasks-per-node=48
#SBATCH --mem=0
#SBATCH --time=16:00:00
#SBATCH -e results/%x_%j.e
#SBATCH -o results/%x_%j.o

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

#Modules required
#This is an example you need to select the modules your code needs.

module load libs/nvidia-cuda/11.2.0/bin

#Run your script.
python3 src/neuro_evolution.py