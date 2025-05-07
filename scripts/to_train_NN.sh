#!/bin/bash

# Entrenamiento en CPU, sin saltar estadísticas de vecinos

export CUDA_VISIBLE_DEVICES="" 
cd ../models/training/
dp train input.json --skip-neighbor-stat -l log.log

dp freeze -c checkpoint_dir/ -o graph.pb

