#!/bin/bash
##NECESSARY JOB SPECIFICATIONS
##SBATCH -p gpu_v100_2
#SBATCH -p gpu_a100_8
#SBATCH --job-name=tc-formula
#SBATCH -t 12:00:00              
#SBATCH -N 1                    
#SBATCH --gres=gpu:1         
#SBATCH -o tc-formula.%j.out      
#SBATCH -e tc-formula.%j.err

##cmd