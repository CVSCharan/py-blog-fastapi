# Architecture: Decoupled API with Auth & Migrations

## Why Decoupled?
We maintain a strict separation of concerns. The backend is a pure REST JSON API built with FastAPI, completely unaware of how the data is rendered. This allows us to serve multiple clients (e.g., web frontend, mobile app) from the same API.

## Authentication Flow
1. Admin POSTs email/password to `/login`.
2. FastAPI hashes the password and compares it to the database using `bcrypt`.
3. If valid, FastAPI signs a JWT using a secret key and returns it.
4. The client attaches this token in the `Authorization: Bearer <token>` header for future protected requests.

## Analytics & Tracking
The backend tracks `views` and `content_type` for each post, and exposes an `/analytics` endpoint to power the frontend admin dashboard with real-time statistics.
