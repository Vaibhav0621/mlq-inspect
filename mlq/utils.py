"""Shared utilities and Rich console setup."""

from rich.console import Console
from rich.panel import Panel

# Singleton Rich console instance
console = Console()


def print_error(msg: str) -> None:
    """Print error message in a Rich red panel."""
    panel = Panel(
        msg,
        title="Error",
        border_style="red",
        style="red",
    )
    console.print(panel)


def print_success(msg: str) -> None:
    """Print success message in Rich green text."""
    console.print(f"[green]✓ {msg}[/green]")


def format_bar(value: float, max_value: float, width: int = 20) -> str:
    """Return a Unicode block bar string proportional to value/max_value.

    Args:
        value: Current value
        max_value: Maximum value for scaling
        width: Width of bar in characters

    Returns:
        Unicode block bar string (filled blocks + empty blocks)
    """
    if max_value == 0:
        filled = 0
    else:
        filled = int((value / max_value) * width)

    filled = min(filled, width)  # Ensure we don't exceed width
    empty = width - filled
    return "█" * filled + "░" * empty
