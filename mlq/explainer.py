"""SHAP integration for model explainability."""

from typing import Any, List, Optional, Tuple

import numpy as np
import pandas as pd
import shap
from rich.progress import Progress

from mlq.inspector import detect_estimator_type
from mlq.utils import console


def compute_shap(
    model: Any,
    X_background: Optional[np.ndarray] = None,
    X_test: Optional[np.ndarray] = None,
) -> Optional[List[Tuple[str, float]]]:
    """Compute SHAP values and return top N features by mean absolute SHAP.

    If X_background not provided, uses synthetic zero background.
    If SHAP computation fails, returns None and prints warning.

    Args:
        model: Fitted sklearn model
        X_background: Background data for SHAP explainer (100 samples ideal)
        X_test: Test data to explain (defaults to X_background)

    Returns:
        List of (feature_name, mean_abs_shap) tuples sorted descending, or None on failure
    """
    try:
        # Determine model type
        estimator_type = detect_estimator_type(model)

        # If no background provided, create synthetic
        n_features = getattr(model, "n_features_in_", None)
        if n_features is None:
            console.print("[yellow]Warning: Could not determine n_features[/yellow]")
            return None

        if X_background is None:
            X_background = np.zeros((100, n_features))
        else:
            # Convert DataFrame to numpy if needed
            if isinstance(X_background, pd.DataFrame):
                X_background = X_background.values

        if X_test is None:
            X_test = X_background
        else:
            # Convert DataFrame to numpy if needed
            if isinstance(X_test, pd.DataFrame):
                X_test = X_test.values

        # Limit background to 100 samples for speed
        if len(X_background) > 100:
            indices = np.random.choice(len(X_background), 100, replace=False)
            X_background = X_background[indices]

        # Limit test data to 100 samples for speed
        if len(X_test) > 100:
            indices = np.random.choice(len(X_test), 100, replace=False)
            X_test = X_test[indices]

        # Create explainer based on model type
        with Progress(transient=True) as progress:
            task = progress.add_task("[cyan]Computing SHAP values...", total=None)

            if estimator_type == "tree":
                explainer = shap.TreeExplainer(model)
            elif estimator_type == "linear":
                explainer = shap.LinearExplainer(model, X_background)
            else:
                console.print(
                    "[yellow]Using KernelExplainer for non-standard model. "
                    "This may be slow for large datasets.[/yellow]"
                )
                explainer = shap.KernelExplainer(model.predict, X_background)

            progress.stop_task(task)

        # Compute SHAP values
        shap_values = explainer.shap_values(X_test)

        # Normalize to 2D (n_samples, n_features)
        # Handle different output formats from SHAP:
        # - Binary classifier: (n_samples, n_features, 2) -> take mean across classes
        # - 3D from TreeExplainer on multiclass: (n_classes, n_samples, n_features)
        # - 2D: (n_samples, n_features)
        # - List of arrays: each is (n_samples, n_features)

        if isinstance(shap_values, list):
            # List of arrays (one per class)
            shap_values = np.array(shap_values)  # -> (n_classes, n_samples, n_features)
            # Average across classes
            shap_values = np.mean(np.abs(shap_values), axis=0)  # -> (n_samples, n_features)
        elif isinstance(shap_values, np.ndarray):
            # Handle 3D array from binary/multiclass classifiers
            if shap_values.ndim == 3:
                # (n_samples, n_features, n_classes) or similar
                # Take mean across the last dimension (classes)
                shap_values = np.mean(np.abs(shap_values), axis=-1)  # -> (n_samples, n_features)
            else:
                # Already 2D
                shap_values = np.mean(np.abs(shap_values), axis=0)  # -> (n_features,)

        # Ensure we have feature importance (1D array)
        if shap_values.ndim > 1:
            shap_values = np.mean(shap_values, axis=0)

        # Get feature names
        if hasattr(model, "feature_names_in_"):
            feature_names = list(model.feature_names_in_)
        else:
            feature_names = [f"feature_{i}" for i in range(n_features)]

        # Sort by absolute SHAP value (descending)
        indices = np.argsort(shap_values)[::-1]

        result = [
            (feature_names[i], float(shap_values[i]))
            for i in indices
        ]

        return result

    except Exception as e:
        console.print(f"[yellow]Warning: SHAP computation failed: {e}[/yellow]")
        return None
