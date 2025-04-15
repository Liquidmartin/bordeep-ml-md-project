#!/bin/bash

# Entrenamiento en CPU, sin saltar estadísticas de vecinos

export CUDA_VISIBLE_DEVICES="" 

dp train /home/raidelmb/Documentos/2025/ML/ml-md-project/models/training/input.json --skip-neighbor-stat -l /home/raidelmb/Documentos/2025/ML/ml-md-project/models/training/log.log

