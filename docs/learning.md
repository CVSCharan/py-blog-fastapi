# Learning Curve & Concepts

## Passlib vs Bcrypt (Node)
In Node, you usually just install `bcrypt`. In Python, the standard is `passlib`, which is a higher-level wrapper that can handle multiple hashing algorithms (though we configured it to use bcrypt).

## python-jose vs jsonwebtoken
In Node, `jsonwebtoken` is the standard for signing/verifying JWTs. In Python, `python-jose` (JavaScript Object Signing and Encryption) provides the exact same functionality with `jwt.encode()` and `jwt.decode()`.

## Alembic vs Prisma Migrations
Alembic is the most common migration tool for SQLAlchemy. 
- `alembic init alembic` sets up the migration environment.
- `alembic revision --autogenerate -m "msg"` compares your `models.py` to the actual database and generates a migration script.
- `alembic upgrade head` runs the migrations against the database.
