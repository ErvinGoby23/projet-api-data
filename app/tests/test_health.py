from httpx import Client

def test_health_local():
    with Client(base_url="http://localhost:8000") as c:
        r = c.get("/tst-health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
