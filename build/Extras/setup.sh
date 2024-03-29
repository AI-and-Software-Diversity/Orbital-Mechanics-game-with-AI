#!/bin/bash
#SBATCH -D /users/adbg285/HPCWORKSNOW/build
#SBATCH --job-name my-gputest
#SBATCH --partition=nodes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=36MB
#SBATCH --time=00:10:00
#SBATCH -e results/%x_%j.e
#SBATCH -o results/%x_%j.o

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

#Modules required
#This is an example you need to select the modules your code needs.

module load python/3.7.12
module load libs/nvidia-cuda/11.2.0/bin

#Run your script.
python3 **PLACEHOLDER**
