"""
Statistical tests for hypothesis testing in insurance analytics.
"""

import pandas as pd
import numpy as np
from scipy import stats
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_t_test(group1: np.ndarray, group2: np.ndarray, 
                   alternative: str = 'two-sided') -> dict:
    """
    Perform independent samples t-test.
    
    Args:
        group1: First group data
        group2: Second group data
        alternative: 'two-sided', 'less', or 'greater'
        
    Returns:
        Dictionary with test results
    """
    logger.info("Performing independent samples t-test")
    
    t_stat, p_value = stats.ttest_ind(group1, group2, alternative=alternative)
    
    return {
        'test': 'Independent t-test',
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'group1_mean': np.mean(group1),
        'group2_mean': np.mean(group2),
        'group1_std': np.std(group1),
        'group2_std': np.std(group2)
    }


def perform_chi_square_test(contingency_table: pd.DataFrame) -> dict:
    """
    Perform chi-square test of independence.
    
    Args:
        contingency_table: Contingency table (cross-tabulation)
        
    Returns:
        Dictionary with test results
    """
    logger.info("Performing chi-square test")
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    return {
        'test': 'Chi-square test',
        'chi_square_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'significant': p_value < 0.05,
        'expected_frequencies': expected
    }


def perform_correlation_test(x: np.ndarray, y: np.ndarray) -> dict:
    """
    Perform Pearson correlation test.
    
    Args:
        x: First variable
        y: Second variable
        
    Returns:
        Dictionary with correlation results
    """
    logger.info("Performing Pearson correlation test")
    
    correlation, p_value = stats.pearsonr(x, y)
    
    return {
        'test': 'Pearson correlation',
        'correlation': correlation,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'interpretation': 'Strong positive' if correlation > 0.7 else 
                         'Moderate positive' if correlation > 0.4 else
                         'Weak positive' if correlation > 0 else
                         'Strong negative' if correlation < -0.7 else
                         'Moderate negative' if correlation < -0.4 else 'Weak negative'
    }


def perform_anova_test(groups: list) -> dict:
    """
    Perform one-way ANOVA test.
    
    Args:
        groups: List of arrays, one for each group
        
    Returns:
        Dictionary with ANOVA results
    """
    logger.info("Performing one-way ANOVA test")
    
    f_stat, p_value = stats.f_oneway(*groups)
    
    group_means = [np.mean(group) for group in groups]
    group_stds = [np.std(group) for group in groups]
    
    return {
        'test': 'One-way ANOVA',
        'f_statistic': f_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'group_means': group_means,
        'group_stds': group_stds,
        'number_of_groups': len(groups)
    }


def compare_premiums_by_smoker(df: pd.DataFrame) -> dict:
    """
    Test if premiums differ significantly between smokers and non-smokers.
    
    Args:
        df: Insurance data DataFrame
        
    Returns:
        Test results
    """
    logger.info("Comparing premiums between smokers and non-smokers")
    
    smokers = df[df['smoker'] == 1]['premium_annual'].dropna()
    non_smokers = df[df['smoker'] == 0]['premium_annual'].dropna()
    
    results = perform_t_test(smokers.values, non_smokers.values)
    results['smokers_mean_premium'] = smokers.mean()
    results['non_smokers_mean_premium'] = non_smokers.mean()
    results['premium_difference'] = smokers.mean() - non_smokers.mean()
    
    return results


def compare_risk_by_age_group(df: pd.DataFrame) -> dict:
    """
    Test if risk scores differ across age groups.
    
    Args:
        df: Insurance data DataFrame
        
    Returns:
        Test results
    """
    logger.info("Comparing risk scores across age groups")
    
    # Create age groups
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 40, 55, 100], 
                             labels=['18-25', '26-40', '41-55', '56+'])
    
    age_groups = [df[df['age_group'] == group]['risk_score'].dropna().values 
                  for group in df['age_group'].unique()]
    
    results = perform_anova_test(age_groups)
    results['age_groups'] = df['age_group'].unique().tolist()
    
    return results


def test_claims_vs_coverage(df: pd.DataFrame) -> dict:
    """
    Test correlation between coverage amount and claims filed.
    
    Args:
        df: Insurance data DataFrame
        
    Returns:
        Test results
    """
    logger.info("Testing correlation between coverage and claims")
    
    coverage = df['coverage_amount'].dropna().values
    claims = df['claims_filed_1y'].dropna().values
    
    # Ensure same length
    min_len = min(len(coverage), len(claims))
    coverage = coverage[:min_len]
    claims = claims[:min_len]
    
    results = perform_correlation_test(coverage, claims)
    results['coverage_description'] = 'Coverage amount'
    results['claims_description'] = 'Claims filed in past year'
    
    return results


def generate_hypothesis_test_report(df: pd.DataFrame, output_path: str = 'outputs/hypothesis_tests.txt') -> str:
    """
    Generate comprehensive hypothesis testing report.
    
    Args:
        df: Insurance data DataFrame
        output_path: Path to save report
        
    Returns:
        Path to report file
    """
    logger.info("Generating hypothesis testing report")
    
    from pathlib import Path
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("HYPOTHESIS TESTING REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        # Test 1: Premiums by Smoker Status
        f.write("Test 1: Premiums by Smoker Status (Independent t-test)\n")
        f.write("-" * 80 + "\n")
        test1 = compare_premiums_by_smoker(df)
        f.write(f"H0: Smokers and non-smokers have same average premium\n")
        f.write(f"H1: Smokers and non-smokers have different average premiums\n")
        f.write(f"Smokers mean premium: ${test1['smokers_mean_premium']:.2f}\n")
        f.write(f"Non-smokers mean premium: ${test1['non_smokers_mean_premium']:.2f}\n")
        f.write(f"Difference: ${test1['premium_difference']:.2f}\n")
        f.write(f"t-statistic: {test1['t_statistic']:.4f}\n")
        f.write(f"p-value: {test1['p_value']:.6f}\n")
        f.write(f"Result: {'REJECT H0 - Statistically significant difference' if test1['significant'] else 'FAIL TO REJECT H0 - No significant difference'}\n\n")
        
        # Test 2: Risk Score by Age Group
        f.write("Test 2: Risk Score Differences Across Age Groups (ANOVA)\n")
        f.write("-" * 80 + "\n")
        test2 = compare_risk_by_age_group(df)
        f.write(f"H0: Risk scores are the same across age groups\n")
        f.write(f"H1: At least one age group has different risk score\n")
        f.write(f"F-statistic: {test2['f_statistic']:.4f}\n")
        f.write(f"p-value: {test2['p_value']:.6f}\n")
        f.write(f"Result: {'REJECT H0 - Statistically significant differences' if test2['significant'] else 'FAIL TO REJECT H0 - No significant differences'}\n\n")
        
        # Test 3: Coverage vs Claims
        f.write("Test 3: Correlation Between Coverage and Claims (Pearson)\n")
        f.write("-" * 80 + "\n")
        test3 = test_claims_vs_coverage(df)
        f.write(f"H0: No correlation between coverage amount and claims filed\n")
        f.write(f"H1: Coverage amount and claims filed are correlated\n")
        f.write(f"Correlation coefficient: {test3['correlation']:.4f}\n")
        f.write(f"p-value: {test3['p_value']:.6f}\n")
        f.write(f"Interpretation: {test3['interpretation']}\n")
        f.write(f"Result: {'REJECT H0 - Statistically significant correlation' if test3['significant'] else 'FAIL TO REJECT H0 - No significant correlation'}\n")
    
    logger.info(f"Hypothesis testing report saved to {output_path}")
    return output_path
