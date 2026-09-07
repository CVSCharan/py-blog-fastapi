from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import re
import time
import logging
import models, schemas, auth
from database import get_db, engine
from starlette.middleware.base import BaseHTTPMiddleware

def generate_slug(title: str, db: Session) -> str:
    base_slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    slug = base_slug
    counter = 1
    while db.query(models.Post).filter(models.Post.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Python Blog API with JWT Auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Logger (Morgan-style)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

class MorganLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
        return response

app.add_middleware(MorganLoggerMiddleware)

# This tells FastAPI where the login route is so it can generate the Swagger UI correctly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- AUTHENTICATION DEPENDENCY ---
# This is like an Express Middleware. Any route that uses `Depends(get_current_user)`
# will require a valid JWT token in the Authorization header.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        from jose import jwt
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

# --- AUTH ROUTES ---

@app.patch("/admin/password")
def change_password(password_data: schemas.PasswordUpdate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """Protected route: update admin password."""
    if not auth.verify_password(password_data.current_password, current_admin.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    current_admin.hashed_password = auth.get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate User
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- BLOG POST ROUTES ---

from typing import Optional, List
from fastapi import Query
from sqlalchemy import func

@app.get("/posts", response_model=schemas.PostPaginatedResponse)
def get_posts(q: Optional[str] = None, tags: List[str] = Query(default=[]), page: int = Query(default=1, ge=1), size: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_db)):
    """Public route: anyone can view posts, optionally filtered by multiple tags (AND logic) with pagination."""
    query = db.query(models.Post)
    if q:
        query = query.filter(models.Post.title.ilike(f"%{q}%"))
    if tags:
        for tag in tags:
            query = query.filter(models.Post.tags.any(models.Tag.name == tag))
            
    total = query.count()
    pages = (total + size - 1) // size
    posts = query.order_by(models.Post.id.desc()).offset((page - 1) * size).limit(size).all()
    
    return {
        "items": posts,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Public route: fetch a specific post."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/posts/slug/{slug}", response_model=schemas.PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """Public route: fetch a specific post by slug and increment views."""
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    post.views += 1
    db.commit()
    db.refresh(post)
    return post

@app.post("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """Protected route: only logged in admins can create posts."""
    slug = generate_slug(post.title, db)
    new_post = models.Post(title=post.title, slug=slug, content=post.content, content_type=post.content_type, author_id=current_admin.id)
    
    # Process tags
    if post.tags:
        for tag_name in post.tags:
            tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.add(tag)
            new_post.tags.append(tag)
            
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.patch("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """Protected route: update an existing post."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    if post_update.title is not None:
        db_post.title = post_update.title
        # Re-generate slug if title changes? We will keep it simple and preserve existing slugs unless we want to change it.
    if post_update.content is not None:
        db_post.content = post_update.content
    if post_update.content_type is not None:
        db_post.content_type = post_update.content_type
        
    if post_update.tags is not None:
        db_post.tags.clear()
        for tag_name in post_update.tags:
            tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.add(tag)
            db_post.tags.append(tag)
            
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """Protected route: delete an existing post."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}

@app.get("/tags", response_model=list[schemas.TagCountResponse])
def get_tags(db: Session = Depends(get_db)):
    """Public route: get all tags with their post counts."""
    results = db.query(
        models.Tag.id,
        models.Tag.name,
        func.count(models.post_tags.c.post_id).label("count")
    ).join(
        models.post_tags, models.Tag.id == models.post_tags.c.tag_id
    ).group_by(
        models.Tag.id
    ).all()
    
    tags_with_counts = [{"id": r[0], "name": r[1], "count": r[2]} for r in results]
    return tags_with_counts

@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """Protected route: get analytics for the dashboard."""
    total_posts = db.query(models.Post).count()
    total_views = db.query(func.sum(models.Post.views)).scalar() or 0
    total_tags = db.query(models.Tag).count()
    
    return {
        "total_posts": total_posts,
        "total_views": total_views,
        "total_tags": total_tags
    }
