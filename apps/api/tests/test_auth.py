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
        assert r.json()["message"] == "User register success!"

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
        assert r.json()["message"] == "User login success!"

    def test_login_wrong_password(self):
        uid = uuid.uuid4().hex[:8]
        client.post(
            "/auth/register",
            json={"name": "Wrong", "email": f"{uid}@test.com", "password": "correct"},
        )
        r = client.post(
            "/auth/login", json={"email": f"{uid}@test.com", "password": "incorrect"}
        )
        assert r.status_code == 401

    def test_login_nonexistent_user(self):
        r = client.post(
            "/auth/login", json={"email": "nonexistent@test.com", "password": "pass"}
        )
        assert r.status_code == 401
