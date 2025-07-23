# 🧠 ML-MD Project: Training Potentials with DeepMD-kit

This project provides tools for processing, filtering, and transforming data from VASP to train neural networks using **DeepMD-kit**. It also includes an energy conservation analysis for trajectories and tools to prepare the training dataset.

---

## 📂 Project Structure

```
.	
├──H2-W(110)
│  ├── data/                      # Raw and processed data (.xml, .traj)
│  │   ├── all_oszicar/           # OSZICAR files from VASP
│  │   ├── all_vasprun/           # vasprun.xml files from VASP
│  │   └── vasp_2_deepmd/         # Data ready for DeepMD training
│  ├── results/                   # Histograms and summary of analysis
│  ├── dinamica/                  # Dynamic of the system using LAMMPS
│  │   ├── data_dft/              # DFT reference input files (eg. POSCAR)
│  │   ├── data_in/               # LAMMPS input files created
│  │   ├── salida_prueba/         # Example of simulation output
│  │   ├── env_lammps.yml         # Conda environment for use LAMMPS
│  │   ├── vasp_2_lammps.py       # Input files VASP-to-LAMMPS structure converter
│  │   ├── in.simulation          # Main LAMMPS input file
│  │   └── lansamiento.sh         # Script to run the simulation 
│  └── scripts/
│      ├── install_deepmd.sh      # Prepare work environment ready to use DeepMD-kit
│      ├── analisis_oscicar.py    # Filters trajectories with poor energy conservation
│      ├── vasp_2_deppmd.py       # Converts and filters data for DeepMD-kit
│      └── to_train_NN.sh         # Shell script to launch training
├── environment.yml               # Conda environment for preprocessing
├── README.md                     # This file
└── H/O-W(110)                    # Raul's study system
```

---

## 🔧 Environment

- `environment.yml`: used for data processing and preparation.
- H2-W(110)/dinamica/env_lammps.yml`: dedicated environment for LAMMPS simulations.

Include essential dependencies: `ASE`, `TensorFlow`, etc.

---

## ⚙️ Main Scripts

### 🔹 `install_deepmd.sh`
- Creates the required environment with ASE, TensorFlow, and other dependencies.
- Installs DeepMD-kit compiled from source to ensure compatibility with this environment.

### 🔹 `analisis_oscicar.py`
- Checks if energy conservation is satisfied in each trajectory.
- Moves failing files to `bad_traj/`.
- Generates a `.csv` summary of bad trajectories.

### 🔹 `vasp_2_deppmd.py`
- Reads `vasprun.xml` files.
- Filters structures by potential energy.
- Saves and plots energy histograms.
- Builds `.npy` training/validation datasets using `dpdata`.

### 🔹 `to_train_NN.sh`
- Executes DeepMD training using `dp train`.

### 🔹 `data_comparison.py`
- Loads all atomic configurations.
- Excludes previously used ones for training and validation.
- Saves new ones for comparison ( data_comparison.traj ).

### 🔹 `plot_comparison.py`
- Loads structures from a .traj file.
- Computes energies and forces using a trained DeepMD model.
- Compares predicted vs DFT values with error metrics (MAE, RMSE, R²).
- Plots energy and force correlations and error distributions.

### 🔹 `dinamica/vasp_2_lammps.py`
- Converts a DFT POSCAR structure into a LAMMPS-compatible input file.  
- This is used to generate the initial atomic configuration for the MD simulation.


### 🔹 `dinamica/lansamiento.sh`
- Launches an MD simulation in LAMMPS using the trained PES.

---

## 🚀 How to Use This Repository

0. **Enter the system folder**:
   cd  H2-W(110)/
   
1. **Create base environment**:
   ./scripts/install_deepmd.sh
   conda activate ml-md-env

2. **Analyze energy conservation**:
   python scripts/analisis_oscicar.py

3. **Preprocess data for DeepMD**:
   python scripts/vasp_2_deppmd.py

4. **Train the neural network**:
   - Launch training:
     ./scripts/to_train_NN.sh

5. **Preprocess data for comparison between DFT and NN**:
   python scripts/data_comparison.py

6. **Compare DFT and DeepMD predictions**:
   python scripts/plot_comparison.py
     
7. **Create the LAMMPS environment**:
   conda env create -f /dinamica/env_lammps.yml
   conda activate lammps_env

8. **Generate the initial conditions**:
   python dinamica/vasp_2_lammps.py


9. **Run the simulation**:
   ./dinamica/lanzamiento.sh

10. **Check results**:
   dinamica/salida_prueba/

Note: Always review and adjust:

input.json → defines neural network training parameters.

in.simulation → defines simulation conditions (timestep, thermostat, number of steps) for LAMMPS.   

---

## 🧬 Requirements

- Python 3.9
- ASE
- DeepMD-kit
- dpdata
- TensorFlow 2.9.x
- matplotlib
- Conda
- LAMMPS

---

## 🧑‍💻 Author

**Raidel Martin-Barrios**  
📧 rmartin9301@gmail.com  
🔗 [GitHub: Liquidmartin](https://github.com/Liquidmartin)

---

## 📄 License

Pascal Larregaray Group  
Institut de Science Moléculaire (ISM), Université de Bordeaux

---

## 📄 Acknowledgments 


We gratefully acknowledge the University of Bordeaux, the Institut des Sciences Moléculaires (ISM), and the CURTA platform for their support and computational resources. This work was funded by the DALTON-ANR project. Special thanks to the Maurice MONNERVILLE group at the University of Lille for their training and support in laying the foundations for machine learning potential training.

---

