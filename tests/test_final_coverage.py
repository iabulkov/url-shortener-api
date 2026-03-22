import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))
os.environ["PYTEST"] = "true"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

class TestFinalCoverage:
    
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
    
    def test_links_test(self):
        response = client.get("/links/test")
        assert response.status_code == 200
        assert response.json()["message"] == "Links router is working"
    
    def test_create_short_link(self):
        response = client.post("/links/shorten", json={"original_url": "https://google.com"})
        assert response.status_code == 200
        assert "short_code" in response.json()
    
    def test_create_short_link_with_alias(self):
        response = client.post("/links/shorten", json={
            "original_url": "https://github.com",
            "custom_alias": "github123"
        })
        assert response.status_code == 200
    
    def test_redirect(self):
        create = client.post("/links/shorten", json={"original_url": "https://example.com"})
        short_code = create.json()["short_code"]
        response = client.get(f"/{short_code}", follow_redirects=False)
        assert response.status_code == 307
    
    def test_redirect_nonexistent(self):
        response = client.get("/nonexistent123", follow_redirects=False)
        # Ваш API может возвращать 307 (редирект на example.com) или 404
        # Проверяем что это не 200
        assert response.status_code != 200
    
    def test_get_stats(self):
        create = client.post("/links/shorten", json={"original_url": "https://example.com"})
        short_code = create.json()["short_code"]
        response = client.get(f"/links/{short_code}/stats")
        assert response.status_code == 200
        assert response.json()["short_code"] == short_code
    
    def test_search_links(self):
        client.post("/links/shorten", json={"original_url": "https://search-test.com"})
        response = client.get("/links/search?original_url=search-test")
        assert response.status_code == 200
    
    def test_update_link(self):
        create = client.post("/links/shorten", json={"original_url": "https://old.com"})
        short_code = create.json()["short_code"]
        response = client.put(f"/links/{short_code}", json={"original_url": "https://new.com"})
        assert response.status_code == 200
    
    def test_delete_link(self):
        create = client.post("/links/shorten", json={"original_url": "https://delete.com"})
        short_code = create.json()["short_code"]
        response = client.delete(f"/links/{short_code}")
        assert response.status_code == 200
    
    def test_get_popular_links(self):
        response = client.get("/links/popular/top?limit=5")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
