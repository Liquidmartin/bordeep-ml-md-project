import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
from ase import Atoms
from deepmd.calculator import DP
from tqdm import tqdm

# Definir la ruta al archivo .traj
TRAJ_FILE = '../data/vasp_2_deepmd/data_comparison.traj'

# Leer las configuraciones desde el archivo .traj
traj = read(TRAJ_FILE, index=':')

# Definir el calculador DeepMD
dp_calculator = DP(model='../models/trainin_example_gaudi/graph.pb')


# Preparar listas para almacenar los resultados
z_values = []
d_values = []
energy_dft = []
energy_deepmd = []

# Extraer datos y calcular energías
for atoms in tqdm(traj):
    positions = atoms.get_positions()
    
    # Supongamos que los átomos de hidrógeno son los primeros dos átomos en 'positions'
    # y el átomo de tungsteno está en la última posición (esto puede ajustarse según tu sistema).
    z1 = positions[0, 2]  # Coordenada Z del primer átomo de hidrógeno
    z2 = positions[1, 2]  # Coordenada Z del segundo átomo de hidrógeno
    d = np.linalg.norm(positions[1] - positions[0])  # Distancia interatómica H-H

    z_values.append(z1)  # Podrías querer usar z2 en lugar de z1, dependiendo de lo que te interese
    d_values.append(d)
    
    # Energía DFT del archivo .traj
    energy_dft.append(atoms.get_potential_energy())
    
    # Calcular la energía usando DeepMD
    atoms.set_calculator(dp_calculator)
    energy_deepmd.append(atoms.get_potential_energy())

# Convertir listas a arrays
z_values = np.array(z_values)
d_values = np.array(d_values)
energy_dft = np.array(energy_dft)
energy_deepmd = np.array(energy_deepmd)

# Suponiendo que ya tienes los siguientes arrays:
# z_values, d_values, energy_dft, energy_deepmd

# Calcular métricas de error
mae = mean_absolute_error(energy_dft, energy_deepmd)
mse = mean_squared_error(energy_dft, energy_deepmd)
rmse = np.sqrt(mse)
r2 = r2_score(energy_dft, energy_deepmd)

# Imprimir valores en consola
print(f"Error absoluto medio (MAE): {mae:.4f} eV")
print(f"Error cuadrático medio (MSE): {mse:.4f} eV^2")
print(f"Raíz del error cuadrático medio (RMSE): {rmse:.4f} eV")
print(f"Coeficiente de determinación (R²): {r2:.4f}")

# Gráfico de comparación entre energías DFT y DeepMD
plt.figure(figsize=(8, 6))
plt.scatter(energy_dft, energy_deepmd, alpha=0.7, label='DeepMD vs DFT')
plt.plot([min(energy_dft), max(energy_dft)], [min(energy_dft), max(energy_dft)], 'r--', label='y=x')

# Agregar las métricas de error dentro de la figura en la parte superior izquierda
text_str = (f"MAE: {mae:.4f} eV\n"
            f"MSE: {mse:.4f} eV²\n"
            f"RMSE: {rmse:.4f} eV\n"
            f"R²: {r2:.4f}")

# Ajustar la posición del texto (un poco más a la izquierda y arriba)
plt.text(0.05, 0.95, text_str,
         transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='left',
         bbox=dict(facecolor='white', alpha=0.6))

# Etiquetas y configuración de la gráfica
plt.xlabel('Energía DFT (eV)')
plt.ylabel('Energía DeepMD (eV)')
plt.title('Comparación de Energías DFT y DeepMD, e=300 meV, Rc=6 A')

# Colocar la leyenda en la parte inferior derecha
plt.legend(loc="lower right")

plt.grid(True)

# Guardar la figura
plt.savefig("../results/plot_comparison/energies_comparison.png", dpi=300, bbox_inches="tight")

# Gráfico de los errores (diferencias)
errors = energy_deepmd - energy_dft
plt.figure(figsize=(8, 6))
# Crear el histograma con normalización (density=True)
n, bins, patches = plt.hist(errors, bins=30, color='blue', alpha=0.7, density=True)

# Multiplicar por el ancho de los bins y por 100 para obtener porcentajes en el área
bin_width = np.diff(bins)
n_percentage = n * bin_width * 100

# Limpiar la figura y graficar el histograma con porcentajes
plt.clf()  # Limpiar la figura
plt.bar(bins[:-1], n_percentage, width=bin_width, color='blue', alpha=0.7, align='edge')

# Etiquetas y título
plt.xlabel('Error (eV)')
plt.ylabel('Porcentaje (%)')
plt.title('Distribución de Errores entre Energías DFT y DeepMD, e=300 meV, Rc=6 A')
plt.grid(True)
plt.savefig("../results/plot_comparison/error_energy_distribution.png", dpi=300, bbox_inches="tight")

