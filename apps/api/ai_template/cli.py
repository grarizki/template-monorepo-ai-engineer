"""Typer CLI for ai-template."""

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(name="ai-cli", help="AI Template CLI")
console = Console()


@app.command()
def create_project(name: str):
    """Scaffold a new project directory."""
    project_dir = Path("projects") / name
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "__init__.py").touch()
    (project_dir / "data").mkdir(exist_ok=True)
    (project_dir / "models").mkdir(exist_ok=True)
    console.print(f"[green]Created project:[/green] {project_dir}")


@app.command()
def train(name: str, epochs: int = 50):
    """Run mocked training with Rich progress."""
    from ai_template.train import train_model

    result = train_model(name, epochs)
    console.print(f"[green]Training complete:[/green] {result['name']}")
    console.print(f"  Artifact: {result['artifact_path']}")
    console.print(f"  Metrics: {result['metrics']}")


@app.command()
def migrate():
    """Run Alembic migrations."""
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    console.print("[green]Migrations applied.[/green]")


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Start FastAPI server."""
    import uvicorn

    console.print(f"[blue]Serving at http://{host}:{port}[/blue]")
    console.print(f"[blue]Scalar docs at http://{host}:{port}/scalar[/blue]")
    uvicorn.run("ai_template.server:app", host=host, port=port, reload=True)


@app.command()
def demo(model: str = "demo_model"):
    """Full demo: train + serve."""
    from ai_template.train import train_model

    console.rule("[bold green]AI Template Demo")

    result = train_model(model)
    console.print(f"\n[green]Model saved:[/green] {result['artifact_path']}")

    console.print("\n[blue]Starting server...[/blue]\n")
    import uvicorn

    uvicorn.run("ai_template.server:app", host="127.0.0.1", port=8000)


@app.command()
def lint():
    """Run ruff check + format."""
    subprocess.run(["ruff", "check", ".", "--fix"], check=True)
    subprocess.run(["ruff", "format", "."], check=True)
    console.print("[green]Lint complete.[/green]")


if __name__ == "__main__":
    app()
