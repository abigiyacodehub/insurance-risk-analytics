"""
Unit tests for data processing module.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_processing import (
    handle_missing_values,
    remove_outliers,
    normalize_numeric_features,
    encode_categorical_features
)


class TestMissingValueHandling:
    """Tests for missing value handling."""
    
    def test_handle_missing_values_mean(self):
        """Test mean imputation strategy."""
        df = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5],
            'B': [10, np.nan, 30, 40, 50]
        })
        
        result = handle_missing_values(df, strategy='mean')
        
        assert result.isnull().sum().sum() == 0
        assert result['A'].iloc[2] == pytest.approx(3.0)
    
    def test_handle_missing_values_drop(self):
        """Test drop strategy for missing values."""
        df = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        result = handle_missing_values(df, strategy='drop')
        
        assert len(result) == 4
        assert result.isnull().sum().sum() == 0


class TestOutlierRemoval:
    """Tests for outlier detection and removal."""
    
    def test_remove_outliers_iqr(self):
        """Test IQR method for outlier removal."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 100]  # 100 is outlier
        })
        
        result = remove_outliers(df, columns=['A'], method='iqr')
        
        assert len(result) < len(df)
        assert result['A'].max() < 100
    
    def test_remove_outliers_zscore(self):
        """Test z-score method for outlier removal."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 100]
        })
        
        result = remove_outliers(df, columns=['A'], method='zscore')
        
        assert len(result) < len(df)


class TestFeatureNormalization:
    """Tests for feature normalization."""
    
    def test_normalize_numeric_features(self):
        """Test normalization to [0,1] range."""
        df = pd.DataFrame({
            'A': [0, 5, 10],
            'B': [10, 20, 30]
        })
        
        result = normalize_numeric_features(df, columns=['A', 'B'])
        
        assert result['A'].min() == pytest.approx(0.0)
        assert result['A'].max() == pytest.approx(1.0)
        assert result['B'].min() == pytest.approx(0.0)
        assert result['B'].max() == pytest.approx(1.0)


class TestCategoricalEncoding:
    """Tests for categorical feature encoding."""
    
    def test_encode_categorical_features(self):
        """Test one-hot encoding of categorical features."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'A', 'C', 'B'],
            'value': [1, 2, 3, 4, 5]
        })
        
        result, mapping = encode_categorical_features(df, columns=['category'])
        
        assert 'category' in result.columns
        assert isinstance(mapping['category'], dict)
        assert len(mapping['category']) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
