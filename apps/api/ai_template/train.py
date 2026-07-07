"""Mocked training with Rich progress."""

import pickle
import time
from pathlib import Path

import numpy as np
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_model(name: str, epochs: int = 50) -> dict:
    """Run mocked training, write artifact, return metrics."""
    weights = np.random.randn(10, 10).tolist()
    metrics = {"accuracy": 0.0, "loss": 1.0}

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(f"Training {name}", total=epochs)
        for epoch in range(epochs):
            time.sleep(0.08)
            metrics["accuracy"] = min(0.95, 0.5 + (epoch / epochs) * 0.45)
            metrics["loss"] = max(0.05, 1.0 - (epoch / epochs) * 0.95)
            progress.update(task, advance=1)

    artifact_path = MODELS_DIR / f"{name}.pkl"
    artifact = {"name": name, "weights": weights, "metrics": metrics}
    with open(artifact_path, "wb") as f:
        pickle.dump(artifact, f)

    return {"name": name, "artifact_path": str(artifact_path), "metrics": metrics}
