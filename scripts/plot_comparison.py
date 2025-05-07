import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
from deepmd.calculator import DP
from tqdm import tqdm
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


data = np.genfromtxt("../models/trainin_example_gaudi/lcurve.out", names=True)
for name in data.dtype.names[1:-1]:
    plt.plot(data["step"], data[name], label=name)
plt.legend()
plt.xlabel("Step")
plt.ylabel("Loss")
#plt.xscale("symlog")
plt.yscale("log")
plt.grid()
plt.title("Training Loss Curve, e=300 meV, Rc=6 A")  
plt.savefig("../results/plot_comparison/loss_curve.png")



# Load trajectory
TRAJ_FILE = '../data/vasp_2_deepmd/data_comparison.traj'
traj = read(TRAJ_FILE, index=':')

# Load DeepMD model
dp_calculator = DP(model='../models/trainin_example_gaudi/graph.pb')

# Lists to store energy comparison
z_values = []
d_values = []
energy_dft = []
energy_deepmd = []

# Compute energies from DFT and DeepMD
for atoms in tqdm(traj, desc='Processing frames'):
    positions = atoms.get_positions()
    z1 = positions[0, 2]
    d = np.linalg.norm(positions[1] - positions[0])

    z_values.append(z1)
    d_values.append(d)

    energy_dft.append(atoms.get_potential_energy())

    atoms_copy = atoms.copy()
    atoms_copy.calc = dp_calculator
    energy_deepmd.append(atoms_copy.get_potential_energy())

# Convert to arrays
energy_dft = np.array(energy_dft)
energy_deepmd = np.array(energy_deepmd)

# Compute energy metrics
mae = mean_absolute_error(energy_dft, energy_deepmd)
mse = mean_squared_error(energy_dft, energy_deepmd)
rmse = np.sqrt(mse)
r2 = r2_score(energy_dft, energy_deepmd)

print(f"Energy MAE: {mae:.4f} eV")
print(f"Energy MSE: {mse:.4f} eV^2")
print(f"Energy RMSE: {rmse:.4f} eV")
print(f"Energy R²: {r2:.4f}")

# Plot energy comparison
plt.figure(figsize=(8, 6))
plt.scatter(energy_dft, energy_deepmd, alpha=0.7, label='DeepMD vs DFT')
plt.plot([min(energy_dft), max(energy_dft)], [min(energy_dft), max(energy_dft)], 'r--', label='y = x')

text_str = (f"MAE: {mae:.4f} eV\n"
            f"MSE: {mse:.4f} eV²\n"
            f"RMSE: {rmse:.4f} eV\n"
            f"R²: {r2:.4f}")
plt.text(0.05, 0.95, text_str, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='left',
         bbox=dict(facecolor='white', alpha=0.6))

plt.xlabel('DFT Energy (eV)')
plt.ylabel('DeepMD Energy (eV)')
plt.title('DFT vs DeepMD Energy Comparison')
plt.legend(loc="lower right")
plt.grid(True)
plt.savefig("../results/plot_comparison/energies_comparison.png", dpi=300, bbox_inches="tight")

# Plot energy error histogram
errors = energy_deepmd - energy_dft
plt.figure(figsize=(8, 6))
n, bins, _ = plt.hist(errors, bins=30, color='blue', alpha=0.7, density=True)
bin_width = np.diff(bins)
n_percentage = n * bin_width * 100
plt.clf()
plt.bar(bins[:-1], n_percentage, width=bin_width, color='blue', alpha=0.7, align='edge')
plt.xlabel('Error (eV)')
plt.ylabel('Percentage (%)')
plt.title('Energy Error Distribution: DFT vs DeepMD')
plt.grid(True)
plt.savefig("../results/plot_comparison/error_energy_distribution.png", dpi=300, bbox_inches="tight")

# Compute DFT and DeepMD forces
forces_dft = np.array([atoms.get_forces() for atoms in traj])

# Force DeepMD to recompute forces (avoid cached ones from .traj)
forces_deepmd = []
for atoms in traj:
    atoms_copy = atoms.copy()
    atoms_copy.calc = dp_calculator
    if 'forces' in atoms_copy.arrays:
        del atoms_copy.arrays['forces']  # force recalculation
    forces_deepmd.append(atoms_copy.get_forces())
forces_deepmd = np.array(forces_deepmd)

# Flatten for metrics
forces_dft_flat = forces_dft.flatten()
forces_deepmd_flat = forces_deepmd.flatten()

# Compute force metrics
mae = mean_absolute_error(forces_dft_flat, forces_deepmd_flat)
mse = mean_squared_error(forces_dft_flat, forces_deepmd_flat)
rmse = np.sqrt(mse)
r2 = r2_score(forces_dft_flat, forces_deepmd_flat)

print(f"Force MAE: {mae:.4f} eV/Å")
print(f"Force MSE: {mse:.4f} (eV/Å)^2")
print(f"Force RMSE: {rmse:.4f} eV/Å")
print(f"Force R²: {r2:.4f}")

# Plot force comparison
plt.figure(figsize=(8, 6))
plt.scatter(forces_dft_flat, forces_deepmd_flat, alpha=0.7, label='DeepMD vs DFT')
plt.plot([min(forces_dft_flat), max(forces_dft_flat)], [min(forces_dft_flat), max(forces_dft_flat)], 'r--', label='y = x')

text_str = (f"MAE: {mae:.4f} eV/Å\n"
            f"MSE: {mse:.4f} (eV/Å)²\n"
            f"RMSE: {rmse:.4f} eV/Å\n"
            f"R²: {r2:.4f}")
plt.text(0.05, 0.95, text_str, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='left',
         bbox=dict(facecolor='white', alpha=0.6))

plt.xlabel('DFT Forces (eV/Å)')
plt.ylabel('DeepMD Forces (eV/Å)')
plt.title('DFT vs DeepMD Force Comparison')
plt.legend(loc="lower right")
plt.grid(True)
plt.savefig("../results/plot_comparison/force_comparison.png", dpi=300, bbox_inches="tight")

# Plot force error histogram
errors = forces_deepmd_flat - forces_dft_flat
plt.figure(figsize=(8, 6))
plt.hist(errors, bins=30, color='blue', alpha=0.7, density=True)
plt.xlabel('Error (eV/Å)')
plt.ylabel('Density')
plt.title('Force Error Distribution: DFT vs DeepMD')
plt.grid(True)
plt.savefig("../results/plot_comparison/error_force_distribution.png", dpi=300, bbox_inches="tight")

