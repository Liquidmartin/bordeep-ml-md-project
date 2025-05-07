import numpy as np
from ase.io import read, write
import matplotlib.pyplot as plt
import ase.io
import random
from tqdm import tqdm  # Make sure you have tqdm installed

# Load the main .traj file
filename = '../data/vasp_2_deepmd/dataset.traj'
frames = ase.io.Trajectory(filename)

# Load the configurations to exclude
exclude_filename = '../data/vasp_2_deepmd/data_2_train.traj'
excluded_frames = ase.io.Trajectory(exclude_filename)

# Total number of configurations
total_configurations = len(frames)

# Create a set of configurations to exclude based on atomic positions and composition
def configuration_hash(atoms):
    """Creates a hash based on atomic positions and composition."""
    positions = tuple(atoms.positions.round(8).flatten())
    numbers = tuple(atoms.numbers)
    return hash((positions, numbers))

excluded_hashes = set(configuration_hash(atoms) for atoms in excluded_frames)

# Number of configurations to extract
num_samples = 2000

# List to store selected configurations
sampled_frames = []

# Perform simple random sampling without replacement and exclude specific configurations
random_indices = random.sample(range(total_configurations), total_configurations)  # Shuffle all configurations
for i in tqdm(random_indices):
    if len(sampled_frames) >= num_samples:
        break  # Stop if desired number of samples is reached

    # Take the current configuration
    atoms = frames[i]
    
    # Check if it's not among the excluded configurations
    if configuration_hash(atoms) not in excluded_hashes:
        sampled_frames.append(atoms)

# Optional: save selected configurations
output_filename = '../data/vasp_2_deepmd/data_prediction.traj'
ase.io.write(output_filename, sampled_frames)

# Print final statistics
print(f"Total number of configurations in original dataset: {total_configurations}")
print(f"Number of excluded configurations: {len(excluded_frames)}")
print(f"Number of selected configurations: {len(sampled_frames)}")

