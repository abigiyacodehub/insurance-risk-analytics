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
│   ├── 01_eda.md              # Task 1: Exploratory Data Analysis
│   └── 02_dvc_pipeline.md     # Task 2: Data Version Control
├── src/
│   ├── __init__.py
│   ├── data_processing.py     # Data cleaning and preprocessing
│   ├── eda_utils.py           # EDA visualization utilities
│   ├── statistical_tests.py   # Hypothesis testing functions
│   └── data_generator.py      # Synthetic data generation
├── scripts/
│   ├── setup.py               # Project initialization
│   ├── preprocess.py          # Data preprocessing
│   ├── run_eda.py             # EDA execution
│   └── run_hypothesis_tests.py # Hypothesis testing
├── tests/
│   ├── __init__.py
│   └── test_data_processing.py # Unit tests
├── dvc.yaml                    # DVC pipeline configuration
├── config.py                   # Project configuration
├── requirements.txt            # Dependencies
├── Makefile                    # Commands
├── START_HERE.md              # Quick navigation
├── QUICKSTART.md              # 5-minute setup
├── GUIDE.md                   # Complete reference
└── README.md
```

## Task 1: Git Setup + Exploratory Data Analysis (EDA)

### Objectives:
- Initialize git repository with proper structure
- Generate and load insurance dataset (10,000 records)
- Perform statistical EDA with preprocessing
- Create comprehensive visualizations
- Generate EDA summary report

### Key Deliverables:
- Git repository with organized folder structure
- Data preprocessing pipeline (5 stages)
- EDA analysis with statistical summaries
- Visualization outputs (5+ charts)
- Comprehensive documentation

## Task 2: Data Version Control (DVC) Pipeline Setup

### Objectives:
- Initialize DVC for data versioning
- Set up reproducible pipeline stages
- Configure data artifact tracking
- Implement hypothesis testing
- Version control and reproducibility

### Key Deliverables:
- DVC initialized project with 4-stage pipeline
- Data version tracking and caching
- Hypothesis testing integration
- Reproducible pipeline execution
- Complete pipeline documentation

## Quick Start

**3-step setup:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize project
python scripts/setup.py

# 3. Run full pipeline
dvc repro
```

Results go to the `reports/` directory.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Full Pipeline
```bash
dvc repro
# or
make pipeline
```

### Reproduce Data With DVC

This repository uses DVC for both a reproducible pipeline and explicit dataset
version files:

- Pipeline stages are defined in `dvc.yaml` and locked in `dvc.lock`.
- The default local remote is configured in `.dvc/config` as `localstorage`.
- Raw and cleaned dataset snapshots are tracked by:
  - `data/versioned/raw_insurance_data.csv.dvc`
  - `data/versioned/cleaned_insurance_data.csv.dvc`
- Generated CSV data remains ignored by Git through `.gitignore`.

```bash
# Fetch versioned data artifacts from the configured local remote
dvc pull

# Regenerate raw data, cleaned data, EDA reports, and hypothesis reports
dvc repro

# Inspect pipeline state
dvc status

# Optional: push updated data artifacts to the local DVC remote
dvc push
```

Primary pipeline outputs are written to:

- `reports/eda/eda_report.txt`
- `reports/eda/*.png`
- `reports/hypothesis_tests.txt`

### Run Specific Tasks
```bash
# EDA only
python scripts/run_eda.py
# or
make eda

# Hypothesis tests only
python scripts/run_hypothesis_tests.py
# or
make test
```

### Using Makefile
```bash
make setup         # Initialize project
make pipeline      # Run DVC pipeline
make eda          # Run EDA
make test         # Run tests
make clean-all    # Clean outputs
```

## Documentation

- **START_HERE.md** - Quick navigation and overview
- **QUICKSTART.md** - 5-minute setup guide
- **GUIDE.md** - Complete implementation guide
- **IMPLEMENTATION_SUMMARY.md** - Detailed deliverables
- **SUBMISSION_READY.md** - Submission checklist
- **INTERIM_SUBMISSION.md** - Executive summary
- **DELIVERY_MANIFEST.txt** - Full inventory
- **notebooks/01_eda.md** - EDA tutorial
- **notebooks/02_dvc_pipeline.md** - Pipeline guide

## Contributing

Please follow the project structure and coding standards outlined above.

## Status

✅ Task 1 & Task 2 Complete and Ready for Use
