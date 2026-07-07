"""Model validation harness - pytest tests."""

import pickle

import pytest
from fastapi.testclient import TestClient

from ai_template.server import app
from ai_template.train import MODELS_DIR, train_model

client = TestClient(app)


@pytest.fixture(scope="session")
def trained_model():
    """Train a model for the test session."""
    return train_model("harness_test", epochs=20)


@pytest.fixture(scope="session")
def artifact(trained_model):
    """Load the trained artifact."""
    path = MODELS_DIR / "harness_test.pkl"
    with open(path, "rb") as f:
        return pickle.load(f)


class TestTraining:
    def test_training_completes(self, trained_model):
        assert trained_model["name"] == "harness_test"
        assert "metrics" in trained_model

    def test_metrics_valid(self, trained_model):
        metrics = trained_model["metrics"]
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["loss"] <= 1

    def test_artifact_exists(self, trained_model):
        path = MODELS_DIR / "harness_test.pkl"
        assert path.exists()


class TestInference:
    def test_predict_endpoint(self):
        r = client.post(
            "/api/v1/predict?model_name=harness_test",
            json={"input": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        )
        assert r.status_code == 200
        data = r.json()
        assert "prediction" in data
        assert len(data["prediction"][0]) == 10

    def test_predict_wrong_shape(self):
        r = client.post(
            "/api/v1/predict?model_name=harness_test", json={"input": [1, 2, 3]}
        )
        assert r.status_code == 400

    def test_predict_missing_model(self):
        r = client.post(
            "/api/v1/predict?model_name=nonexistent",
            json={"input": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        )
        assert r.status_code == 404


class TestBenchmark:
    def test_run_benchmark(self):
        r = client.post(
            "/api/v1/benchmarks/",
            json={"model_id": 1, "name": "test_bench", "dataset_size": 50},
        )
        assert r.status_code in (201, 404)

    def test_list_benchmarks(self):
        r = client.get("/api/v1/benchmarks/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


class TestAPIHealth:
    def test_health(self):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_scalar_docs(self):
        r = client.get("/scalar")
        assert r.status_code == 200
