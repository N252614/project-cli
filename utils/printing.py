from __future__ import annotations
from rich.console import Console
from rich.table import Table

console = Console()

def info(msg: str) -> None:
    """Simple info message."""
    console.print(f"[bold green]INFO:[/bold green] {msg}")

def warn(msg: str) -> None:
    """Simple warning message."""
    console.print(f"[bold yellow]WARN:[/bold yellow] {msg}")

def error(msg: str) -> None:
    """Simple error message."""
    console.print(f"[bold red]ERROR:[/bold red] {msg}")

def table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    """Render a simple table using rich."""
    t = Table(title=title)
    for c in columns:
        t.add_column(c)
    for r in rows:
        t.add_row(*[str(x) for x in r])
    console.print(t)