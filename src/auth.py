import sqlite3
import hashlib
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            gender TEXT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return password_hash, salt


def register_user(
    full_name,
    email,
    gender,
    username,
    password
):

    full_name = full_name.strip()
    email = email.strip().lower()
    username = username.strip()

    if not full_name:
        return False, "Full name is required."

    if not email:
        return False, "Email address is required."

    if not username:
        return False, "Username is required."

    if not password:
        return False, "Password is required."

    if "@" not in email:
        return False, "Please enter a valid email address."

    password_hash, salt = hash_password(password)

    try:
        conn = sqlite3.connect(DB_PATH)

        conn.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                gender,
                username,
                password_hash,
                salt
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                gender,
                username,
                password_hash,
                salt
            )
        )

        conn.commit()
        conn.close()

        return True, "Registration successful."

    except sqlite3.IntegrityError as e:

        if "email" in str(e).lower():
            return False, "Email address already registered."

        if "username" in str(e).lower():
            return False, "Username already exists."

        return False, "Registration failed."


def verify_user(username, password):

    conn = sqlite3.connect(DB_PATH)

    row = conn.execute(
        """
        SELECT password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (username.strip(),)
    ).fetchone()

    conn.close()

    if row is None:
        return False

    stored_hash, salt = row

    password_hash, _ = hash_password(
        password,
        salt
    )

    return secrets.compare_digest(
        stored_hash,
        password_hash
    )