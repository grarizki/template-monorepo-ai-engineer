"""Model versioning harness - end-to-end version lifecycle tests."""

import pytest
from fastapi.testclient import TestClient

from ai_template.server import app
from ai_template.train import train_model

client = TestClient(app)


@pytest.fixture(scope="module")
def trained_model():
    return train_model("versioning_test", epochs=20)


@pytest.fixture(scope="module")
def model_id(trained_model):
    name = f"versioning_test_{trained_model['name']}"
    r = client.get("/api/v1/models/")
    for m in r.json():
        if m["name"] == name:
            return m["id"]
    r = client.post(
        "/api/v1/models/",
        json={"name": name, "description": "versioning test model"},
    )
    assert r.status_code == 201
    return r.json()["id"]


@pytest.fixture(scope="module")
def version_ids(model_id):
    r1 = client.post(
        f"/api/v1/models/{model_id}/versions/",
        json={"version": "v1.0.0", "metrics": {"accuracy": 0.85, "loss": 0.15}},
    )
    r2 = client.post(
        f"/api/v1/models/{model_id}/versions/",
        json={"version": "v1.1.0", "metrics": {"accuracy": 0.92, "loss": 0.08}},
    )
    return r1.json()["id"], r2.json()["id"]


class TestVersionCRUD:
    def test_create_version_v1(self, model_id, version_ids):
        v1_id, _ = version_ids
        r = client.get(f"/api/v1/models/{model_id}/versions/{v1_id}")
        assert r.status_code == 200
        assert r.json()["version"] == "v1.0.0"
        assert r.json()["model_id"] == model_id
        assert r.json()["metrics"]["accuracy"] == 0.85

    def test_create_version_v2(self, model_id, version_ids):
        _, v2_id = version_ids
        r = client.get(f"/api/v1/models/{model_id}/versions/{v2_id}")
        assert r.status_code == 200
        assert r.json()["version"] == "v1.1.0"

    def test_list_versions(self, model_id, version_ids):
        r = client.get(f"/api/v1/models/{model_id}/versions/")
        assert r.status_code == 200
        assert len(r.json()) >= 2

    def test_get_version(self, model_id, version_ids):
        v1_id, _ = version_ids
        r = client.get(f"/api/v1/models/{model_id}/versions/{v1_id}")
        assert r.status_code == 200
        assert r.json()["id"] == v1_id

    def test_delete_version(self, model_id, version_ids):
        v1_id, _ = version_ids
        r = client.delete(f"/api/v1/models/{model_id}/versions/{v1_id}")
        assert r.status_code == 204

    def test_get_deleted_version_404(self, model_id, version_ids):
        v1_id, _ = version_ids
        r = client.get(f"/api/v1/models/{model_id}/versions/{v1_id}")
        assert r.status_code == 404


class TestVersionEdgeCases:
    def test_version_nonexistent_model(self):
        r = client.post(
            "/api/v1/models/9999/versions/",
            json={"version": "v1.0.0"},
        )
        assert r.status_code == 404

    def test_list_versions_nonexistent_model(self):
        r = client.get("/api/v1/models/9999/versions/")
        assert r.status_code == 404

    def test_delete_nonexistent_version(self, model_id):
        r = client.delete(f"/api/v1/models/{model_id}/versions/9999")
        assert r.status_code == 404
