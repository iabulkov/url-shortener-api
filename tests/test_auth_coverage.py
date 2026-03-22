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
from models import User
from auth import get_password_hash

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

class TestAuthCoverage:
    """Тесты для аутентификации"""
    
    def setup_method(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    
    def test_register_success(self):
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "email": "new@example.com", "password": "pass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
    
    def test_register_duplicate_username(self):
        client.post("/auth/register", json={"username": "duplicate", "email": "dup1@example.com", "password": "pass123"})
        response = client.post(
            "/auth/register",
            json={"username": "duplicate", "email": "dup2@example.com", "password": "pass123"}
        )
        assert response.status_code == 400
    
    def test_register_duplicate_email(self):
        client.post("/auth/register", json={"username": "user1", "email": "same@example.com", "password": "pass123"})
        response = client.post(
            "/auth/register",
            json={"username": "user2", "email": "same@example.com", "password": "pass123"}
        )
        assert response.status_code == 400
    
    def test_login_success(self):
        client.post("/auth/register", json={"username": "loginuser", "email": "login@example.com", "password": "pass123"})
        response = client.post("/auth/token", data={"username": "loginuser", "password": "pass123"})
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_wrong_password(self):
        client.post("/auth/register", json={"username": "wrongpass", "email": "wrong@example.com", "password": "pass123"})
        response = client.post("/auth/token", data={"username": "wrongpass", "password": "wrongpass"})
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self):
        response = client.post("/auth/token", data={"username": "nonexistent", "password": "pass123"})
        assert response.status_code == 401
    
    def test_get_current_user(self):
        client.post("/auth/register", json={"username": "meuser", "email": "me@example.com", "password": "pass123"})
        login = client.post("/auth/token", data={"username": "meuser", "password": "pass123"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "meuser"
    
    def test_get_current_user_unauthorized(self):
        response = client.get("/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
