from pydantic import BaseModel, EmailStr
from typing import List

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
    tags: List[str] = [] # Optional list of tag names

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str | None = None
    content: str
    author_id: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: List[str] | None = None

# --- TOKENS ---
class Token(BaseModel):
    access_token: str
    token_type: str
