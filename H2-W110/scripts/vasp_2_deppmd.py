import os
import glob
import random
import numpy as np
from tqdm import tqdm
from ase.io import read, write
import matplotlib.pyplot as plt
from dpdata import LabeledSystem, MultiSystems

# --------------------------- Configuration ---------------------------
DIR = '../data/all_vasprun'
OUTPUT_DIR = '../data/vasp_2_deepmd'
RESULTS_DIR = '../results/data_train'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
pattern = '*.xml'
energy_range = (-414.5, -412.6)
num_samples = 20000
batch_size = 512
seed_val = 1

# --------------------------- Functions ---------------------------
def get_sorted_files(directory, pattern):
    file_list = glob.glob(os.path.join(directory, pattern))
    return sorted(file_list, key=lambda x: x.lower())

def read_trajectories(files):
    traj = []
    for path in tqdm(files, desc='Reading VASP files'):
        traj.extend(read(path, index=':'))
    return traj

def filter_by_energy(traj, energy_range):
    return [atoms for atoms in traj if energy_range[0] < atoms.get_potential_energy() < energy_range[1]]

def sample_random(traj, num_samples):
    if num_samples > len(traj):
        raise ValueError("Requested more samples than available frames.")
    indices = random.sample(range(len(traj)), num_samples)
    return [traj[i] for i in indices]

def compute_energies(traj):
    return [atoms.get_potential_energy() for atoms in traj]

def save_histogram(all_energies, sampled_energies, filename):
    plt.figure(figsize=(8, 6))
    bins = np.arange(min(all_energies), max(all_energies) + 0.1, 0.1)
    plt.hist(all_energies, bins=bins, alpha=0.6, label='Filtered', edgecolor='black')
    plt.hist(sampled_energies, bins=bins, alpha=0.6, label='Sampled', edgecolor='black')
    plt.xlabel('Potential Energy (eV)')
    plt.ylabel('Count')
    plt.title('Energy Distribution')
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def build_labeled_system(file_path, batch_size):
    traj = read(file_path, index=':')
    sys_dic = {}
    for start in tqdm(range(0, len(traj), batch_size), desc='Batch processing'):
        end = min(start + batch_size, len(traj))
        systems = MultiSystems.from_file(file_path, fmt='ase/structure', ase_fmt='traj', begin=start, end=end)
        sys_dic[f'data{start}'] = systems

    labeled_sys = LabeledSystem()
    for key in tqdm(sys_dic, desc='Merging systems'):
        system = next(iter(sys_dic[key].systems.values()))
        if 'virials' in system.data:
            del system.data['virials']
        labeled_sys.append(system)
    return labeled_sys

def split_and_export_data(system, output_path, seed=1):
    np.random.seed(seed)
    indices = np.arange(len(system))
    np.random.shuffle(indices)
    val_size = int(0.2 * len(system))
    val_idx = indices[:val_size]
    train_idx = indices[val_size:]

    data_training = system.sub_system(train_idx)
    data_validation = system.sub_system(val_idx)

    data_training.to_deepmd_npy(os.path.join(output_path, 'deepmd_data/training_data'))
    data_validation.to_deepmd_npy(os.path.join(output_path, 'deepmd_data/validation_data'))

    np.savetxt(os.path.join(output_path, 'id_validation.dat'), val_idx, fmt='%d')

    print(f'# Training frames: {len(data_training)}')
    print(f'# Validation frames: {len(data_validation)}')

# --------------------------- Main Script ---------------------------
if __name__ == "__main__":
    all_files = get_sorted_files(DIR, pattern)
    traj = read_trajectories(all_files)

    # Save full trajectory
    full_traj_path = os.path.join(OUTPUT_DIR, 'dataset.traj')
    write(full_traj_path, traj)

    # Filter by energy range
    filtered_traj = filter_by_energy(traj, energy_range)
    filtered_energies = compute_energies(filtered_traj)

    # Sample from filtered
    sampled_traj = sample_random(filtered_traj, num_samples)
    sampled_energies = compute_energies(sampled_traj)

    # Save sampled trajectory
    sampled_traj_path = os.path.join(OUTPUT_DIR, 'data_2_train.traj')
    write(sampled_traj_path, sampled_traj)

    # Plot and save histogram
    histogram_path = os.path.join(RESULTS_DIR, 'energies_comparison.png')
    save_histogram(filtered_energies, sampled_energies, histogram_path)

    # Build LabeledSystem and split into training/validation
    labeled_system = build_labeled_system(sampled_traj_path, batch_size)
    split_and_export_data(labeled_system, OUTPUT_DIR, seed=seed_val)

