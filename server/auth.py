import hashlib
import jwt
import datetime
import sqlite3

class AuthManager:
    SECRET_KEY = "your_secret_key"
    DB_PATH = "users.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.create_users_table()

    def create_users_table(self):
        try:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL
                    )
                """)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_user(self, username, password):
        hashed_password = self.hash_password(password)
        print(f"Adding user {username} with password {hashed_password}")  # Логирование
        try:
            with self.conn:
                self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                print(f"User {username} added successfully")  # Логирование
        except sqlite3.IntegrityError:
            raise Exception(f"User {username} already exists")
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")

    def authenticate(self, username, password):
        user = self.get_user(username)
        if user and self.check_password(password, user[1]):
            return self.generate_token(username)
        raise Exception("Authentication failed")

    def get_user(self, username):
        try:
            with self.conn:
                cursor = self.conn.execute("SELECT username, password FROM users WHERE username = ?", (username,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password, hashed_password):
        return self.hash_password(password) == hashed_password

    def generate_token(self, username):
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return payload["username"]
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
