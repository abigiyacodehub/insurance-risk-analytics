"""
Master setup and initialization script.
Sets up the entire project structure and generates initial data.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_generator import save_sample_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_project():
    """Initialize project structure and generate sample data."""
    
    logger.info("=" * 80)
    logger.info("INSURANCE RISK ANALYTICS - PROJECT SETUP")
    logger.info("=" * 80)
    
    # Create necessary directories
    directories = [
        'data/raw',
        'data/processed',
        'outputs/eda',
        'notebooks',
        'scripts'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Generate sample data
    logger.info("\nGenerating sample insurance data...")
    df = save_sample_data('data/raw/insurance_data.csv')
    
    logger.info(f"\nProject setup complete!")
    logger.info(f"Sample data: {df.shape}")
    logger.info("\nNext steps:")
    logger.info("1. Run preprocessing: python scripts/preprocess.py")
    logger.info("2. Run EDA: python scripts/run_eda.py")
    logger.info("3. Run hypothesis tests: python scripts/run_hypothesis_tests.py")
    logger.info("4. Or run entire pipeline: dvc repro")
    
    return df


if __name__ == '__main__':
    setup_project()
