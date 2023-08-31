#!/bin/bash
##NECESSARY JOB SPECIFICATIONS
#SBATCH -p gpu_v100_2
##SBATCH -p gpu_a100_8
#SBATCH --job-name=pseudocode-scraping
#SBATCH -t 12:00:00              #Set the wall clock limit
#SBATCH -N 1                    #Number of Nodes
#SBATCH --gres=gpu:1          #Request 1 task
#SBATCH -o pseudocode-scraping.%j.out      #Send stdout/err to "Example4Out.[jobID]"
#SBATCH -e pseudocode-scraping.%j.err

python3 scripts/dataset_for_token-class.py