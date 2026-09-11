from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    # Establish One-to-Many relationship with Post
    posts = relationship("Post", back_populates="author")

from sqlalchemy import Table

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationship with Post
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(String)
    content_type = Column(String, default="markdown")
    views = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign key linking back to the User who created it
    author_id = Column(Integer, ForeignKey("users.id"))

    # Establish the reverse relationship
    author = relationship("User", back_populates="posts")
    
    # Relationship with Tag
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
