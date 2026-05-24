"""
Main preprocessing script for Task 1 and 2.
Handles data preprocessing and preparation for analysis.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_processing import preprocess_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run data preprocessing pipeline."""
    
    raw_data_path = 'data/raw/insurance_data.csv'
    processed_data_path = 'data/processed/insurance_data_processed.csv'
    
    # Define numeric columns to check for outliers
    outlier_columns = [
        'TotalPremium',
        'TotalClaims',
        'CustomValueEstimate',
        'premium_annual',
        'coverage_amount',
        'risk_score'
    ]
    
    # Run preprocessing
    df_processed = preprocess_data(
        raw_data_path=raw_data_path,
        processed_data_path=processed_data_path,
        missing_value_strategy='mean',
        outlier_method='iqr',
        outlier_columns=outlier_columns
    )
    
    logger.info(f"Preprocessing complete. Output shape: {df_processed.shape}")
    logger.info(f"Columns: {df_processed.columns.tolist()}")
    
    return df_processed


if __name__ == '__main__':
    main()
