# 🧠 Machine Learning for Molecular Dynamics (ML-MD)

Este proyecto contiene las herramientas necesarias para entrenar modelos de Machine Learning aplicados a la dinámica molecular, especialmente usando **DeepMD-kit**, **ASE** y **LAMMPS**.

Fue desarrollado en el marco de un postdoctorado en el grupo de investigación en Burdeos, con el objetivo de facilitar la integración de métodos de ML en simulaciones de dinámica molecular.

---

## 📂 Estructura del proyecto

```
ml-md-project/
├── data/           # Configuraciones atómicas (POSCAR, .traj, etc.)
├── scripts/        # Scripts de entrenamiento, preprocesamiento y análisis
├── models/         # Modelos entrenados (frozen_model.pb, checkpoints)
├── results/        # Gráficos y métricas
├── notebooks/      # Notebooks explicativos y ejemplos paso a paso
├── environment.yml # Entorno conda con dependencias
└── README.md       # Este documento
```

---

## 🚀 Cómo comenzar

### 1. Clonar el repositorio (cuando esté en GitHub)
```bash
git clone https://github.com/tu-usuario/ml-md-project.git
cd ml-md-project
```

### 2. Crear y activar el entorno
```bash
conda env create -f environment.yml
conda activate ml-md-env
```

### 3. Ejecutar un ejemplo mínimo
```bash
python scripts/hello_ml.py
```

### 4. Ejecutar una simulación con LAMMPS y el modelo entrenado

Este proyecto asume que tienes instalado LAMMPS como ejecutable (`lmp`). No se utiliza `lammps-cython` para evitar problemas de compilación.

```bash
lmp -in input.lammps
```

El archivo `input.lammps` debe estar configurado para usar el modelo de DeepMD (`frozen_model.pb`) como potencial.

---

## 📦 Dependencias principales

Estas son las librerías clave utilizadas en este proyecto:

| Librería        | Uso principal |
|-----------------|----------------|
| **ASE**         | Manipulación de estructuras atómicas y trayectorias |
| **DeepMD-kit**  | Entrenamiento de redes neuronales para energías y fuerzas |
| **dpdata**      | Preparación de conjuntos de datos para DeepMD-kit |
| **NumPy**       | Cálculos numéricos |
| **matplotlib**  | Visualización de datos |

---

## 🔍 Flujo de trabajo general

1. **Conversión de datos**: POSCAR o .traj → formato DeepMD
2. **Entrenamiento**: usar `dp train` con configuraciones y etiquetas
3. **Validación**: comparar energías y fuerzas con DFT
4. **Simulación**: correr LAMMPS con el modelo `.pb`
5. **Análisis**: generación de gráficos y métricas

---

## ⚠️ Sobre LAMMPS y Python (`lammps-cython`)

No se incluye el paquete `lammps-cython` en este entorno debido a errores frecuentes durante su compilación. Para la mayoría de los usos, especialmente en simulaciones de dinámica molecular, basta con usar LAMMPS como ejecutable externo (`lmp`).

Si en el futuro se requiere controlar LAMMPS directamente desde Python, se recomienda seguir la [guía oficial de instalación del wrapper Python de LAMMPS](https://docs.lammps.org/Python_install.html).

---

## 📬 Contacto

Para dudas o colaboración:

**Raidel Martín-Barrios**  
📧 raidelmartinbarrios@gmail.com
