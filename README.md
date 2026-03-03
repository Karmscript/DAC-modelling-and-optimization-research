<a href="https://doi.org/10.5281/zenodo.18851858"><img src="https://zenodo.org/badge/1171801551.svg" alt="DOI"></a>
---

# README: Machine-Learning Accelerated Direct Air Capture (DAC) Optimization

### Mechanistic Modelling, Surrogate Modeling & Multi-Objective Optimization of DAC using Eggshell-Derived Calcium Hydroxide

## 📌 Project Overview

This repository contains a computational framework designed to optimize $CO_2$ capture using waste-derived eggshell ($Ca(OH)_2$) sorbent. The project integrates first-principles chemical engineering models with gradient-boosted machine learning and evolutionary algorithms to find the optimal trade-offs between capture efficiency and energy consumption.

**The Workflow:**

1. **Latin Hypercube Sampling:** For creating space-filling variables.
2. **Process Simulation:** Aspen Plus flowsheet
3. **Kinetics Modelling:** MATLAB Shrinking Core Model 
4. **Surrogate Modelling:** XGBoost regression trained on the results from kinetics and process modelling.
5. **Global Optimization:** NSGA-II to identify the Pareto Front of optimal operations.

---

## 📁 Repository Structure

```bash
.
├── Folder PATH listing
├── Volume serial number is 34B8-A336
├── C:.
├── |   DAC_project_structure.txt
├── |   README.md
├── |   
├── +---DAC_optimization
├── |       DAC_optimal_inputs_from_NSGAII.csv
├── |       DAC_optimization_workflow.ipynb
├── |       pareto_points.csv
├── |       
├── +---Heterogeneous_co-simulation
├── |   |   DAC_helpers.py
├── |   |   DAC_optimal_simulation_results_testing.csv
├── |   |   DAC_simulation_results.csv
├── |   |   Heterogeneous_co_simulator.ipynb
├── |   |   LHS_variables_to_be_manipulated_by_python.csv
├── |   |   
├── |   +---Aspen_plus_simulation_files
├── |   |       DAC_simulation_V2.apw
├── |   |       DAC_simulation_V2.bkp
├── |   |       
├── |   \---MATLAB_simulation_file
├── |           DAC_func.m
├── |           
├── +---LatinHyperCube_Sampler
├── |       DAC_LHS_sampler.ipynb
├── |       LHS_variables_to_be_manipulated_by_python.csv
├── |       
├── +---Results_Analysis
├── |   |   DAC_Analysis_results.ipynb
├── |   |   
├── |   \---Results
├── |           Capture-efficiency-vs-column-height-DAC.JPG
├── |           Capture-efficiency-vs-pellet-size-DAC.JPG
├── |           Capture_efficiency-vs_Humidity_DAC.JPG
├── |           Efficiency-predicted-vs-actual_DAC.JPG
├── |           Feature-importance-Efficiency.JPG
├── |           Feature-importance-SECC.JPG
├── |           Pareto-front_DAC.JPG
├── |           SECC-predicted-vs-actual_DAC.JPG
├── |           SECC-vs-height_DAC.JPG
├── |           SECC-vs-humidity_DAC.JPG
├── |           SECC-vs-pellet-size_DAC.JPG
├── |           
└── \---Surrogate_modelling/
    ├── DAC_efficiency_XGBmodel.json
    ├── DAC_ML_workflow.ipynb
    ├── DAC_SECC_XGBmodel.json
    └── wrangled_DAC_simulation_results.csv

---

## 🛠 Installation & Requirements

### Software Prerequisites:

* **Aspen Plus, with valid license key** (V14.0 or higher)
* **MATLAB with valid license key** (R2024a or higher)
* **Python 3.11** (important to prevent dependency issues with MATLAB engine and python COM)

### Python Dependencies:

```bash
pip install xgboost scikit-learn pandas matplotlib scipy pymoo

```

---

## 🚀 Execution Guide

### Step 1: Data Generation 
Run the co-simulation to generate the training data. This script opens Aspen Plus in the background and iterates through the LHS design space.

* **Property Methods:** PR-BM (Reactors), IDEAL (Mixers).
* **Inputs:** Moisture, Porosity, Air Velocity, Temperature, etc.

### Step 2: Surrogate Training

The XGBoost model approximates the heterogeneous operator

* **Metrics:** $R^2 > 0.95$ for Energy and Capture Efficiency.

### Step 3: Optimization

Run the **DAC_optimization_workflow.ipynb** script to find the non-dominated sorting of designs.

* **Objectives:** $\min(SECC)$ and $\max(\eta_{capture_efficiency})$.
* **Output:** `Pareto-front_DAC.JPG` showing the trade-off curve.

---

## 📊 Key Results


* **Optimization:** Identified a "Knee Point" capable of at least 65% $CO_2$ capture effficiency an energy penalty cost lower than $10dollars/kg-captured CO_2$.
* **Verification:** Optimal points were rerun through the Aspen "Oracle" to filter out non-physical points
---

## 📝 Citation & Contact

If you use this framework for DAC research or any codes contained, please cite:

>...check for paper link later....

**Contact:** [ahmedramadanbamidele@gmail.com]

---

### LICENSE
**MIT License**, but referencing and citation of paper required in the event of any usage of the codes.