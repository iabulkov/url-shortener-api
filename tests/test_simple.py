import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))
os.environ["PYTEST"] = "true"

def test_import():
    from main import app
    assert app is not None
    print("Приложение импортируется")

def test_client():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/")
    print(f"Статус: {response.status_code}")
    assert response.status_code in [200, 404]
    print("Клиент работает")
