#!/bin/bash

# Load Conda into this shell
source ~/anaconda3/etc/profile.d/conda.sh

echo "Creating environment ml-md-env3..."
cd ..
conda env create -f environment.yml

# Activate the conda environment (adjust name if needed)
echo "Activating environment ml-md-env3..."
conda activate ml-md-env || { echo "Failed to activate the environment"; exit 1; }


# Ensure system compiler is used instead of Anaconda's internal one
#echo "Switching to system compiler..."
#export PATH=/usr/bin:$PATH

# Install DeepMD-kit from source
echo "Installing DeepMD-kit from source..."
pip install --no-binary deepmd-kit deepmd-kit

echo "Installing dpdata from source..."
pip install dpdata

echo "✅ DeepMD-kit installation completed successfully."
