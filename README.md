# Python Blog CMS (Backend)

This is the backend repository for the Phase 3 Blog/CMS project. It introduces JWT Authentication and Database Migrations to the Python stack.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** passlib (bcrypt) + python-jose (JWT)
- **Deployment:** Vercel (via `vercel.json`)

## How to Run Locally

1. Create a PostgreSQL database and paste the connection string in your `.env` file (or just let the fallback SQLite database generate automatically for local testing!).
2. Activate your environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations to create tables:
   ```bash
   alembic upgrade head
   ```
5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
