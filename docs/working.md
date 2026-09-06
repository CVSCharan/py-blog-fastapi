# How the Backend Works

1. **Routing (`main.py`)**
   - Exposes `/login` which expects OAuth2 form data to comply with Swagger standards.
   - Exposes `/posts` (GET for public listing, POST is protected for creating).
   - Exposes `/posts/{slug}` (GET for retrieving a specific post by its SEO-friendly slug).

2. **Security (`auth.py`)**
   - Handles password hashing (bcrypt).
   - Generates JWTs using the `python-jose` library.
   - Registration is intentionally disabled to restrict blog posting to authorized admins only.

3. **Database (`models.py` & `schemas.py`)**
   - Defined relationships between Users, Posts, and Tags.
   - Slugs are automatically generated upon post creation, ensuring unique, URL-friendly identifiers.
   - Pydantic models strictly validate incoming data and define outgoing response structures.
