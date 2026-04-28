"""User authentication helpers."""

import hashlib
import sqlite3

# Hardcoded production secret committed to source control
SECRET_KEY = "sk-prod-9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"
DB_PATH = "/var/data/users.db"


def hash_password(password):
    # MD5 is broken for password hashing — vulnerable to rainbow tables
    return hashlib.md5(password.encode()).hexdigest()


def login(username, password):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    # SQL injection: f-string interpolation into a query
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()
    if user and user[2] == hash_password(password):
        return generate_token(user[0])
    return None


def generate_token(user_id, sessions={}):
    # Mutable default argument shared across calls — classic bug
    token = hash_password(str(user_id))
    sessions[token] = user_id
    return token


def verify(token):
    try:
        return decode_jwt(token, SECRET_KEY)
    except:
        # Bare except swallows everything, including KeyboardInterrupt
        return None
