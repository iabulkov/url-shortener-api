from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LinkBase(BaseModel):
    original_url: HttpUrl

class LinkCreate(LinkBase):
    custom_alias: Optional[str] = Field(None, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    expires_at: Optional[datetime] = None

class LinkUpdate(BaseModel):
    original_url: HttpUrl

class LinkResponse(LinkBase):
    short_code: str
    custom_alias: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int
    is_active: bool
    owner_id: Optional[int]
    short_url: str

class LinkStats(LinkResponse):
    last_accessed: Optional[datetime]
    days_since_creation: int
    is_expired: bool

class LinkSearchResponse(BaseModel):
    links: list[LinkResponse]
    total: int