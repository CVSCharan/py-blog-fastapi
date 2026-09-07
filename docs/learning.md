# Learning Curve & Concepts

## Raw Bcrypt vs Passlib
While `passlib` is a common wrapper in Python, it has been deprecated and poses issues with newer Python versions (3.13+). We switched to using the `bcrypt` library directly (`bcrypt<4.0.0`) to handle password hashing and verification securely.

## python-jose vs jsonwebtoken
In Node, `jsonwebtoken` is the standard for signing/verifying JWTs. In Python, `python-jose` (JavaScript Object Signing and Encryption) provides the exact same functionality with `jwt.encode()` and `jwt.decode()`.

## Alembic vs Raw Migrations
While Alembic is powerful for tracking schema changes, sometimes rapid prototyping requires simple Python scripts to execute raw DDL (like `ALTER TABLE`). We use a mix of Alembic for core structure and scratch scripts for rapid data migrations.
