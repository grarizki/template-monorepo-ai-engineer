import uuid

from conftest import client


class TestAuth:
    def test_register_user(self):
        uid = uuid.uuid4().hex[:8]
        r = client.post(
            "/auth/register",
            json={
                "name": "Test User",
                "email": f"{uid}@test.com",
                "password": "secret123",
            },
        )
        assert r.status_code == 200

    def test_login_success(self):
        uid = uuid.uuid4().hex[:8]
        client.post(
            "/auth/register",
            json={
                "name": "Login User",
                "email": f"{uid}@test.com",
                "password": "pass123",
            },
        )
        r = client.post(
            "/auth/login", json={"email": f"{uid}@test.com", "password": "pass123"}
        )
        assert r.status_code == 200


class TestProjects:
    def test_crud(self):
        r = client.post(
            "/api/v1/projects/",
            json={"name": f"Proj-{uuid.uuid4().hex[:4]}", "description": "Test"},
        )
        assert r.status_code == 201
        pid = r.json()["id"]
        r = client.get(f"/api/v1/projects/{pid}")
        assert r.status_code == 200
        r = client.delete(f"/api/v1/projects/{pid}")
        assert r.status_code == 204


class TestModels:
    def test_crud(self):
        r = client.post(
            "/api/v1/models/",
            json={
                "name": f"Model-{uuid.uuid4().hex[:4]}",
                "metrics": {"accuracy": 0.9},
            },
        )
        assert r.status_code == 201
        mid = r.json()["id"]
        r = client.get(f"/api/v1/models/{mid}")
        assert r.status_code == 200
        r = client.delete(f"/api/v1/models/{mid}")
        assert r.status_code == 204


class TestDeployments:
    def test_crud(self):
        r = client.post("/api/v1/deployments/", json={"status": "pending"})
        assert r.status_code == 201
        did = r.json()["id"]
        r = client.get(f"/api/v1/deployments/{did}")
        assert r.status_code == 200
        r = client.delete(f"/api/v1/deployments/{did}")
        assert r.status_code == 204


class TestHealth:
    def test_health(self):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
