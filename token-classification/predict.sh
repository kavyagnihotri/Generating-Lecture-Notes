#!/bin/bash

BASE_DIR="$(pwd)"

MODEL_DIR="${BASE_DIR}/../models/image-location"  
OUTPUT_DIR="${BASE_DIR}/../output/image-location"      
TEST_FILE="${BASE_DIR}/../data/image-location/test.json"  
VAL_FILE="${BASE_DIR}/../data/image-location/validation.json"
TRAIN_FILE="${BASE_DIR}/../data/image-location/train.json"

# Run the NER prediction script
python3 run_ner.py \
  --model_name_or_path $MODEL_DIR \
  --train_file $TRAIN_FILE \
  --validation_file $VAL_FILE \
  --output_dir $OUTPUT_DIR \
  --do_predict \
  --test_file $TEST_FILE
