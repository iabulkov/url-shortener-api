import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))

class TestAuth:
    
    def test_register_success(self, client):
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "email": "newuser@example.com", "password": "newpassword"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
    
    def test_register_duplicate_username(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={"username": "testuser", "email": "new@example.com", "password": "password"}
        )
        assert response.status_code == 400
    
    def test_register_duplicate_email(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={"username": "newuser2", "email": "test@example.com", "password": "password"}
        )
        assert response.status_code == 400
    
    def test_login_success(self, client, test_user):
        response = client.post(
            "/auth/token",
            data={"username": "testuser", "password": "testpass"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_wrong_password(self, client, test_user):
        response = client.post(
            "/auth/token",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/auth/token",
            data={"username": "nonexistent", "password": "password"}
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers, test_user):
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
    
    def test_get_current_user_unauthorized(self, client):
        response = client.get("/auth/me")
        assert response.status_code == 401
