import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))

class TestLinks:
    
    def test_create_short_link_anonymous(self, client):
        response = client.post("/links/shorten", json={"original_url": "https://www.google.com"})
        assert response.status_code == 200
        assert "short_code" in response.json()
    
    def test_create_short_link_with_custom_alias(self, client, auth_headers):
        response = client.post(
            "/links/shorten",
            json={"original_url": "https://www.github.com", "custom_alias": "mygithub"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["custom_alias"] == "mygithub"
    
    def test_create_short_link_duplicate_alias(self, client, auth_headers, test_link):
        response = client.post(
            "/links/shorten",
            json={"original_url": "https://www.google.com", "custom_alias": "test123"},
            headers=auth_headers
        )
        assert response.status_code == 400
    
    def test_redirect_to_original(self, client, test_link):
        response = client.get(f"/{test_link.short_code}", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == test_link.original_url
    
    def test_redirect_nonexistent(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_get_link_stats(self, client, test_link):
        response = client.get(f"/links/{test_link.short_code}/stats")
        assert response.status_code == 200
        assert response.json()["short_code"] == test_link.short_code
    
    def test_update_link(self, client, auth_headers, test_link):
        response = client.put(
            f"/links/{test_link.short_code}",
            json={"original_url": "https://www.updated.com"},
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_delete_link(self, client, auth_headers, test_link):
        response = client.delete(f"/links/{test_link.short_code}", headers=auth_headers)
        assert response.status_code == 200
    
    def test_search_links(self, client, test_link):
        response = client.get(f"/links/search?original_url={test_link.original_url}")
        assert response.status_code == 200
        assert response.json()["total"] >= 1
