"""Tests for model inspection logic."""

import pytest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

from mlq.inspector import (
    extract_metadata,
    get_feature_names,
    detect_estimator_type,
)


@pytest.fixture
def rf_model_with_names():
    """RandomForest trained with feature names."""
    X, y = make_classification(n_samples=50, n_features=10, n_informative=5, random_state=42)
    # Use DataFrame to get feature names
    X_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    rf = RandomForestClassifier(n_estimators=2, random_state=42, max_depth=3)
    rf.fit(X_df, y)
    return rf


@pytest.fixture
def lr_model_with_names():
    """LogisticRegression trained with feature names."""
    X, y = make_classification(n_samples=50, n_features=8, n_informative=4, random_state=42)
    X_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(8)])
    lr = LogisticRegression(max_iter=100, random_state=42)
    lr.fit(X_df, y)
    return lr


def test_extract_metadata_rf(rf_model_with_names):
    """Test extracting metadata from RandomForest."""
    meta = extract_metadata(rf_model_with_names)

    assert meta["class_name"] == "RandomForestClassifier"
    assert meta["n_features"] == 10
    assert meta["n_classes"] == 2
    assert meta["estimator_type"] == "tree"
    assert "params" in meta
    assert isinstance(meta["params"], dict)


def test_extract_metadata_lr(lr_model_with_names):
    """Test extracting metadata from LogisticRegression."""
    meta = extract_metadata(lr_model_with_names)

    assert meta["class_name"] == "LogisticRegression"
    assert meta["n_features"] == 8
    assert meta["n_classes"] == 2
    assert meta["estimator_type"] == "linear"
    assert "params" in meta


def test_get_feature_names_with_names(rf_model_with_names):
    """Test extracting feature names from model."""
    names = get_feature_names(rf_model_with_names)

    # Should have feature names since trained with DataFrame
    assert names is not None
    assert len(names) == 10
    assert all(isinstance(n, str) for n in names)
    # Check they match what we set
    assert names[0] == "feature_0"


def test_get_feature_names_without_names():
    """Test model without feature names returns None."""
    # Create model but don't fit (shouldn't have feature_names_in_)
    rf = RandomForestClassifier(n_estimators=2)
    names = get_feature_names(rf)
    assert names is None


def test_detect_estimator_type():
    """Test estimator type detection."""
    rf = RandomForestClassifier()
    assert detect_estimator_type(rf) == "tree"

    lr = LogisticRegression()
    assert detect_estimator_type(lr) == "linear"
