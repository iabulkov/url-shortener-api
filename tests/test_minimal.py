import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))
os.environ["PYTEST"] = "true"

from main import app
from database import Base, engine, get_db
from models import User, Link
from auth import get_password_hash
from sqlalchemy.orm import Session

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAPI:
    
    def test_root_endpoint(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        response = client.get("/")
        assert response.status_code == 200
        assert "URL Shortener API" in response.text
    
    def test_test_endpoint(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        response = client.get("/links/test")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Links router is working"
        assert data["db_check"] == True
    
    def test_create_short_link(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        response = client.post("/links/shorten", json={"original_url": "https://www.google.com"})
        assert response.status_code == 200
        data = response.json()
        assert "short_code" in data
        assert data["original_url"].rstrip('/') == "https://www.google.com"
    
    def test_create_short_link_with_alias(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        response = client.post(
            "/links/shorten",
            json={"original_url": "https://www.github.com", "custom_alias": "github123"}
        )
        assert response.status_code == 200
        data = response.json()
        alias = data.get("custom_alias") or data.get("short_code")
        assert alias == "github123", f"Expected 'github123', got '{alias}'"
    
    def test_register_user(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        response = client.post(
            "/auth/register",
            json={"username": "testuser2", "email": "test2@example.com", "password": "pass123"}
        )
        assert response.status_code == 200, f"Registration failed: {response.text}"
        data = response.json()
        assert data["username"] == "testuser2"
    
    def test_login(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        reg = client.post("/auth/register", json={"username": "testuser3", "email": "test3@example.com", "password": "pass123"})
        assert reg.status_code == 200, f"Registration failed: {reg.text}"
        
        response = client.post("/auth/token", data={"username": "testuser3", "password": "pass123"})
        assert response.status_code == 200, f"Login failed: {response.text}"
        assert "access_token" in response.json()
    
    def test_get_current_user(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        reg = client.post("/auth/register", json={"username": "testuser4", "email": "test4@example.com", "password": "pass123"})
        assert reg.status_code == 200
        
        login = client.post("/auth/token", data={"username": "testuser4", "password": "pass123"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "testuser4"
    
    def test_search_links(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        client.post("/links/shorten", json={"original_url": "https://www.google.com"})
        response = client.get("/links/search?original_url=google")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.json()["total"] >= 1
