import uuid

from conftest import client


class TestStocks:
    def test_create_stock(self):
        ticker = f"T{uuid.uuid4().hex[:4].upper()}"
        r = client.post(
            "/stocks/",
            json={
                "ticker": ticker,
                "name": "Test Corp",
                "sector": "Tech",
                "current_price": 100.0,
            },
        )
        assert r.status_code == 201
        data = r.json()
        assert data["ticker"] == ticker
        assert data["name"] == "Test Corp"

    def test_create_stock_duplicate(self):
        ticker = f"D{uuid.uuid4().hex[:4].upper()}"
        client.post("/stocks/", json={"ticker": ticker, "name": "Dup Corp"})
        r = client.post("/stocks/", json={"ticker": ticker, "name": "Dup Corp 2"})
        assert r.status_code == 400

    def test_get_stock_by_ticker(self):
        ticker = f"G{uuid.uuid4().hex[:4].upper()}"
        client.post("/stocks/", json={"ticker": ticker, "name": "Get Corp"})
        r = client.get(f"/stocks/{ticker}")
        assert r.status_code == 200
        assert r.json()["ticker"] == ticker

    def test_get_stock_not_found(self):
        r = client.get("/stocks/NOPE")
        assert r.status_code == 404

    def test_list_stocks(self):
        r = client.get("/stocks/")
        assert r.status_code == 200
        data = r.json()
        assert "stocks" in data
        assert "total" in data

    def test_update_stock(self):
        ticker = f"U{uuid.uuid4().hex[:4].upper()}"
        client.post("/stocks/", json={"ticker": ticker, "name": "Old Name"})
        r = client.patch(f"/stocks/{ticker}", json={"name": "New Name"})
        assert r.status_code == 200
        assert r.json()["name"] == "New Name"

    def test_delete_stock(self):
        ticker = f"X{uuid.uuid4().hex[:4].upper()}"
        client.post("/stocks/", json={"ticker": ticker, "name": "Delete Me"})
        r = client.delete(f"/stocks/{ticker}")
        assert r.status_code == 204

    def test_seed_stocks(self):
        r = client.post("/stocks/seed")
        assert r.status_code == 200
