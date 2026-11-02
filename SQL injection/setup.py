# Create database and sample users

import sqlite3
import hashlib
import secrets

from database import get_connection


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000
    )

    return salt, password_hash


def setup_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            salt BLOB NOT NULL
        )
    """)

    salt, password_hash_value = hash_password("DemoPass123!")

    connection.execute("""
        INSERT OR IGNORE INTO users
        (username, password_hash, salt)
        VALUES (?, ?, ?)
    """, ("admin", password_hash_value, salt))

    connection.commit()
    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    setup_database()