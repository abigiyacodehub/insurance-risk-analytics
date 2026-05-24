# Quick Start Guide

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abigiyacodehub/insurance-risk-analytics.git
   cd insurance-risk-analytics
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize DVC**:
   ```bash
   dvc init
   ```

## Running the Project

### Option 1: Run Individual Scripts

```bash
# Step 1: Setup and generate data
python scripts/setup.py

# Step 2: Preprocess data
python scripts/preprocess.py

# Step 3: Run EDA
python scripts/run_eda.py

# Step 4: Run hypothesis tests
python scripts/run_hypothesis_tests.py
```

### Option 2: Run DVC Pipeline (Recommended)

```bash
# Run entire pipeline
dvc repro

# View pipeline DAG
dvc dag

# Check pipeline status
dvc status
```

### Option 3: Run Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open notebooks in browser and run cells
```

## Output Files

After execution, you'll find:

- **Data**:
  - `data/raw/insurance_data.csv`: Original dataset
  - `data/processed/insurance_data_processed.csv`: Cleaned data

- **Analysis Results**:
  - `outputs/eda/eda_report.txt`: Summary statistics
  - `outputs/eda/*.png`: Visualization plots
  - `outputs/hypothesis_tests.txt`: Statistical test results

- **Pipeline Files**:
  - `dvc.lock`: Pipeline execution record
  - `.dvc` files: DVC metadata

## Project Structure

```
insurance-risk-analytics/
├── data/
│   ├── raw/                    # Original data
│   └── processed/              # Preprocessed data
├── outputs/
│   ├── eda/                    # EDA results
│   └── hypothesis_tests.txt    # Statistical test results
├── src/
│   ├── data_generator.py       # Generate sample data
│   ├── data_processing.py      # Data cleaning utilities
│   ├── eda_utils.py           # EDA visualization functions
│   └── statistical_tests.py    # Hypothesis testing functions
├── scripts/
│   ├── setup.py               # Project initialization
│   ├── preprocess.py          # Data preprocessing
│   ├── run_eda.py             # EDA execution
│   └── run_hypothesis_tests.py # Hypothesis testing
├── notebooks/
│   ├── 01_eda.md              # EDA documentation
│   └── 02_dvc_pipeline.md     # DVC pipeline guide
├── dvc.yaml                    # DVC pipeline config
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```

## Common Tasks

### Run Specific Pipeline Stage

```bash
dvc repro preprocess_data  # Run only preprocessing
dvc repro eda_analysis     # Run only EDA
```

### Add New Dependencies

```bash
pip install package_name
pip freeze > requirements.txt
```

### Update DVC Remote Storage

```bash
# Configure S3 storage
dvc remote add myremote s3://bucket-name/path

# Set as default
dvc remote default myremote

# Push data
dvc push
```

### View Pipeline Metrics

```bash
dvc plots show
dvc exp show  # If using experiments
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Deactivate and remove venv
deactivate
rm -rf venv

# Recreate from scratch
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### DVC Pipeline Errors

```bash
# Clear cache and retry
dvc cache remove --all
dvc repro --force

# Check logs
dvc status
dvc dag
```

### Missing Data Files

```bash
# Generate sample data
python scripts/setup.py

# Or pull from remote
dvc pull
```

## Next Steps

1. Review `notebooks/01_eda.md` for detailed EDA walkthrough
2. Review `notebooks/02_dvc_pipeline.md` for pipeline details
3. Explore output files in `outputs/` directory
4. Proceed to Task 3: Statistical Modeling (if available)

## Support

For issues or questions:
1. Check the README.md
2. Review notebook documentation
3. Check DVC logs: `dvc status`
4. Open a GitHub issue in the repository

---

**Last Updated**: 2026-05-24
