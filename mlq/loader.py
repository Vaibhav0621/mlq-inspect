"""Model loading logic with joblib + pickle fallback."""

import os
import sys
from pathlib import Path
from typing import Any, Dict

import joblib
import pickle

from mlq.utils import console, print_error


def load_model(model_path: str) -> Dict[str, Any]:
    """Load a trained sklearn-compatible model.
    
    Tries joblib first, falls back to pickle. Returns metadata dict with model,
    path, and file size in KB.
    
    Args:
        model_path: Path to model file (.pkl, .joblib, etc.)
        
    Returns:
        Dict with keys: model, path, size_kb
        
    Raises:
        SystemExit: If file not found or unpickling fails
    """
    path = Path(model_path)
    
    # Check file exists
    if not path.exists():
        print_error(f"Model file not found: {model_path}")
        sys.exit(1)
    
    # Get file size in KB
    size_kb = path.stat().st_size / 1024
    
    # Try joblib first
    try:
        model = joblib.load(model_path)
        return {
            "model": model,
            "path": str(path.absolute()),
            "size_kb": size_kb,
        }
    except Exception as e:
        console.log(f"[dim]joblib.load() failed, trying pickle: {e}[/dim]")
    
    # Fall back to pickle
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return {
            "model": model,
            "path": str(path.absolute()),
            "size_kb": size_kb,
        }
    except Exception as e:
        print_error(
            f"Failed to load model: {e}\n"
            "The model may have been saved with a different scikit-learn version. "
            "Try retraining with your current environment."
        )
        sys.exit(1)
