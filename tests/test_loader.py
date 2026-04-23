"""Tests for model loading logic."""

import tempfile
from pathlib import Path
from typing import Any

import joblib
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from mlq.loader import load_model


@pytest.fixture
def tmp_rf_model() -> Path:
    """Create a temporary trained RandomForest model."""
    # Create small synthetic dataset
    X, y = make_classification(n_samples=50, n_features=10, n_informative=5, random_state=42)
    
    # Train tiny RF
    rf = RandomForestClassifier(n_estimators=2, random_state=42)
    rf.fit(X, y)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        joblib.dump(rf, f.name)
        return Path(f.name)


def test_load_valid_joblib_model(tmp_rf_model: Path) -> None:
    """Test loading a valid joblib-saved model."""
    result = load_model(str(tmp_rf_model))
    
    assert "model" in result
    assert "path" in result
    assert "size_kb" in result
    assert result["size_kb"] > 0
    assert result["model"] is not None
    
    # Cleanup
    tmp_rf_model.unlink()


def test_load_missing_file() -> None:
    """Test that missing file exits with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        load_model("/nonexistent/path/model.pkl")
    
    assert exc_info.value.code == 1


def test_load_corrupted_file() -> None:
    """Test that corrupted file exits with code 1."""
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        # Write garbage bytes
        f.write(b"this is not a valid pickle file\x00\xff\xfe")
        temp_path = f.name
    
    try:
        with pytest.raises(SystemExit) as exc_info:
            load_model(temp_path)
        assert exc_info.value.code == 1
    finally:
        Path(temp_path).unlink()
