"""Pytest configuration and shared fixtures."""

import tempfile
from pathlib import Path

import joblib
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np


@pytest.fixture(scope="session")
def sample_model_path():
    """Create a sample trained RandomForest model for testing."""
    # Create synthetic data
    X, y = make_classification(
        n_samples=100,
        n_features=10,
        n_informative=6,
        n_redundant=2,
        random_state=42,
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=5, random_state=42, max_depth=5)
    model.fit(X, y)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        joblib.dump(model, f.name)
        return Path(f.name)


@pytest.fixture(scope="session")
def sample_reference_csv(sample_model_path):
    """Create a sample reference CSV for drift testing."""
    # Generate data consistent with the model
    X, y = make_classification(
        n_samples=150,
        n_features=10,
        n_informative=6,
        n_redundant=2,
        random_state=42,
    )
    
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    df["target"] = y
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        df.to_csv(f.name, index=False)
        return Path(f.name)
