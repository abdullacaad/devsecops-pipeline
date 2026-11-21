from app import app


def client():
    return app.test_client()


def test_health():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_add():
    response = client().get("/add/2/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 5}
