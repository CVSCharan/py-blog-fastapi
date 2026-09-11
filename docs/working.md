# How the Backend Works

1. **Routing (`main.py`)**
   - Exposes `/login` which expects OAuth2 form data to comply with Swagger standards.
   - Exposes `/posts` (GET for public listing, POST is protected for creating).
   - Exposes `/posts/{slug}` (GET for retrieving a specific post by its SEO-friendly slug).
   - Exposes `/analytics` for dashboard statistics.
   - Exposes `/admin/password` for updating credentials.

2. **Security (`auth.py`)**
   - Handles password hashing natively with `bcrypt`.
   - Generates JWTs using the `python-jose` library.
   - Registration is intentionally disabled to restrict blog posting to authorized admins only.

3. **Database (`models.py` & `schemas.py`)**
   - Defines relationships between Users, Posts, and Tags.
   - Automatically tracks page `views` and uses `published_at` to handle publication dates.
   - Slugs are automatically generated upon post creation, ensuring unique, URL-friendly identifiers.
   - Pydantic models strictly validate incoming data and define outgoing response structures.
