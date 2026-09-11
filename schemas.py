from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- USERS ---
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool = False

    class Config:
        from_attributes = True

# --- TAGS ---
class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TagCountResponse(BaseModel):
    id: int
    name: str
    count: int

# --- POSTS ---
class PostCreate(BaseModel):
    title: str
    content: str
    content_type: str = "markdown"
    tags: List[str] = [] # Optional list of tag names
    published_at: Optional[datetime] = None

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str | None = None
    content: str
    content_type: str
    views: int
    published_at: datetime
    author_id: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    content_type: str | None = None
    tags: List[str] | None = None
    published_at: Optional[datetime] = None

class PostPaginatedResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    size: int
    pages: int

# --- TOKENS ---
class Token(BaseModel):
    access_token: str
    token_type: str
