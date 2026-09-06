from pydantic import BaseModel, EmailStr
from typing import List

# --- USERS ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# --- POSTS ---
class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True

# --- TOKENS ---
class Token(BaseModel):
    access_token: str
    token_type: str
