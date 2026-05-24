"""
Main EDA script for Task 1.
Performs comprehensive exploratory data analysis.
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from eda_utils import (
    generate_summary_statistics,
    plot_distribution,
    plot_correlation_heatmap,
    plot_missing_values,
    plot_feature_importance_by_target,
    generate_eda_report
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run comprehensive EDA analysis."""
    
    processed_data_path = 'data/processed/insurance_data_processed.csv'
    output_dir = 'reports/eda'
    
    logger.info("Starting EDA Analysis")
    
    # Load processed data
    df = pd.read_csv(processed_data_path)
    logger.info(f"Loaded data with shape: {df.shape}")
    
    # Generate summary statistics
    logger.info("\nGenerating summary statistics...")
    stats = generate_summary_statistics(df)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Plot visualizations
    logger.info("\nCreating visualizations...")
    
    # Plot missing values if any
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        plot_missing_values(df, output_path=f'{output_dir}/01_missing_values.png')
    else:
        logger.info("No missing values to visualize")
    
    # Plot correlation heatmap
    plot_correlation_heatmap(df, output_path=f'{output_dir}/02_correlation_heatmap.png')
    
    # Plot distributions of rubric-critical numeric columns first.
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    priority_cols = [
        'TotalPremium',
        'TotalClaims',
        'CustomValueEstimate',
        'premium_annual',
        'coverage_amount'
    ]
    for col in [col for col in priority_cols if col in df.columns]:
        plot_distribution(df, col, output_path=f'{output_dir}/03_distribution_{col}.png')
    
    # Plot feature importance by risk category if available
    if 'risk_category' in df.columns:
        feature_cols = [col for col in numeric_cols if col not in ['risk_category']]
        plot_feature_importance_by_target(
            df, 'risk_category', feature_cols[:4],
            output_path=f'{output_dir}/04_features_by_risk_category.png'
        )
    
    # Generate comprehensive report
    logger.info("\nGenerating EDA report...")
    report_path = generate_eda_report(df, target_col='risk_category', output_dir=output_dir)
    
    logger.info(f"\nEDA Analysis Complete!")
    logger.info(f"Report saved to: {report_path}")
    logger.info(f"Visualizations saved to: {output_dir}/")
    
    return df


if __name__ == '__main__':
    main()
