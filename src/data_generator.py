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
    
    provinces = np.array([
        "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape",
        "Free State", "Limpopo", "Mpumalanga", "North West", "Northern Cape"
    ])
    province_risk = {
        "Gauteng": 1.15,
        "Western Cape": 0.95,
        "KwaZulu-Natal": 1.10,
        "Eastern Cape": 1.00,
        "Free State": 0.90,
        "Limpopo": 0.85,
        "Mpumalanga": 1.05,
        "North West": 0.92,
        "Northern Cape": 0.88,
    }
    vehicle_makes = np.array(["Toyota", "Volkswagen", "Ford", "BMW", "Mercedes-Benz", "Hyundai", "Nissan"])
    vehicle_make_risk = {
        "Toyota": 0.92,
        "Volkswagen": 1.00,
        "Ford": 1.03,
        "BMW": 1.35,
        "Mercedes-Benz": 1.30,
        "Hyundai": 0.90,
        "Nissan": 0.96,
    }
    vehicle_models = {
        "Toyota": ["Corolla", "Hilux", "Fortuner"],
        "Volkswagen": ["Polo", "Golf", "Tiguan"],
        "Ford": ["Fiesta", "Ranger", "EcoSport"],
        "BMW": ["320i", "X3", "X5"],
        "Mercedes-Benz": ["C-Class", "GLA", "GLE"],
        "Hyundai": ["i20", "Tucson", "Creta"],
        "Nissan": ["Micra", "Navara", "Qashqai"],
    }
    cover_types = np.array(["Comprehensive", "Third Party", "Fire and Theft"])
    cover_type_factor = {
        "Comprehensive": 1.30,
        "Third Party": 0.70,
        "Fire and Theft": 0.95,
    }
    vehicle_types = np.array(["Sedan", "SUV", "Hatchback", "Bakkie", "Truck"])
    vehicle_type_factor = {
        "Sedan": 0.95,
        "SUV": 1.15,
        "Hatchback": 0.88,
        "Bakkie": 1.10,
        "Truck": 1.35,
    }

    province = np.random.choice(provinces, n_samples, p=[0.25, 0.17, 0.16, 0.10, 0.07, 0.08, 0.07, 0.06, 0.04])
    zip_code = np.array([f"{np.random.randint(1000, 9999)}" for _ in range(n_samples)])
    gender = np.random.choice(["Female", "Male", "Not specified"], n_samples, p=[0.48, 0.49, 0.03])
    cover_type = np.random.choice(cover_types, n_samples, p=[0.58, 0.27, 0.15])
    vehicle_type = np.random.choice(vehicle_types, n_samples, p=[0.34, 0.24, 0.22, 0.16, 0.04])
    vehicle_make = np.random.choice(vehicle_makes, n_samples, p=[0.24, 0.20, 0.15, 0.10, 0.08, 0.12, 0.11])
    vehicle_model = np.array([np.random.choice(vehicle_models[make]) for make in vehicle_make])

    # Age: 18-80
    age = np.random.uniform(18, 80, n_samples)
    
    # Premium: influenced by age, smoker status, etc.
    base_premium = 500
    geo_factor = np.array([province_risk[item] for item in province])
    make_factor = np.array([vehicle_make_risk[item] for item in vehicle_make])
    cover_factor = np.array([cover_type_factor[item] for item in cover_type])
    type_factor = np.array([vehicle_type_factor[item] for item in vehicle_type])
    premium = (base_premium + (age * 20) + np.random.normal(100, 50, n_samples))
    premium = premium * geo_factor * make_factor * cover_factor * type_factor
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
    claim_severity = np.random.exponential(3000, n_samples) * geo_factor * make_factor * type_factor
    total_claims = claims_filed * claim_severity
    custom_value_estimate = coverage * np.random.uniform(0.08, 0.55, n_samples) * make_factor
    transaction_month = pd.to_datetime(
        np.random.choice(pd.date_range("2023-01-01", "2024-12-31", freq="D"), n_samples)
    )
    
    # Health conditions: number of pre-existing conditions
    health_conditions = np.random.poisson(1, n_samples)
    
    # Employment status
    employment_status = np.random.choice(['Employed', 'Self-employed', 'Unemployed', 'Retired'], n_samples)
    
    # Income bracket
    income = np.random.choice(['<$30k', '$30k-$60k', '$60k-$100k', '>$100k'], n_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'PolicyID': [f"POL{idx:07d}" for idx in range(1, n_samples + 1)],
        'TransactionMonth': transaction_month,
        'Province': province,
        'ZipCode': zip_code,
        'Gender': gender,
        'CoverType': cover_type,
        'VehicleType': vehicle_type,
        'make': vehicle_make,
        'Model': vehicle_model,
        'TotalPremium': np.round(premium, 2),
        'TotalClaims': np.round(total_claims, 2),
        'CustomValueEstimate': np.round(custom_value_estimate, 2),
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
