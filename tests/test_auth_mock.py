import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))
os.environ["PYTEST"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User

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

class TestAuthMock:
    """Тесты аутентификации с прямым созданием пользователя в БД"""
    
    def setup_method(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    
    def _create_user(self, username, email, password):
        """Создаёт пользователя напрямую в БД"""
        from auth import get_password_hash
        db = TestingSessionLocal()
        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user
    
    def test_register_success(self):
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "email": "new@example.com", "password": "p" * 20}
        )
        assert response.status_code == 200
    
    def test_login_success(self):
        # Создаём пользователя напрямую
        self._create_user("loginuser", "login@example.com", "testpass")
        response = client.post("/auth/token", data={"username": "loginuser", "password": "testpass"})
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_wrong_password(self):
        self._create_user("wrongpass", "wrong@example.com", "correctpass")
        response = client.post("/auth/token", data={"username": "wrongpass", "password": "wrongpass"})
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self):
        response = client.post("/auth/token", data={"username": "nonexistent", "password": "pass"})
        assert response.status_code == 401
    
    def test_get_current_user(self):
        self._create_user("meuser", "me@example.com", "mypass")
        login = client.post("/auth/token", data={"username": "meuser", "password": "mypass"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "meuser"
    
    def test_get_current_user_unauthorized(self):
        response = client.get("/auth/me")
        assert response.status_code == 401
    
    def test_register_duplicate_username(self):
        self._create_user("duplicate", "dup1@example.com", "pass")
        response = client.post(
            "/auth/register",
            json={"username": "duplicate", "email": "dup2@example.com", "password": "pass"}
        )
        assert response.status_code == 400
    
    def test_register_duplicate_email(self):
        self._create_user("user1", "same@example.com", "pass")
        response = client.post(
            "/auth/register",
            json={"username": "user2", "email": "same@example.com", "password": "pass"}
        )
        assert response.status_code == 400
