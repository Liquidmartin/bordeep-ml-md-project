import os
from ase.io import read, write
#Este codigo convierte POSCARS existentes en archivos .lammps  con lasmisas condiciones de los POSCRAS

# Directorio donde se encuentran los archivos POSCAR
poscar_dir = '/home/raidelmb/Documentos/2024/ML/DeepMD/h-w110-300meV-alberto/dinamica/LAMMPS/all_poscar'

# Directorio donde se guardarán los archivos de datos para LAMMPS
output_dir = '/home/raidelmb/Documentos/2024/ML/DeepMD/h-w110-300meV-alberto/dinamica/LAMMPS/data_lammps_h2_w110'

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Obtener una lista de todos los archivos POSCAR en el directorio
poscar_files = [f for f in os.listdir(poscar_dir) if f.startswith('POSCAR')]

# Iterar sobre todos los archivos POSCAR y convertirlos a archivos de datos LAMMPS
for poscar_file in poscar_files:
    # Leer el archivo POSCAR
    poscar_path = os.path.join(poscar_dir, poscar_file)
    atoms = read(poscar_path)
    
    # Generar el nombre de archivo de salida
    output_file = os.path.join(output_dir, f"data_{poscar_file}.lammps")
    
    # Escribir el archivo de datos en formato LAMMPS
    write(output_file, atoms, format='lammps-data', masses={1: 1.00784, 2: 183.84}, 
          atom_style='atomic', units='real')

    print(f"Archivo {poscar_file} convertido a {output_file}")

