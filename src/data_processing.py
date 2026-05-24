"""
Data processing utilities for insurance risk analytics.
Handles data loading, cleaning, and preprocessing.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load raw insurance data from CSV file.
    
    Args:
        filepath: Path to raw data file
        
    Returns:
        DataFrame with raw data
    """
    logger.info(f"Loading data from {filepath}")
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise


def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: Input DataFrame
        strategy: 'mean', 'median', 'drop', or 'forward_fill'
        
    Returns:
        DataFrame with missing values handled
    """
    logger.info(f"Handling missing values using {strategy} strategy")
    df_clean = df.copy()
    
    if strategy == 'drop':
        df_clean = df_clean.dropna()
    elif strategy == 'mean':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif strategy == 'median':
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    elif strategy == 'forward_fill':
        df_clean = df_clean.ffill()
    
    logger.info(f"Missing values after handling: {df_clean.isnull().sum().sum()}")
    return df_clean


def remove_outliers(df: pd.DataFrame, columns: list, method: str = 'iqr') -> pd.DataFrame:
    """
    Remove outliers from specified columns.
    
    Args:
        df: Input DataFrame
        columns: List of column names to check for outliers
        method: 'iqr' or 'zscore'
        
    Returns:
        DataFrame with outliers removed
    """
    logger.info(f"Removing outliers using {method} method")
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    if method == 'iqr':
        for col in columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
    
    elif method == 'zscore':
        numeric_cols = df_clean[columns].select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            median = df_clean[col].median()
            mad = np.median(np.abs(df_clean[col] - median))
            if mad == 0:
                std = df_clean[col].std(ddof=0)
                if std == 0:
                    continue
                z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / std)
                df_clean = df_clean[z_scores < 3]
                continue

            modified_z_scores = 0.6745 * (df_clean[col] - median) / mad
            df_clean = df_clean[np.abs(modified_z_scores) < 3.5]
    
    removed_rows = initial_rows - len(df_clean)
    logger.info(f"Removed {removed_rows} outlier rows. Remaining: {len(df_clean)}")
    return df_clean


def normalize_numeric_features(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Normalize numeric features to [0, 1] range.
    
    Args:
        df: Input DataFrame
        columns: List of columns to normalize. If None, normalize all numeric columns.
        
    Returns:
        DataFrame with normalized features
    """
    df_norm = df.copy()
    
    if columns is None:
        columns = df_norm.select_dtypes(include=[np.number]).columns.tolist()
    
    logger.info(f"Normalizing {len(columns)} numeric columns")
    
    for col in columns:
        min_val = df_norm[col].min()
        max_val = df_norm[col].max()
        if max_val - min_val > 0:
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
    
    return df_norm


def encode_categorical_features(df: pd.DataFrame, columns: list = None) -> tuple:
    """
    One-hot encode categorical features.
    
    Args:
        df: Input DataFrame
        columns: List of categorical columns to encode. If None, encode all object columns.
        
    Returns:
        Tuple of (encoded DataFrame, mapping dictionary)
    """
    df_encoded = df.copy()
    
    if columns is None:
        columns = df_encoded.select_dtypes(include=['object']).columns.tolist()
    
    logger.info(f"Encoding {len(columns)} categorical columns")
    
    encoding_map = {}
    for col in columns:
        df_encoded[col], mapping = pd.factorize(df_encoded[col])
        encoding_map[col] = dict(enumerate(mapping))
    
    return df_encoded, encoding_map


def preprocess_data(
    raw_data_path: str,
    processed_data_path: str,
    missing_value_strategy: str = 'mean',
    outlier_method: str = 'iqr',
    outlier_columns: list = None
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline.
    
    Args:
        raw_data_path: Path to raw data
        processed_data_path: Path to save processed data
        missing_value_strategy: Strategy for handling missing values
        outlier_method: Method for outlier detection
        outlier_columns: Columns to check for outliers
        
    Returns:
        Processed DataFrame
    """
    logger.info("Starting data preprocessing pipeline")
    
    # Load data
    df = load_raw_data(raw_data_path)
    
    # Handle missing values
    df = handle_missing_values(df, strategy=missing_value_strategy)
    
    # Remove outliers if columns specified
    if outlier_columns:
        df = remove_outliers(df, columns=outlier_columns, method=outlier_method)
    
    # Encode categorical features
    df, encoding_map = encode_categorical_features(df)
    
    # Save processed data
    Path(processed_data_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_data_path, index=False)
    logger.info(f"Saved processed data to {processed_data_path}")
    
    return df
