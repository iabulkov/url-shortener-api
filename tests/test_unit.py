import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/app'))

from models import Link
from schemas import LinkCreate, LinkResponse
from datetime import datetime

class TestUnitModels:
    
    def test_link_generate_short_code(self):
        code = Link.generate_short_code()
        assert len(code) == 6
        assert code.isalnum()
    
    def test_link_generate_short_code_length(self):
        code = Link.generate_short_code(length=8)
        assert len(code) == 8
    
    def test_link_creation(self):
        link = Link(
            original_url="https://example.com",
            short_code="abc123",
            clicks=0,
            is_active=True
        )
        assert link.original_url == "https://example.com"
        assert link.short_code == "abc123"


class TestUnitSchemas:
    
    def test_link_create_schema_valid(self):
        data = {"original_url": "https://example.com"}
        schema = LinkCreate(**data)
        assert str(schema.original_url) == "https://example.com/"
    
    def test_link_create_schema_with_alias(self):
        data = {
            "original_url": "https://example.com",
            "custom_alias": "myalias",
            "expires_at": "2025-12-31T23:59:59"
        }
        schema = LinkCreate(**data)
        assert schema.custom_alias == "myalias"
    
    def test_link_create_schema_invalid_url(self):
        import pytest
        with pytest.raises(ValueError):
            LinkCreate(original_url="not-a-url")
    
    def test_link_response_schema(self):
        data = {
            "original_url": "https://example.com",
            "short_code": "abc123",
            "custom_alias": None,
            "created_at": datetime.now(),
            "expires_at": None,
            "clicks": 0,
            "is_active": True,
            "owner_id": None,
            "short_url": "http://localhost/abc123"
        }
        schema = LinkResponse(**data)
        assert schema.short_code == "abc123"
        assert schema.clicks == 0
