"""
EDA utilities for exploratory data analysis and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def generate_summary_statistics(df: pd.DataFrame) -> dict:
    """
    Generate comprehensive summary statistics.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    logger.info("Generating summary statistics")
    
    stats = {
        'shape': df.shape,
        'dtypes': df.dtypes.value_counts(),
        'missing_values': df.isnull().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'numeric_summary': df.describe(),
        'correlation_matrix': df.select_dtypes(include=[np.number]).corr()
    }
    
    return stats


def add_loss_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Add LossRatio for portfolio risk analysis."""
    df_ratio = df.copy()
    if {'TotalClaims', 'TotalPremium'}.issubset(df_ratio.columns):
        df_ratio['LossRatio'] = df_ratio['TotalClaims'] / df_ratio['TotalPremium'].replace(0, np.nan)
    return df_ratio


def plot_distribution(df: pd.DataFrame, column: str, output_path: str = None):
    """
    Plot distribution of a single column.
    
    Args:
        df: Input DataFrame
        column: Column name
        output_path: Path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(df[column].dropna(), bins=30, color='skyblue', edgecolor='black')
    axes[0].set_title(f'Distribution of {column}', fontsize=12, fontweight='bold')
    axes[0].set_xlabel(column)
    axes[0].set_ylabel('Frequency')
    axes[0].grid(alpha=0.3)
    
    # Box plot
    axes[1].boxplot(df[column].dropna(), vert=True)
    axes[1].set_title(f'Box Plot of {column}', fontsize=12, fontweight='bold')
    axes[1].set_ylabel(column)
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved distribution plot to {output_path}")
    
    plt.close(fig)


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str = None):
    """
    Plot correlation heatmap for numeric columns.
    
    Args:
        df: Input DataFrame
        output_path: Path to save figure
    """
    logger.info("Creating correlation heatmap")
    
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    fig = plt.figure(figsize=(14, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix of Numeric Features', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved correlation heatmap to {output_path}")
    
    plt.close(fig)


def plot_missing_values(df: pd.DataFrame, output_path: str = None):
    """
    Plot missing values analysis.
    
    Args:
        df: Input DataFrame
        output_path: Path to save figure
    """
    logger.info("Creating missing values plot")
    
    missing_percent = (df.isnull().sum() / len(df)) * 100
    missing_percent = missing_percent[missing_percent > 0].sort_values(ascending=False)
    
    if len(missing_percent) == 0:
        logger.info("No missing values found")
        return
    
    fig = plt.figure(figsize=(12, 6))
    missing_percent.plot(kind='barh', color='coral')
    plt.title('Missing Values Percentage by Column', fontsize=14, fontweight='bold')
    plt.xlabel('Percentage (%)')
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved missing values plot to {output_path}")
    
    plt.close(fig)


def plot_feature_importance_by_target(df: pd.DataFrame, target_col: str, 
                                     feature_cols: list, output_path: str = None):
    """
    Plot feature distributions grouped by target variable.
    
    Args:
        df: Input DataFrame
        target_col: Target column name
        feature_cols: List of feature columns to analyze
        output_path: Path to save figure
    """
    logger.info(f"Creating feature analysis plots grouped by {target_col}")
    
    n_features = len(feature_cols)
    n_cols = 2
    n_rows = (n_features + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, n_rows * 5))
    axes = axes.flatten()
    
    for idx, feature in enumerate(feature_cols):
        if feature in df.columns and pd.api.types.is_numeric_dtype(df[feature]):
            for group in df[target_col].unique():
                subset = df[df[target_col] == group][feature]
                axes[idx].hist(subset, alpha=0.6, label=f'{target_col}={group}', bins=20)
            axes[idx].set_title(f'{feature} by {target_col}', fontweight='bold')
            axes[idx].set_xlabel(feature)
            axes[idx].set_ylabel('Frequency')
            axes[idx].legend()
            axes[idx].grid(alpha=0.3)
    
    # Hide unused subplots
    for idx in range(n_features, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved feature importance plot to {output_path}")
    
    plt.close(fig)


def generate_eda_report(df: pd.DataFrame, target_col: str = None, 
                       output_dir: str = 'outputs/eda') -> str:
    """
    Generate comprehensive EDA report.
    
    Args:
        df: Input DataFrame
        target_col: Target column name for stratified analysis
        output_dir: Directory to save reports and plots
        
    Returns:
        Path to report file
    """
    logger.info("Generating comprehensive EDA report")
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_path = Path(output_dir) / 'eda_report.txt'
    
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("EXPLORATORY DATA ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        # Dataset Overview
        f.write("1. DATASET OVERVIEW\n")
        f.write("-" * 80 + "\n")
        f.write(f"Shape: {df.shape}\n")
        f.write(f"Total Cells: {df.shape[0] * df.shape[1]}\n")
        f.write(f"Total Missing Cells: {df.isnull().sum().sum()}\n")
        f.write(f"Missing Percentage: {(df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.2f}%\n")
        f.write(f"Duplicate Rows: {df.duplicated().sum()}\n\n")
        
        # Data Types
        f.write("2. DATA TYPES\n")
        f.write("-" * 80 + "\n")
        f.write(str(df.dtypes) + "\n\n")
        
        # Missing Values
        f.write("3. MISSING VALUES\n")
        f.write("-" * 80 + "\n")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            f.write(missing[missing > 0].to_string() + "\n\n")
        else:
            f.write("No missing values found.\n\n")
        
        # Summary Statistics
        f.write("4. SUMMARY STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(str(df.describe()) + "\n\n")
        
        # Correlation Matrix
        f.write("5. CORRELATION MATRIX\n")
        f.write("-" * 80 + "\n")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            f.write(str(df[numeric_cols].corr()) + "\n\n")
        else:
            f.write("No numeric columns found.\n\n")
        
        # Target Variable Analysis (if specified)
        if target_col and target_col in df.columns:
            f.write("6. TARGET VARIABLE ANALYSIS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Target Column: {target_col}\n")
            f.write(f"Value Counts:\n{df[target_col].value_counts()}\n")
            f.write(f"Value Distribution:\n{(df[target_col].value_counts() / len(df) * 100).round(2)}\n\n")

        if {'TotalPremium', 'TotalClaims'}.issubset(df.columns):
            df_ratio = add_loss_ratio(df)
            f.write("7. GUIDING QUESTIONS\n")
            f.write("-" * 80 + "\n")
            for group_col in ['Province', 'VehicleType', 'Gender']:
                if group_col in df_ratio.columns:
                    grouped = df_ratio.groupby(group_col, observed=False).agg(
                        TotalPremium=('TotalPremium', 'sum'),
                        TotalClaims=('TotalClaims', 'sum'),
                        LossRatio=('LossRatio', 'mean')
                    ).sort_values('LossRatio', ascending=False)
                    f.write(f"\nLoss Ratio by {group_col}:\n{grouped.head(10)}\n")

            if {'TransactionMonth', 'TotalClaims'}.issubset(df_ratio.columns):
                month = pd.to_datetime(df_ratio['TransactionMonth'], errors='coerce').dt.to_period('M')
                trend = df_ratio.assign(Period=month).groupby('Period').agg(
                    ClaimFrequency=('TotalClaims', lambda s: (s > 0).mean()),
                    ClaimSeverity=('TotalClaims', lambda s: s[s > 0].mean())
                )
                f.write(f"\nTemporal claim frequency/severity:\n{trend.tail(12)}\n")

            if {'make', 'Model', 'TotalClaims', 'TotalPremium'}.issubset(df_ratio.columns):
                vehicle_risk = df_ratio.groupby(['make', 'Model'], observed=False).agg(
                    Policies=('PolicyID', 'count') if 'PolicyID' in df_ratio.columns else ('TotalPremium', 'count'),
                    TotalPremium=('TotalPremium', 'sum'),
                    TotalClaims=('TotalClaims', 'sum'),
                    LossRatio=('LossRatio', 'mean')
                ).sort_values('LossRatio', ascending=False)
                f.write(f"\nVehicle make/model risk profiles:\n{vehicle_risk.head(10)}\n")
    
    logger.info(f"EDA report saved to {report_path}")
    return str(report_path)
