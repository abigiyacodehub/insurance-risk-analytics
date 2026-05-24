# Task 2: Data Version Control (DVC) Pipeline

## Overview

This document describes the Data Version Control (DVC) pipeline setup for the insurance risk analytics project. DVC enables reproducible workflows, data versioning, and efficient collaboration.

## DVC Pipeline Architecture

The pipeline consists of four stages:

```
generate_data
    ↓
preprocess_data
    ↓
eda_analysis
    ↓
hypothesis_testing
```

### Stage 1: Generate Data

**Purpose**: Create or load the raw insurance dataset

**Command**: `python src/data_generator.py`

**Outputs**:
- `data/raw/insurance_data.csv`: Raw insurance data with 10,000 records

**Characteristics**:
- Generates synthetic data based on realistic insurance patterns
- Includes age, premium, coverage, claims, and risk factors
- Reproducible with fixed random seed

### Stage 2: Preprocess Data

**Purpose**: Clean, transform, and prepare data for analysis

**Command**: `python scripts/preprocess.py`

**Inputs**:
- `data/raw/insurance_data.csv`

**Outputs**:
- `data/processed/insurance_data_processed.csv`: Cleaned and preprocessed data

**Processing Steps**:
1. Handle missing values (mean imputation)
2. Remove outliers (IQR method)
3. Encode categorical variables
4. Normalize numeric features

### Stage 3: EDA Analysis

**Purpose**: Perform comprehensive exploratory data analysis

**Command**: `python scripts/run_eda.py`

**Inputs**:
- `data/processed/insurance_data_processed.csv`

**Outputs**:
- `outputs/eda/eda_report.txt`: Summary statistics and insights
- `outputs/eda/*.png`: Visualization files

**Analyses**:
- Distribution plots for numeric features
- Correlation matrix heatmap
- Missing value visualization
- Feature relationships with target variable

### Stage 4: Hypothesis Testing

**Purpose**: Perform statistical tests to validate hypotheses

**Command**: `python scripts/run_hypothesis_tests.py`

**Inputs**:
- `data/raw/insurance_data.csv`

**Outputs**:
- `outputs/hypothesis_tests.txt`: Statistical test results

**Tests Performed**:
- T-test: Premiums by smoker status
- ANOVA: Risk scores across age groups
- Pearson correlation: Coverage vs claims

## Pipeline Configuration

The pipeline is defined in `dvc.yaml`:

```yaml
stages:
  generate_data:
    cmd: python src/data_generator.py
    deps:
      - src/data_generator.py
    outs:
      - data/raw/insurance_data.csv:
          cache: true

  preprocess_data:
    cmd: python scripts/preprocess.py
    deps:
      - data/raw/insurance_data.csv
      - src/data_processing.py
    outs:
      - data/processed/insurance_data_processed.csv:
          cache: true

  eda_analysis:
    cmd: python scripts/run_eda.py
    deps:
      - data/processed/insurance_data_processed.csv
      - src/eda_utils.py
    outs:
      - outputs/eda/eda_report.txt
      - outputs/eda/:
          cache: false

  hypothesis_testing:
    cmd: python scripts/run_hypothesis_tests.py
    deps:
      - data/raw/insurance_data.csv
      - src/statistical_tests.py
    outs:
      - outputs/hypothesis_tests.txt
```

## Usage

### Initialize DVC

```bash
# Initialize DVC in the repository
dvc init

# Configure remote storage (optional)
dvc remote add myremote /path/to/storage
dvc remote default myremote
```

### Run Pipeline

```bash
# Run entire pipeline
dvc repro

# Run specific stage
dvc repro preprocess_data

# Force rerun all stages
dvc repro --force
```

### Version Control

```bash
# Add outputs to DVC tracking
dvc add data/raw/insurance_data.csv

# Commit DVC files to Git
git add .gitignore dvc.yaml dvc.lock
git commit -m "Add DVC pipeline"

# Push data to remote
dvc push

# Pull data from remote
dvc pull
```

## Key Features

### 1. Reproducibility

- Each stage has explicit dependencies and outputs
- Automatic cache management prevents redundant execution
- Deterministic results with fixed random seeds

### 2. Data Versioning

- Track data changes across experiments
- Version data artifacts without storing in Git
- Compare outputs across different runs

### 3. Dependency Tracking

- Automatically tracks which files depend on which
- Detects when inputs change and reruns dependent stages
- Creates DAG (directed acyclic graph) of pipeline

### 4. Cache Management

- Efficient storage with content-based hashing
- Only reprocess changed data
- Local and remote cache support

## Working with Experiments

### Track Experiments

```bash
# Run experiment with modifications
dvc exp run -n exp1

# Compare experiments
dvc exp show

# Save best experiment
dvc exp push myremote -r exp1
```

### Modify Pipeline

Edit `dvc.yaml` to add or modify stages:

```yaml
new_stage:
  cmd: python scripts/new_script.py
  deps:
    - input_file.csv
  outs:
    - output_file.csv
```

Then run:
```bash
dvc repro new_stage
```

## Best Practices

1. **Semantic Versioning**: Tag releases with git tags
2. **Documentation**: Document pipeline stages in comments
3. **Modular Design**: Keep stages focused on single tasks
4. **Testing**: Validate outputs of each stage
5. **Performance**: Monitor execution time and optimize slow stages
6. **Collaboration**: Use remote storage for team sharing

## Troubleshooting

### Pipeline not running

```bash
# Check DVC status
dvc status

# Validate pipeline
dvc dag

# Clean cache and rerun
dvc repro --force
```

### Data not syncing

```bash
# Check remote configuration
dvc remote list

# Push specific file
dvc push data/raw/insurance_data.csv.dvc

# Pull updates
dvc pull
```

## Next Steps

1. Deploy pipeline to CI/CD system (GitHub Actions, GitLab CI)
2. Set up remote storage (S3, Azure Blob, etc.)
3. Integrate with model registry for versioning
4. Automate pipeline triggers on data updates
5. Add data quality checks to pipeline stages

## References

- DVC Documentation: https://dvc.org/doc
- Pipeline Best Practices: https://dvc.org/doc/start/data-pipelines
- Remote Storage Setup: https://dvc.org/doc/user-guide/setup-and-teardown
