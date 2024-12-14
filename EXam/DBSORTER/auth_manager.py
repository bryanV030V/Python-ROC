import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize or connect to the local SQLite database
def init_auth_db():
    with sqlite3.connect("auth.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# Function to create an account
def create_account(username, password):
    try:
        hashed_password = generate_password_hash(password, method='sha256')
        with sqlite3.connect("auth.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        return {"success": True, "message": "Account created successfully!"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username already exists."}
    except Exception as e:
        return {"success": False, "message": str(e)}

# Function to log in
def login(username, password):
    try:
        with sqlite3.connect("auth.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            return {"success": True, "message": "Login successful!"}
        else:
            return {"success": False, "message": "Invalid username or password."}
    except Exception as e:
        return {"success": False, "message": str(e)}

# Ensure the database is ready on import
init_auth_db()
