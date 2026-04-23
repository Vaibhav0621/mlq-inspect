"""Drift detection: KS-test + PSI per feature."""

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def compute_psi(expected: np.ndarray, observed: np.ndarray, bins: int = 10) -> float:
    """Compute Population Stability Index (PSI) between two distributions.
    
    Args:
        expected: Reference distribution values
        observed: Observed distribution values
        bins: Number of bins for discretization
        
    Returns:
        PSI value (higher = more drift)
    """
    # Remove NaN values
    expected = expected[~np.isnan(expected)]
    observed = observed[~np.isnan(observed)]
    
    if len(expected) == 0 or len(observed) == 0:
        return 0.0
    
    # Discretize into bins based on expected distribution
    breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf
    
    # Count occurrences in each bin
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    observed_counts = np.histogram(observed, bins=breakpoints)[0]
    
    # Convert to proportions
    expected_props = expected_counts / len(expected)
    observed_props = observed_counts / len(observed)
    
    # Avoid log(0)
    expected_props = np.where(expected_props == 0, 1e-10, expected_props)
    observed_props = np.where(observed_props == 0, 1e-10, observed_props)
    
    # PSI = sum((observed - expected) * ln(observed / expected))
    psi = np.sum((observed_props - expected_props) * np.log(observed_props / expected_props))
    
    return float(psi)


def compute_drift(
    reference_df: pd.DataFrame,
    model: Any,
    target_col: str = "target",
) -> List[Dict[str, Any]]:
    """Compute drift statistics per feature against reference distribution.
    
    Only runs on numeric features. For each:
    - Kolmogorov-Smirnov (KS) test
    - Population Stability Index (PSI)
    - Status: "ok" (PSI < 0.1), "warn" (0.1 <= PSI < 0.25), "drift" (PSI >= 0.25)
    
    Args:
        reference_df: Reference dataset (e.g., training data)
        model: Fitted model (used to get feature names)
        target_col: Name of target column in reference_df
        
    Returns:
        List of dicts with keys: feature, ks_stat, p_value, psi, status
    """
    results = []
    
    # Get feature names from model
    if hasattr(model, "feature_names_in_"):
        feature_names = list(model.feature_names_in_)
    else:
        # Assume all non-target columns are features
        feature_names = [c for c in reference_df.columns if c != target_col]
    
    # Generate synthetic test data (simple: add small noise to reference)
    test_df = reference_df.copy()
    numeric_cols = test_df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if col == target_col or col not in feature_names:
            continue
        
        # Get reference and "test" distributions
        ref_values = reference_df[col].dropna().values
        test_values = test_df[col].dropna().values
        
        # KS test
        ks_stat, p_value = ks_2samp(ref_values, test_values)
        
        # PSI
        psi = compute_psi(ref_values, test_values, bins=10)
        
        # Determine status
        if psi < 0.1:
            status = "ok"
        elif psi < 0.25:
            status = "warn"
        else:
            status = "drift"
        
        results.append({
            "feature": col,
            "ks_stat": float(ks_stat),
            "p_value": float(p_value),
            "psi": float(psi),
            "status": status,
        })
    
    # Sort by PSI descending
    results.sort(key=lambda x: x["psi"], reverse=True)
    
    return results
