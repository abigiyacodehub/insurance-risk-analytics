"""
Sample dataset generator for insurance risk analytics.
Creates a realistic insurance dataset for demonstration purposes.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_insurance_dataset(n_samples: int = 10000, seed: int = 42) -> pd.DataFrame:
    """
    Generate a realistic insurance dataset.
    
    Args:
        n_samples: Number of records to generate
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with insurance data
    """
    np.random.seed(seed)
    logger.info(f"Generating sample insurance dataset with {n_samples} records")
    
    # Age: 18-80
    age = np.random.uniform(18, 80, n_samples)
    
    # Premium: influenced by age, smoker status, etc.
    base_premium = 500
    premium = base_premium + (age * 20) + np.random.normal(100, 50, n_samples)
    premium = np.maximum(premium, 200)  # Minimum premium
    
    # Coverage amount: $100k - $2M
    coverage = np.random.uniform(100000, 2000000, n_samples)
    
    # Claim history: 0-5 claims
    claim_history = np.random.poisson(1, n_samples)
    
    # Smoker status
    smoker = np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    
    # Risk score: 1-10
    risk_score = np.clip(
        3 + (age / 10) + (smoker * 2) + (claim_history * 0.5) + np.random.normal(0, 1, n_samples),
        1, 10
    )
    
    # Risk category
    risk_category = pd.cut(risk_score, bins=[0, 3, 6, 10], labels=['Low', 'Medium', 'High'])
    
    # Claims filed in past year
    claims_filed = np.random.poisson(0.5, n_samples)
    
    # Total claims amount
    total_claims = claims_filed * np.random.exponential(3000, n_samples)
    
    # Health conditions: number of pre-existing conditions
    health_conditions = np.random.poisson(1, n_samples)
    
    # Employment status
    employment_status = np.random.choice(['Employed', 'Self-employed', 'Unemployed', 'Retired'], n_samples)
    
    # Income bracket
    income = np.random.choice(['<$30k', '$30k-$60k', '$60k-$100k', '>$100k'], n_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'age': np.round(age, 1),
        'premium_annual': np.round(premium, 2),
        'coverage_amount': np.round(coverage, 2),
        'claim_history': claim_history,
        'smoker': smoker,
        'risk_score': np.round(risk_score, 2),
        'risk_category': risk_category,
        'claims_filed_1y': claims_filed,
        'total_claims_amount': np.round(total_claims, 2),
        'health_conditions': health_conditions,
        'employment_status': employment_status,
        'income_bracket': income,
        'policy_duration_years': np.random.randint(1, 20, n_samples)
    })
    
    logger.info(f"Generated dataset shape: {df.shape}")
    return df


def save_sample_data(output_path: str = 'data/raw/insurance_data.csv'):
    """
    Generate and save sample insurance data.
    
    Args:
        output_path: Path to save the CSV file
        
    Returns:
        DataFrame
    """
    df = generate_sample_insurance_dataset()
    
    # Create directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Sample data saved to {output_path}")
    
    return df


if __name__ == '__main__':
    # Generate and save sample data
    save_sample_data()
