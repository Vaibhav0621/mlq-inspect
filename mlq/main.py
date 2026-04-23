"""MLQ CLI app — main entry point with all Typer commands."""

from pathlib import Path
from typing import Optional

import typer
import pandas as pd
from rich.table import Table
from rich.panel import Panel

from mlq import __version__
from mlq.loader import load_model
from mlq.inspector import extract_metadata
from mlq.explainer import compute_shap
from mlq.drift import compute_drift
from mlq.reporter import generate_markdown, generate_html
from mlq.utils import console, format_bar, print_error, print_success

app = typer.Typer(
    name="mlq",
    help="Inspect, explain and audit ML models from your terminal.",
)


@app.command()
def inspect(
    model_path: str = typer.Argument(..., help="Path to trained model (.pkl, .joblib, etc.)"),
    ref: Optional[str] = typer.Option(None, help="Path to reference CSV for drift check"),
    target: str = typer.Option("target", help="Target column name in reference CSV"),
    output: Optional[str] = typer.Option(None, help="Save report as .md or .html (auto-detect)"),
    no_shap: bool = typer.Option(False, help="Skip SHAP computation (for large models)"),
) -> None:
    """Inspect a model: metadata, params, SHAP, and optional drift.
    
    Example:
        mlq inspect model.pkl --ref training_data.csv --target target_col
    """
    # Load model
    console.print(f"[cyan]Loading model from {model_path}...[/cyan]")
    result = load_model(model_path)
    model = result["model"]
    print_success(f"Loaded {Path(model_path).name} ({result['size_kb']:.1f} KB)")
    
    # Extract metadata
    metadata = extract_metadata(model)
    
    # Compute SHAP if not skipped
    shap_data = None
    if not no_shap:
        console.print("[cyan]Computing SHAP feature importance...[/cyan]")
        shap_data = compute_shap(model)
    
    # Compute drift if reference provided
    drift_data = None
    if ref:
        console.print(f"[cyan]Checking drift against {ref}...[/cyan]")
        try:
            ref_df = pd.read_csv(ref)
            drift_data = compute_drift(ref_df, model, target_col=target)
            print_success("Drift computation complete")
        except Exception as e:
            console.print(f"[yellow]Warning: Drift computation failed: {e}[/yellow]")
    
    # Display main panel
    _display_inspection_panel(metadata, shap_data, drift_data)
    
    # Save report if output specified
    if output:
        _save_report(output, metadata, shap_data, drift_data)


@app.command()
def compare(
    model_a: str = typer.Argument(..., help="Path to first model"),
    model_b: str = typer.Argument(..., help="Path to second model"),
    ref: Optional[str] = typer.Option(None, help="Path to reference CSV for drift"),
    target: str = typer.Option("target", help="Target column name"),
) -> None:
    """Compare two models: metadata, params, and SHAP side-by-side.
    
    Example:
        mlq compare model_v1.pkl model_v2.pkl
    """
    console.print("[cyan]Loading models...[/cyan]")
    
    result_a = load_model(model_a)
    result_b = load_model(model_b)
    
    model_a_obj = result_a["model"]
    model_b_obj = result_b["model"]
    
    print_success(f"Loaded both models")
    
    # Extract metadata
    meta_a = extract_metadata(model_a_obj)
    meta_b = extract_metadata(model_b_obj)
    
    # Create comparison table
    table = Table(title="Model Comparison")
    table.add_column("Attribute", style="cyan")
    table.add_column(Path(model_a).name, style="magenta")
    table.add_column(Path(model_b).name, style="magenta")
    
    # Class name
    table.add_row("Class", meta_a["class_name"], meta_b["class_name"])
    
    # Number of features
    table.add_row("n_features", str(meta_a["n_features"]), str(meta_b["n_features"]))
    
    # Number of classes
    n_classes_a = str(meta_a["n_classes"]) if meta_a["n_classes"] else "N/A"
    n_classes_b = str(meta_b["n_classes"]) if meta_b["n_classes"] else "N/A"
    table.add_row("n_classes", n_classes_a, n_classes_b)
    
    # Estimator type
    table.add_row("estimator_type", meta_a["estimator_type"], meta_b["estimator_type"])
    
    # Key hyperparams (top 3 differences)
    console.print(table)
    
    # SHAP comparison
    console.print("\n[cyan]Computing SHAP for both models...[/cyan]")
    shap_a = compute_shap(model_a_obj)
    shap_b = compute_shap(model_b_obj)
    
    if shap_a and shap_b:
        console.print("\n[bold cyan]Top-5 Important Features[/bold cyan]")
        shap_table = Table()
        shap_table.add_column("Feature", style="cyan")
        shap_table.add_column(Path(model_a).name, style="magenta", justify="right")
        shap_table.add_column(Path(model_b).name, style="magenta", justify="right")
        
        for i in range(min(5, len(shap_a), len(shap_b))):
            feat_a, val_a = shap_a[i]
            feat_b, val_b = shap_b[i]
            shap_table.add_row(f"{i+1}. {feat_a}", f"{val_a:.6f}", f"{val_b:.6f}")
        
        console.print(shap_table)


@app.command()
def report(
    model_path: str = typer.Argument(..., help="Path to trained model"),
    output: str = typer.Option("report.html", help="Output file (.html or .md)"),
    ref: Optional[str] = typer.Option(None, help="Path to reference CSV for drift"),
    target: str = typer.Option("target", help="Target column name"),
) -> None:
    """Generate a standalone HTML or Markdown report.
    
    Example:
        mlq report model.pkl --output report.html --ref training_data.csv
    """
    console.print(f"[cyan]Generating report for {model_path}...[/cyan]")
    
    result = load_model(model_path)
    model = result["model"]
    
    # Extract metadata
    metadata = extract_metadata(model)
    
    # Compute SHAP
    shap_data = compute_shap(model)
    
    # Compute drift if reference provided
    drift_data = None
    if ref:
        try:
            ref_df = pd.read_csv(ref)
            drift_data = compute_drift(ref_df, model, target_col=target)
        except Exception as e:
            console.print(f"[yellow]Warning: Drift computation failed: {e}[/yellow]")
    
    # Save report
    _save_report(output, metadata, shap_data, drift_data)


@app.command()
def version() -> None:
    """Print MLQ version and dependencies."""
    import sys
    import sklearn
    import shap
    
    console.print(f"[bold cyan]MLQ {__version__}[/bold cyan]")
    console.print(f"Python {sys.version.split()[0]}")
    console.print(f"scikit-learn {sklearn.__version__}")
    console.print(f"SHAP {shap.__version__}")
    console.print(f"typer 0.12.3")
    console.print(f"rich 13.0+")


def _display_inspection_panel(
    metadata: dict,
    shap_data: Optional[list],
    drift_data: Optional[list],
) -> None:
    """Display the main inspection output as Rich panel and tables."""
    # Main info panel
    lines = []
    lines.append(f"[bold]Class:[/bold] {metadata['class_name']}")
    lines.append(f"[bold]Features:[/bold] {metadata['n_features']}")
    
    if metadata["n_classes"]:
        lines.append(f"[bold]Classes:[/bold] {metadata['n_classes']}")
    
    lines.append(f"[bold]Type:[/bold] {metadata['estimator_type']}")
    
    panel = Panel(
        "\n".join(lines),
        title=metadata["class_name"],
        border_style="blue",
        padding=(1, 2),
    )
    console.print(panel)
    
    # SHAP table
    if shap_data:
        console.print("\n[bold cyan]Feature Importance (SHAP - Top 10)[/bold cyan]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Feature", style="cyan")
        table.add_column("Mean |SHAP|", justify="right")
        table.add_column("Importance", style="green")
        
        max_val = max([v for _, v in shap_data[:10]])
        for i, (feat, val) in enumerate(shap_data[:10], 1):
            bar = format_bar(val, max_val, width=15)
            table.add_row(f"{i:2}. {feat}", f"{val:.6f}", bar)
        
        console.print(table)
    
    # Drift table
    if drift_data:
        console.print("\n[bold cyan]Drift Detection[/bold cyan]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Feature")
        table.add_column("KS Stat", justify="right")
        table.add_column("PSI", justify="right")
        table.add_column("Status")
        
        for drift in drift_data[:10]:
            status_text = drift["status"].upper()
            if drift["status"] == "ok":
                status_style = "[green]"
            elif drift["status"] == "warn":
                status_style = "[yellow]"
            else:
                status_style = "[red]"
            
            table.add_row(
                drift["feature"],
                f"{drift['ks_stat']:.4f}",
                f"{drift['psi']:.4f}",
                f"{status_style}{status_text}[/{status_style.split('[')[1].split(']')[0]}]",
            )
        
        console.print(table)


def _save_report(
    output_path: str,
    metadata: dict,
    shap_data: Optional[list],
    drift_data: Optional[list],
) -> None:
    """Save report to file (auto-detect format by extension)."""
    path = Path(output_path)
    
    if path.suffix.lower() == ".html":
        html_content = generate_html(metadata, shap_data, drift_data)
        path.write_text(html_content)
        print_success(f"HTML report saved to {output_path}")
    elif path.suffix.lower() == ".md":
        md_content = generate_markdown(metadata, shap_data, drift_data)
        path.write_text(md_content)
        print_success(f"Markdown report saved to {output_path}")
    else:
        print_error(f"Unsupported output format: {path.suffix}. Use .html or .md")


if __name__ == "__main__":
    app()
