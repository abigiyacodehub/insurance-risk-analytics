# DVC Workflow Evidence

This project includes a complete DVC setup for Task 2.

## Initialized Repository

DVC metadata is committed under `.dvc/`, including:

- `.dvc/config`
- `.dvc/.gitignore`

## Local Remote

The default remote is configured in `.dvc/config`:

```ini
[core]
    remote = localstorage
[remote "localstorage"]
    url = ../../dvc-remote
```

## Tracked Dataset Versions

The repository commits two explicit DVC tracking files for dataset versions:

- `data/versioned/raw_insurance_data.csv.dvc`
- `data/versioned/cleaned_insurance_data.csv.dvc`

Raw CSV files are not committed to Git. They are ignored by `.gitignore` and can
be restored with:

```bash
dvc pull
```

## Reproducible Pipeline

The pipeline is defined in `dvc.yaml`:

1. `generate_data` creates `data/raw/insurance_data.csv`.
2. `preprocess_data` creates `data/processed/insurance_data_processed.csv`.
3. `eda_analysis` creates `reports/eda/`.
4. `hypothesis_testing` creates `reports/hypothesis_tests.txt`.

Reproduce the workflow:

```bash
dvc repro
dvc status
```

The exact reproduced state is captured in `dvc.lock`.
