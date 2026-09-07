# CVS Blogs - Backend API

A pure REST JSON API built with FastAPI, SQLAlchemy, and Neon PostgreSQL. It handles authentication (JWT), data persistence, analytics, and core business logic for the CVS Blogs application.

## Tech Stack
- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **SQLAlchemy**: The Python SQL toolkit and Object Relational Mapper (ORM).
- **Neon PostgreSQL**: A serverless Postgres database.
- **JWT (JSON Web Tokens)**: Used for secure, stateless authentication.
- **bcrypt**: Used directly for secure password hashing.

## Prerequisites
- Python 3.9+
- A Neon PostgreSQL database URL (or any local Postgres).

## Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary "bcrypt<4.0.0" python-jose pydantic[email] python-dotenv
   ```
3. Configure your `.env` file:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>
   SECRET_KEY=your_secret_key
   ```
4. Run the backend server (runs on `http://127.0.0.1:8000`):
   ```bash
   uvicorn main:app --reload
   ```

## Features
- **Authentication**: JWT-based authentication for admin users.
- **Database**: PostgreSQL integration with SQLAlchemy ORM.
- **SEO-Friendly URLs**: Automatically generates unique URL slugs for blog posts.
- **Analytics**: Built-in endpoint for fetching platform analytics (total posts, total views, unique tags).
- **Security**: Direct `bcrypt` hashing for password updates and verification.

## Database Management
To populate the database with an initial admin user and tags:
```bash
python ../scratch/seed.py
```
To seed demo articles:
```bash
python ../scratch/seed_new_articles.py
```
