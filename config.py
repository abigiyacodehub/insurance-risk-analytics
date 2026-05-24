"""
Configuration file for project paths and settings.
"""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.resolve()

# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Source code directory
SRC_DIR = PROJECT_ROOT / 'src'

# Scripts directory
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'

# Notebooks directory
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'

# Outputs directory
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'
EDA_OUTPUT_DIR = OUTPUTS_DIR / 'eda'

# Tests directory
TESTS_DIR = PROJECT_ROOT / 'tests'

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUTS_DIR, EDA_OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuration parameters
CONFIG = {
    'data_generation': {
        'n_samples': 10000,
        'random_seed': 42,
    },
    'preprocessing': {
        'missing_value_strategy': 'mean',
        'outlier_method': 'iqr',
        'normalize': True,
    },
    'eda': {
        'figure_dpi': 300,
        'figure_size': (12, 6),
    },
    'statistical_tests': {
        'alpha': 0.05,
        'test_type': 'two-sided',
    }
}

# File paths
FILE_PATHS = {
    'raw_data': RAW_DATA_DIR / 'insurance_data.csv',
    'processed_data': PROCESSED_DATA_DIR / 'insurance_data_processed.csv',
    'eda_report': EDA_OUTPUT_DIR / 'eda_report.txt',
    'hypothesis_report': OUTPUTS_DIR / 'hypothesis_tests.txt',
}
