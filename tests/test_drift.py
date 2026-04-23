"""Tests for drift detection."""

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from mlq.drift import compute_drift, compute_psi


@pytest.fixture
def reference_data():
    """Create reference dataset."""
    np.random.seed(42)
    X, y = make_classification(n_samples=200, n_features=5, random_state=42)

    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(5)])
    df["target"] = y
    return df


@pytest.fixture
def trained_model(reference_data):
    """Train model on reference data."""
    X = reference_data.drop(columns=["target"]).values
    y = reference_data["target"].values

    model = RandomForestClassifier(n_estimators=2, random_state=42)
    model.fit(X, y)
    return model


def test_no_drift(reference_data, trained_model):
    """Test that same distribution has no drift."""
    results = compute_drift(reference_data, trained_model, target_col="target")

    # All features should have status "ok" for identical distribution
    assert len(results) > 0
    # Most should be "ok" (PSI < 0.1 for no actual drift)
    ok_count = sum(1 for r in results if r["status"] == "ok")
    assert ok_count >= len(results) * 0.7  # At least 70% should be ok


def test_drift_detected():
    """Test that shifted distribution is detected as drift."""
    np.random.seed(42)

    # Create reference data
    ref_data = np.random.normal(0, 1, (200, 5))
    ref_df = pd.DataFrame(ref_data, columns=[f"feature_{i}" for i in range(5)])
    ref_df["target"] = np.random.randint(0, 2, 200)

    # Train model
    model = RandomForestClassifier(n_estimators=2, random_state=42)
    model.fit(ref_data, ref_df["target"].values)

    # Create shifted test data with large drift
    test_data = ref_data + 5.0  # Shift by 5 std devs
    test_df = pd.DataFrame(test_data, columns=[f"feature_{i}" for i in range(5)])
    test_df["target"] = np.random.randint(0, 2, 200)

    # Compute PSI between ref and test
    for i in range(5):
        psi = compute_psi(ref_data[:, i], test_data[:, i], bins=10)
        # Large shift should result in high PSI
        assert psi > 0.5


def test_psi_calculation():
    """Test PSI calculation with known input/output."""
    # Two identical distributions should have PSI ~= 0
    data = np.random.normal(0, 1, 1000)
    psi = compute_psi(data, data, bins=10)
    assert psi < 0.01

    # Shifted distribution should have higher PSI
    shifted = data + 2.0
    psi_shifted = compute_psi(data, shifted, bins=10)
    assert psi_shifted > 0.1
