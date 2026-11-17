
import sqlite3
import hashlib
import secrets
import hmac
import json

DB_NAME = "movie_users.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add columns to support individual user preferences
    cursor.execute("PRAGMA table_info(user_preferences)")
    columns = [column[1] for column in cursor.fetchall()]

    new_columns = {
        "liked_movies": "TEXT DEFAULT '[]'",
        "disliked_movies": "TEXT DEFAULT '[]'",
        "movie_ratings": "TEXT DEFAULT '{}'"
    }

    for column, definition in new_columns.items():
        if column not in columns:
            cursor.execute(
                f"ALTER TABLE user_preferences ADD COLUMN {column} {definition}"
            )

    # Keep only one preference record per user
    cursor.execute("""
        DELETE FROM user_preferences
        WHERE preference_id NOT IN (
            SELECT MIN(preference_id)
            FROM user_preferences
            GROUP BY user_id
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_user_preferences_user_id
        ON user_preferences(user_id)
    """)


    # Add password columns to an existing users table
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "password_hash" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN password_hash TEXT"
        )

    if "password_salt" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN password_salt TEXT"
        )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            preferred_genres TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    ).hex()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password_hash, password_salt)
            VALUES (?, ?, ?)
        """, (username, password_hash, salt))

        conn.commit()
        conn.close()

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username already exists."


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, password_hash, password_salt
        FROM users
        WHERE username = ?
    """, (username.strip(),))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    user_id, stored_hash, salt = user

    if not stored_hash or not salt:
        return None

    entered_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    ).hex()

    if hmac.compare_digest(entered_hash, stored_hash):
        return user_id

    return None

def load_user_preferences(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT preferred_genres, liked_movies,
               disliked_movies, movie_ratings
        FROM user_preferences
        WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "preferred_genres": [],
            "liked_movies": [],
            "disliked_movies": [],
            "movie_ratings": {}
        }

    return {
        "preferred_genres": json.loads(row[0] or "[]"),
        "liked_movies": json.loads(row[1] or "[]"),
        "disliked_movies": json.loads(row[2] or "[]"),
        "movie_ratings": json.loads(row[3] or "{}")
    }


def save_user_preferences(user_id, preferences):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_preferences (
            user_id, preferred_genres,
            liked_movies, disliked_movies, movie_ratings
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(user_id) DO UPDATE SET
            preferred_genres = excluded.preferred_genres,
            liked_movies = excluded.liked_movies,
            disliked_movies = excluded.disliked_movies,
            movie_ratings = excluded.movie_ratings
    """, (
        user_id,
        json.dumps(preferences["preferred_genres"]),
        json.dumps(preferences["liked_movies"]),
        json.dumps(preferences["disliked_movies"]),
        json.dumps(preferences["movie_ratings"])
    ))

    conn.commit()
    conn.close()