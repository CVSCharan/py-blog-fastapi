# Architecture: Decoupled with Auth & Migrations

## Why Decoupled Again?
Unlike the URL Shortener (which used SSR), we returned to a Decoupled architecture for this project. Why? Because handling JSON Web Tokens (JWTs) on the frontend is a crucial skill for modern SPA development. We needed a separate frontend client to practice storing and attaching JWTs to API requests.

## Authentication Flow
1. User POSTs email/password to `/login`.
2. FastAPI hashes the password and compares it to the database using `passlib`.
3. If valid, FastAPI signs a JWT using a secret key and returns it.
4. The client attaches this token in the `Authorization: Bearer <token>` header for future requests.
5. FastAPI uses a `Dependency` (`get_current_user`) on protected routes to decode the token and identify the user.

## Database Migrations
Instead of using `Base.metadata.create_all` (which is a hack for simple projects), this project uses **Alembic**. 
Alembic tracks changes to `models.py` and generates migration scripts (like `npx prisma migrate dev`), allowing safe database schema upgrades over time.
