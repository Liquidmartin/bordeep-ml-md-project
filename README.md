# 🧠 ML-MD Project: Training Potentials with DeepMD-kit

This project provides tools for processing, filtering, and transforming data from VASP to train neural networks using **DeepMD-kit**. It also includes an energy conservation analysis for trajectories and tools to prepare the training dataset.

---

## 📂 Project Structure

```
.
├── data/                       # Raw and processed data (.xml, .traj)
│   ├── all_oszicar/           # OSZICAR files from VASP
│   ├── all_vasprun/           # vasprun.xml files from VASP
│   └── vasp_2_deepmd/         # Data ready for DeepMD training
├── results/                   # Histograms and summary of analysis
├── scripts/
│   ├── analisis_oscicar.py    # Filters trajectories with poor energy conservation
│   ├── vasp_2_deppmd.py       # Converts and filters data for DeepMD-kit
│   └── to_train_NN.sh         # Shell script to launch training
├── environment.yml            # Conda environment for preprocessing
├── environment2.yml           # Conda environment for DeepMD training
└── README.md                  # This file
```

---

## 🔧 Environments

- `environment.yml`: used for data processing and preparation.
- `environment2.yml`: used to compile and train the model with DeepMD.

Both include essential dependencies: `deepmd-kit`, `dpdata`, `ASE`, `TensorFlow`, etc.

---

## ⚙️ Main Scripts

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

---

## 🚀 How to Use This Repository

1. **Create base environment**:
   ```bash
   conda env create -f environment.yml
   conda activate ml-md-env
   ```

2. **Analyze energy conservation**:
   ```bash
   python scripts/analisis_oscicar.py
   ```

3. **Preprocess data for DeepMD**:
   ```bash
   python scripts/vasp_2_deppmd.py
   ```

4. **Train the neural network**:
   - Switch to training environment if needed:
     ```bash
     conda deactivate
     conda env create -f environment2.yml
     conda activate ml-md-env2
     ```
   - Launch training:
     ```bash
     bash scripts/to_train_NN.sh
     ```

---

## 🧬 Requirements

- Python 3.9
- ASE
- DeepMD-kit
- dpdata
- TensorFlow 2.9.x
- matplotlib
- Conda

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