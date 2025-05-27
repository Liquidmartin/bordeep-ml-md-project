import os
import shutil
import csv

def check_and_move_bad_files(base_path, oszicar_dir="all_oszicar", vasprun_dir="all_vasprun",
                              num_files=400, energy_threshold=0.1):
    oszicar_path = os.path.join(base_path, oszicar_dir)
    vasprun_path = os.path.join(base_path, vasprun_dir)
    bad_oszicar_path = os.path.join(oszicar_path, 'bad_traj')
    bad_vasprun_path = os.path.join(vasprun_path, 'bad_traj')

    os.makedirs(bad_oszicar_path, exist_ok=True)
    os.makedirs(bad_vasprun_path, exist_ok=True)

    bad_files_info = []

    for i in range(1, num_files + 1):
        file_name = f"OSZICAR_{i}"
        file_path = os.path.join(oszicar_path, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            initial_E = None
            E_values = []
            time_steps = []

            for line in lines:
                if 'E=' in line:
                    parts = line.split()
                    try:
                        E = float(parts[parts.index('E=') + 1])
                        time = len(E_values)
                        E_values.append(E)
                        time_steps.append(time)
                        if initial_E is None:
                            initial_E = E
                    except (ValueError, IndexError):
                        continue

            if initial_E is not None:
                for idx, E in enumerate(E_values):
                    difference = abs(E - initial_E)
                    if difference > energy_threshold:
                        # Mover OSZICAR
                        shutil.move(file_path, os.path.join(bad_oszicar_path, file_name))
                        # Buscar y mover el vasprun correspondiente
                        vasprun_filename = f"vasprun_{i}.xml"
                        vasprun_file_path = os.path.join(vasprun_path, vasprun_filename)
                        if os.path.exists(vasprun_file_path):
                            shutil.move(vasprun_file_path, os.path.join(bad_vasprun_path, vasprun_filename))
                        else:
                            print(f"⚠️  vasprun correspondiente no encontrado: {vasprun_filename}")
                        bad_files_info.append({
                            'index': i,
                            'oszicar': file_name,
                            'vasprun': vasprun_filename,
                            'initial_E': initial_E,
                            'difference': difference,
                            'time_step': time_steps[idx],
                            'E_value_at_deviation': E
                        })
                        break
    return bad_files_info



# Al final del script, después de la línea: return bad_files_info
# Escribe esto para guardar el resumen en CSV

def guardar_csv(resumen, output_path="../data/bad_traj_summary.csv"):
    if not resumen:
        print("No se identificaron archivos problemáticos.")
        return
    with open(output_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=resumen[0].keys())
        writer.writeheader()
        writer.writerows(resumen)
    print(f"✅ Resumen guardado en: {output_path}")

# Uso
base_path = "../data"
bad_files = check_and_move_bad_files(base_path)

print("\nArchivos movidos por variación excesiva de energía:")
for entry in bad_files:
    print(f"[{entry['index']}] OSZICAR: {entry['oszicar']}, VASP: {entry['vasprun']}, ΔE: {entry['difference']:.4f} eV")
    guardar_csv(bad_files)


