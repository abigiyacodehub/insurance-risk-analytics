# Insurance Risk Analytics

This project implements end-to-end insurance risk analytics and predictive modeling using Data Version Control (DVC) and statistical modeling.

## Project Structure

```
insurance-risk-analytics/
├── data/
│   ├── raw/                    # Original, immutable data
│   ├── processed/              # Cleaned and preprocessed data
│   └── .gitignore
├── notebooks/
│   ├── 01_eda.ipynb           # Task 1: Exploratory Data Analysis
│   └── 02_hypothesis_testing.ipynb
├── src/
│   ├── __init__.py
│   ├── data_processing.py     # Data cleaning and preprocessing
│   ├── eda_utils.py           # EDA visualization utilities
│   ├── statistical_tests.py   # Hypothesis testing functions
│   └── modeling.py            # Predictive modeling
├── dvc.yaml                    # DVC pipeline configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Task 1: Git Setup + Exploratory Data Analysis (EDA)

### Objectives:
- Initialize git repository with proper structure
- Load and explore insurance dataset
- Perform statistical EDA
- Create comprehensive visualizations
- Generate EDA summary report

### Key Deliverables:
- Git repository with organized folder structure
- Jupyter notebook with EDA analysis
- Visualization outputs
- Data summary statistics

## Task 2: Data Version Control (DVC) Pipeline Setup

### Objectives:
- Initialize DVC for data versioning
- Set up data pipeline stages
- Configure reproducible workflows
- Version control data artifacts

### Key Deliverables:
- DVC initialized project
- dvc.yaml with pipeline configuration
- Data version tracking
- Reproducible pipeline execution

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Task 1: Run EDA
```bash
jupyter notebook notebooks/01_eda.ipynb
```

### Task 2: Run DVC Pipeline
```bash
dvc repro
```

## Contributing

Please follow the project structure and coding standards outlined above.
