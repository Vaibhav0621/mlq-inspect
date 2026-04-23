"""Report generation: Markdown and HTML via Jinja2."""

import base64
import io
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import jinja2
from jinja2 import Environment, select_autoescape


def generate_shap_chart_base64(
    feature_names: List[str],
    shap_values: List[float],
    top_n: int = 10,
) -> str:
    """Generate SHAP importance chart as base64-encoded PNG.
    
    Args:
        feature_names: List of feature names
        shap_values: List of SHAP values (mean absolute)
        top_n: Number of top features to show
        
    Returns:
        Base64-encoded PNG string
    """
    # Limit to top_n
    if len(feature_names) > top_n:
        feature_names = feature_names[:top_n]
        shap_values = shap_values[:top_n]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar plot
    ax.barh(range(len(feature_names)), shap_values, color="steelblue")
    ax.set_yticks(range(len(feature_names)))
    ax.set_yticklabels(feature_names)
    ax.set_xlabel("Mean |SHAP value|")
    ax.set_title("Feature Importance (SHAP)")
    ax.invert_yaxis()
    
    plt.tight_layout()
    
    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    
    # Encode to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    return img_base64


def generate_markdown(
    metadata: Dict[str, Any],
    shap_data: Optional[List[tuple]],
    drift_data: Optional[List[Dict]],
) -> str:
    """Generate Markdown report.
    
    Args:
        metadata: Model metadata dict
        shap_data: SHAP features list (feature_name, value) or None
        drift_data: Drift results list or None
        
    Returns:
        Markdown string
    """
    lines = []
    
    # Header
    lines.append(f"# Model Inspection Report: {metadata['class_name']}\n")
    
    # Metadata section
    lines.append("## Model Metadata\n")
    lines.append(f"- **Class**: {metadata['class_name']}\n")
    lines.append(f"- **Number of Features**: {metadata['n_features']}\n")
    
    if metadata.get('n_classes'):
        lines.append(f"- **Number of Classes**: {metadata['n_classes']}\n")
        if metadata.get('classes'):
            lines.append(f"- **Classes**: {', '.join(str(c) for c in metadata['classes'])}\n")
    
    lines.append(f"- **Estimator Type**: {metadata['estimator_type']}\n")
    
    if metadata.get('feature_names'):
        lines.append(f"\n### Feature Names\n")
        for i, name in enumerate(metadata['feature_names'][:20], 1):
            lines.append(f"{i}. {name}\n")
        if len(metadata['feature_names']) > 20:
            lines.append(f"... and {len(metadata['feature_names']) - 20} more\n")
    
    # Hyperparameters section
    lines.append("\n## Hyperparameters\n")
    params = metadata.get('params', {})
    for key, value in sorted(params.items()):
        lines.append(f"- `{key}`: {value}\n")
    
    # SHAP section
    if shap_data:
        lines.append("\n## Feature Importance (SHAP)\n")
        lines.append("| Feature | Mean |SHAP| |\n")
        lines.append("|---------|------|\n")
        for feature, value in shap_data[:10]:
            lines.append(f"| {feature} | {value:.6f} |\n")
    else:
        lines.append("\n## Feature Importance (SHAP)\n")
        lines.append("*SHAP computation skipped or failed*\n")
    
    # Drift section
    if drift_data:
        lines.append("\n## Drift Detection\n")
        lines.append("| Feature | KS Stat | P-Value | PSI | Status |\n")
        lines.append("|---------|---------|---------|-----|--------|\n")
        for drift in drift_data[:20]:
            lines.append(
                f"| {drift['feature']} | {drift['ks_stat']:.4f} | "
                f"{drift['p_value']:.4f} | {drift['psi']:.4f} | {drift['status']} |\n"
            )
    
    return "".join(lines)


def generate_html(
    metadata: Dict[str, Any],
    shap_data: Optional[List[tuple]],
    drift_data: Optional[List[Dict]],
) -> str:
    """Generate HTML report via Jinja2 template.
    
    Args:
        metadata: Model metadata dict
        shap_data: SHAP features list or None
        drift_data: Drift results list or None
        
    Returns:
        HTML string
    """
    # Load template using FileSystemLoader to work with moved templates
    import os
    from pathlib import Path
    
    template_dir = Path(__file__).parent
    env = Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    
    template = env.get_template("report.html.j2")
    
    # Generate SHAP chart if available
    shap_chart_base64 = None
    if shap_data:
        feature_names = [f[0] for f in shap_data]
        shap_values = [f[1] for f in shap_data]
        shap_chart_base64 = generate_shap_chart_base64(feature_names, shap_values)
    
    # Render template
    html = template.render(
        metadata=metadata,
        shap_data=shap_data[:10] if shap_data else None,
        drift_data=drift_data[:20] if drift_data else None,
        shap_chart_base64=shap_chart_base64,
    )
    
    return html
