# Task 1: Exploratory Data Analysis (EDA)

## Overview

This notebook demonstrates comprehensive exploratory data analysis (EDA) on the insurance risk dataset. The EDA process helps understand data structure, distributions, relationships, and identify patterns that inform the predictive modeling phase.

## Key Objectives

1. **Data Loading & Inspection**: Load and examine the dataset structure
2. **Statistical Summary**: Compute descriptive statistics and distributions
3. **Missing Data Analysis**: Identify and visualize missing values
4. **Distribution Analysis**: Examine feature distributions and identify outliers
5. **Correlation Analysis**: Identify relationships between variables
6. **Target Variable Analysis**: Understand the distribution of risk categories
7. **Feature Relationships**: Analyze how features interact with the target variable

## Dataset Overview

The insurance dataset contains the following features:

### Continuous Variables
- **age**: Customer age (18-80 years)
- **premium_annual**: Annual insurance premium ($)
- **coverage_amount**: Total coverage amount ($)
- **risk_score**: Calculated risk score (1-10)
- **policy_duration_years**: Years of policy ownership
- **total_claims_amount**: Total claims filed ($)

### Categorical Variables
- **smoker**: Smoking status (0=No, 1=Yes)
- **risk_category**: Risk classification (Low, Medium, High)
- **employment_status**: Employment type
- **income_bracket**: Income range
- **claim_history**: Number of previous claims
- **claims_filed_1y**: Claims filed in past year
- **health_conditions**: Number of pre-existing conditions

## Analysis Steps

### 1. Data Loading and Initial Exploration

```python
import pandas as pd
import numpy as np
from src.data_processing import load_raw_data
from src.eda_utils import generate_summary_statistics

# Load data
df = load_raw_data('data/raw/insurance_data.csv')

# Display basic info
print(df.head())
print(df.info())
print(df.describe())
```

### 2. Missing Values Analysis

Examine the extent and pattern of missing data:

```python
from src.eda_utils import plot_missing_values

# Visualize missing values
plot_missing_values(df, output_path='outputs/eda/missing_values.png')

# Get missing value statistics
missing_summary = df.isnull().sum()
print(missing_summary)
```

### 3. Distribution Analysis

Analyze distributions of key features:

```python
from src.eda_utils import plot_distribution

# Plot distributions for numeric columns
numeric_cols = df.select_dtypes(include=['number']).columns

for col in numeric_cols[:5]:
    plot_distribution(df, col, output_path=f'outputs/eda/dist_{col}.png')
```

### 4. Correlation Analysis

Examine relationships between variables:

```python
from src.eda_utils import plot_correlation_heatmap

# Create correlation heatmap
plot_correlation_heatmap(df, output_path='outputs/eda/correlation_matrix.png')

# Get top correlations
corr_matrix = df.corr()
```

### 5. Target Variable Analysis

Understand risk category distribution:

```python
# Distribution of target variable
print(df['risk_category'].value_counts())
print(df['risk_category'].value_counts(normalize=True))

# Visualize
df['risk_category'].value_counts().plot(kind='bar')
plt.title('Risk Category Distribution')
plt.show()
```

### 6. Feature Relationships with Target

```python
from src.eda_utils import plot_feature_importance_by_target

# Analyze how features vary by risk category
feature_cols = ['age', 'premium_annual', 'coverage_amount', 'risk_score']
plot_feature_importance_by_target(
    df, 'risk_category', feature_cols,
    output_path='outputs/eda/features_by_target.png'
)
```

## Key Insights from EDA

After running the EDA, you should discover:

1. **Premium Patterns**: Higher premiums correlate with age and smoker status
2. **Risk Distribution**: Most customers fall into Medium risk category
3. **Coverage Trends**: Coverage amount increases with premium levels
4. **Age Effect**: Strong relationship between age and both premium and risk
5. **Claims Pattern**: Previous claims significantly increase premiums

## Output Files

The EDA process generates:

- `01_missing_values.png`: Missing data visualization
- `02_correlation_heatmap.png`: Feature correlation matrix
- `03_distribution_*.png`: Individual feature distributions
- `04_features_by_risk_category.png`: Feature distributions by risk category
- `eda_report.txt`: Comprehensive text report with statistics

## Next Steps

After EDA, proceed to:
1. **Data Preprocessing** (Task 1 continued): Clean and prepare data
2. **Hypothesis Testing** (Task 2): Validate statistical assumptions
3. **Modeling**: Build predictive models based on insights

## References

- Statistical concepts: Descriptive statistics, correlation, distributions
- Tools: Pandas, Matplotlib, Seaborn for visualization
- Best practices: Handle outliers, normalize features, balance classes
