# How the Backend Works

1. **Routing (`main.py`)**
   - Exposes `/register` for creating users.
   - Exposes `/login` which strictly expects OAuth2 form data (not JSON!) to comply with Swagger standards.
   - Exposes `/posts` (GET for public, POST is protected).

2. **Security (`auth.py`)**
   - Handles password hashing (bcrypt).
   - Generates JWTs using the `python-jose` library.

3. **Database (`models.py` & `schemas.py`)**
   - We defined a One-to-Many relationship (One User has Many Posts).
   - Pydantic validates incoming post creation data and outgoing response structures.
