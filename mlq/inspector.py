"""Core inspection logic: extract metadata and feature info from models."""

from typing import Any, Dict, List, Optional



def get_feature_names(model: Any) -> Optional[List[str]]:
    """Extract feature names from model if available.

    Handles both sklearn 0.x (feature_names_in_) and older versions.

    Args:
        model: Fitted sklearn model

    Returns:
        List of feature names or None
    """
    # sklearn 1.0+ stores in feature_names_in_
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)

    # Try to get from pipeline or nested estimator
    if hasattr(model, "named_steps"):
        # Pipeline
        final_estimator = model.named_steps.get("clf") or model.named_steps.get("model")
        if final_estimator and hasattr(final_estimator, "feature_names_in_"):
            return list(final_estimator.feature_names_in_)

    return None


def detect_estimator_type(model: Any) -> str:
    """Detect estimator type for selecting appropriate explainer.

    Args:
        model: Fitted sklearn model

    Returns:
        One of: "tree", "linear", "other"
    """
    model_name = model.__class__.__name__

    # Tree-based models
    tree_models = {
        "RandomForestClassifier",
        "RandomForestRegressor",
        "GradientBoostingClassifier",
        "GradientBoostingRegressor",
        "DecisionTreeClassifier",
        "DecisionTreeRegressor",
        "ExtraTreesClassifier",
        "ExtraTreesRegressor",
        "XGBClassifier",
        "XGBRegressor",
        "LGBMClassifier",
        "LGBMRegressor",
        "CatBoostClassifier",
        "CatBoostRegressor",
    }

    if model_name in tree_models:
        return "tree"

    # Linear models
    linear_models = {
        "LogisticRegression",
        "LinearRegression",
        "Ridge",
        "Lasso",
        "ElasticNet",
        "RidgeCV",
        "LassoCV",
        "ElasticNetCV",
        "SGDClassifier",
        "SGDRegressor",
    }

    if model_name in linear_models:
        return "linear"

    return "other"


def extract_metadata(model: Any) -> Dict[str, Any]:
    """Extract comprehensive metadata from a fitted model.

    Args:
        model: Fitted sklearn model

    Returns:
        Dict with keys:
        - class_name: str
        - n_features: int
        - feature_names: List[str] or None
        - n_classes: int or None (for classifiers)
        - params: Dict (all hyperparameters)
        - estimator_type: str ("tree", "linear", "other")
        - training_score: float or None (if stored)
    """
    metadata: Dict[str, Any] = {}

    # Class name
    metadata["class_name"] = model.__class__.__name__

    # Number of features
    if hasattr(model, "n_features_in_"):
        metadata["n_features"] = int(model.n_features_in_)
    else:
        metadata["n_features"] = None

    # Feature names
    metadata["feature_names"] = get_feature_names(model)

    # Number of classes (for classifiers)
    if hasattr(model, "classes_"):
        metadata["n_classes"] = len(model.classes_)
        metadata["classes"] = list(model.classes_)
    else:
        metadata["n_classes"] = None
        metadata["classes"] = None

    # All hyperparameters
    if hasattr(model, "get_params"):
        try:
            metadata["params"] = model.get_params()
        except Exception:
            metadata["params"] = {}
    else:
        metadata["params"] = {}

    # Estimator type
    metadata["estimator_type"] = detect_estimator_type(model)

    # Training score if available
    if hasattr(model, "score"):
        metadata["training_score"] = None
    else:
        metadata["training_score"] = None

    return metadata
