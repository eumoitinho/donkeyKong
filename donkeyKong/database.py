# database.py
import sqlite3
import hashlib

def initialize_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('game.db')
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        return True  # Registro bem-sucedido
    except sqlite3.IntegrityError:
        return False  # Registro falhou (provavelmente devido a um nome de usuário duplicado)
    finally:
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def update_score(username, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users SET score = ? WHERE username = ?
    ''', (score, username))
    conn.commit()
    conn.close()

def get_score(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT score FROM users WHERE username = ?
    ''', (username,))
    score = cursor.fetchone()
    conn.close()
    return score[0] if score else 0
