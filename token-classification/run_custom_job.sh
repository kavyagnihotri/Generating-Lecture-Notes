#!/bin/bash
##NECESSARY JOB SPECIFICATIONS
##SBATCH -p gpu_v100_2
#SBATCH -p gpu_a100_8
#SBATCH --job-name=token-classification-image-location
#SBATCH -t 12:00:00              #Set the wall clock limit to 3hr and 30min
#SBATCH -N 1                    #Number of Nodes
#SBATCH --gres=gpu:1          #Request 1 task
#SBATCH -o token-classification-image-location.%j.out      #Send stdout/err to "Example4Out.[jobID]"
#SBATCH -e token-classification-image-location.%j.err

BASE_DIR="$(pwd)"
python3 run_ner.py \
  --model_name_or_path bert-base-uncased \
  --train_file "${BASE_DIR}/../data/image-location/test.json" \
  --validation_file "${BASE_DIR}/../data/image-location/validation.json" \
  --test_file "${BASE_DIR}/../data/image-location/test.json" \
  --output_dir "${BASE_DIR}/../models/image-location" \
  --do_train \
  --do_eval \
  --do_predict
