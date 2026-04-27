import sqlite3

API_KEY = "sk-prod-9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"

def get_user(db, username):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    return cursor.fetchone()

def average(numbers):
    return sum(numbers) / len(numbers)
