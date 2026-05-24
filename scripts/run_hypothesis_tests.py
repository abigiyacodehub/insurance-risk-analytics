"""
Hypothesis testing script for Task 3.
Performs statistical tests on insurance data.
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from statistical_tests import (
    compare_premiums_by_smoker,
    compare_risk_by_age_group,
    test_claims_vs_coverage,
    generate_hypothesis_test_report
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run hypothesis testing analysis."""
    
    raw_data_path = 'data/raw/insurance_data.csv'
    output_path = 'outputs/hypothesis_tests.txt'
    
    logger.info("Starting Hypothesis Testing")
    
    # Load raw data
    df = pd.read_csv(raw_data_path)
    logger.info(f"Loaded data with shape: {df.shape}")
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate comprehensive hypothesis testing report
    logger.info("\nPerforming statistical tests...")
    report_path = generate_hypothesis_test_report(df, output_path=output_path)
    
    logger.info(f"\nHypothesis Testing Complete!")
    logger.info(f"Report saved to: {report_path}")
    
    return df


if __name__ == '__main__':
    main()
