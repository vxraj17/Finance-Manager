import sqlite3
import bcrypt
from db import get_connection

def register_user(username, password):
    """Register a new user with hashed password."""

    # Validate inputs
    if not username.strip():
        return False, "❌ Username cannot be empty."
    if not password.strip():
        return False, "❌ Password cannot be empty."

    conn = get_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "❌ Username already exists."

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert into DB
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash),
    )
    conn.commit()
    conn.close()
    return True, "✅ Registration successful!"



def login_user(username, password):
    """Authenticate user and return True if successful."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False, None, "❌ Username not found."

    user_id, password_hash = row

    # Check password
    if bcrypt.checkpw(password.encode('utf-8'), password_hash):
        return True, user_id, "✅ Login successful!"
    else:
        return False, None, "❌ Incorrect password."

