from dpdata import LabeledSystem, MultiSystems
from tqdm import tqdm
from ase.io import read, write
import numpy as np
import matplotlib.pyplot as plt
import random

from ase.io.vasp import read_vasp_xml # Methods to run xml files into trajectory object
import glob # For pattern recognition
import os # For directory navigation

DIR = '../data/all_vasprun' # Path to VASP files
pattern = '*.xml' # Name of your POSCAR/CONTCAR files
wd = os.getcwd() # Getting the current working directory for security

full_dir = os.path.join(DIR, pattern) # Building the pattern searcher path
data_files = glob.glob(full_dir) # Parsing all the corresponding files

def sort_dict_by_key(unsorted_dict):
    """Sort a dictionnary by key

    Args:
        unsorted_dict (dict): Unsorted dictionnary

    Returns:
        dict: Sorted dictionnary by keys
    """
    sorted_keys = sorted(unsorted_dict.keys(), key=lambda x:x.lower())
    sorted_dict= {}
    for key in sorted_keys:
        sorted_dict.update({key: unsorted_dict[key]})
    return sorted_dict

def vasp_to_traj(dic):
    """Transform vasp files to traj object

    Args:
        dic (dict): dictionnary containing the file information

    Returns:
        list: trajectory object
    """
    traj = []
    for file in dic.items():
    #    print(file[1])
        atoms = read(filename=file[1], index=':')
        for atom in atoms:
            traj.append(atom)
    return traj

data_dict = {} # Initialization of the dictionnary containing all the information
for i in range(len(data_files)): # Looping over VASP files
    data_dict[data_files[i].split('/')[-1]] = data_files[i] # Dictionnary declaration
    
data_dict = sort_dict_by_key(data_dict) # Sorting the dictionnary

traj = vasp_to_traj(data_dict) # Transforming the VASP files into trajectory object

# Saving the file into a trajectory file
file_path = os.path.join(wd, '../data/vasp_2_deepmd/dataset.traj')
#print(type(traj))
#print(traj)
write(file_path, traj)

potential_energies = [] # Initialization of the potential energy list

for atoms in tqdm(traj):
    potential_energy = atoms.get_potential_energy()
    potential_energies.append(potential_energy)




#Choise the rang of energie, we can put all thes energies if we deside
#======
new_traj = []
for atoms in tqdm(traj):
    potential_energy = atoms.get_potential_energy()
    if -414.5 < potential_energy < -412.6:

        new_traj.append(atoms)


new_potential_energies = [] # Initialization of the potential energy list

for atoms in tqdm(new_traj):
    new_potential_energy = atoms.get_potential_energy()
    new_potential_energies.append(new_potential_energy)

#======


# Número total de configuraciones esta las coge aleatorias en todo el rango de energía
total_configurations = len(new_traj)

# Número de configuraciones a extraer
num_samples = 20000

# Realizar un muestreo aleatorio simple sin reemplazo
random_indices = random.sample(range(total_configurations), num_samples)

# Lista para almacenar las configuraciones seleccionadas
sampled_frames = []

# Extraer las configuraciones seleccionadas
for i in random_indices:
    sampled_frames.append(new_traj[i])

# Ahora, por ejemplo, puedes calcular las distribuciones de ángulos, distancias, y posiciones
# ... como hemos hecho en ejemplos anteriores, o guardarlos para análisis posterior.

sample_potential_energies = [] # Initialization of the potential energy list

for atoms in tqdm(sampled_frames):
    sample_potential_energy = atoms.get_potential_energy()
    sample_potential_energies.append(sample_potential_energy)

write('../data/vasp_2_deepmd/data_2_train.traj', sampled_frames)


# Some plots

# Plotting the information

#plt.style.use('science')
plt.close('all')
fig, (ax1) = plt.subplots(1, 1, figsize=(8,6), sharex='all', sharey='all')


# Potential energies
ax1.set_title('Full dataset')
mini=np.min(new_potential_energies)
maxi=np.max(new_potential_energies)
bin_list = np.arange(mini,maxi, 0.1)
counts, bin_edges, patches = ax1.hist(new_potential_energies, bins=bin_list, density = False)
counts, bin_edges, patches = ax1.hist(sample_potential_energies, bins=bin_list, density = False)



ax1.set_ylabel('Count')
ax1.set_xlabel('Potential energy (eV)')
#ax1.set_ylim(0,1500)

fig.tight_layout()

plt.savefig('../results/data_train/energies_comaprison.png')



# Extracting general information from ASE trajectory file
#No tocarlo si se ejecuto el bloque anterior
file_path = '../data/vasp_2_deepmd/data_2_train.traj'
traj = read(file_path, index = ':')
frame_number = len(traj)
print('The file {0} contains {1} frames.'.format(file_path, frame_number))



batch_size = 512  # Number of geometries to process at a time

sys_dic = {} # Dictionnary for MultiSystems handling

# Function to process a subset of the dataset (ASE trajectory format)
def process_subset(file_path, start_idx, end_idx, fmt='ase/structure'):
    # Assuming file_path is a format that supports slicing or individual loading
    # For actual implementation, this might need to adapt based on how the .traj file is structured
    # and how dpdata or your file handling supports partial loading.
    systems = MultiSystems.from_file(file_path, fmt=fmt, ase_fmt = 'traj', begin=start_idx, end=end_idx)
    # Here you would add your processing logic for the systemsdata-preparatio
    # For example, saving them to a new format, analyzing data, etc.
    return systems

# Batch processing
for start_idx in tqdm(range(0, frame_number, batch_size)):
    end_idx = min(start_idx + batch_size, frame_number)
    processed_systems = process_subset(file_path, start_idx, end_idx)
    sys_dic['data'+str(start_idx)] = processed_systems


My_sys = LabeledSystem() # Declaration of an empty LabeledSystem object
for systems in tqdm(sys_dic.keys()): # Looping over the MultiSystems
    system = next(iter(sys_dic[systems].systems.values())) # Taking the next MultiSystem
    if hasattr(system, 'data') and 'virials' in system.data: # Checking the virials
        print('WARNING: Virial detected. Automatic delete on.')
        del system.data['virials']
    # system = system.data.pop('virials')
    My_sys.append(system) # Adding the MultiSystem to the LabeledSystem object






seed_val = 1 # Value for the random seed

np.random.seed(seed_val) # Applying the random seed

# Defining the validation set configuration indexes
index_validation = np.random.choice(len(My_sys),size=int(len(My_sys)*0.2),replace=False) 

# Write index_validation
INDEX_OUTFILE = '../data/vasp_2_deepmd/id_validation.dat'
outfile = open(INDEX_OUTFILE, 'w')
for i in index_validation:
    outfile.write("{0}\n".format(int(i)))
outfile.close()

# Other indexes are training_data
index_training = list(set(range(len(My_sys)))-set(index_validation)) 

# Shuffle the indexes to incorporate randomness in the batch creation
# This step is optional when working with data from dynamics 
np.random.shuffle(index_training)  

# Building the training and the validation subsystems
data_training = My_sys.sub_system(index_training)
data_validation = My_sys.sub_system(index_validation)

# all training data put into directory:"training_data" 
data_training.to_deepmd_npy('../data/vasp_2_deepmd/deepmd_data/training_data')               
# all validation data put into directory:"validation_data"
data_validation.to_deepmd_npy('../data/vasp_2_deepmd/deepmd_data/validation_data')
   
# Printing section        
print('# the training data contains {} frames'.format(len(data_training))) 
print('# the validation data contains {} frames'.format(len(data_validation)))   
