import sqlite3
import hashlib
import os
import secrets
from datetime import datetime, timezone
from app.config import USERS_DB_PATH

def get_users_db_connection():
    conn = sqlite3.connect(USERS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    # Using PBKDF2 HMAC SHA-256 with 100,000 iterations for secure key derivation
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return dk.hex(), salt

def verify_password(password: str, salt: str, password_hash: str) -> bool:
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return secrets.compare_digest(dk.hex(), password_hash)

def init_users_db():
    conn = get_users_db_connection()
    cursor = conn.cursor()
    
    # Table 1: Registered viewers and admin users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'viewer',
        created_at TEXT NOT NULL,
        last_login_at TEXT
    )
    """)

    # Table 2: Active authenticated sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        ip_address TEXT,
        user_agent TEXT,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Table 3: Security & Visitor Audit Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        action TEXT NOT NULL,
        details TEXT,
        ip_address TEXT,
        user_agent TEXT,
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()

    # Seed default Admin and Guest accounts if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        now = datetime.now(timezone.utc).isoformat()
        
        # Admin: biswa / Biswa@2026
        admin_hash, admin_salt = hash_password("Biswa@2026")
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, salt, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("biswa", "biswajeetshadangi98@gmail.com", admin_hash, admin_salt, "admin", now)
        )
        
        # Demo Viewer: guest / Guest@2026
        guest_hash, guest_salt = hash_password("Guest@2026")
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, salt, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("guest", "visitor@cybervault.internal", guest_hash, guest_salt, "viewer", now)
        )
        conn.commit()
    conn.close()

def create_user(username: str, email: str, password: str, role: str = "viewer") -> dict:
    conn = get_users_db_connection()
    cursor = conn.cursor()
    pwd_hash, salt = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, salt, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (username.strip().lower(), email.strip().lower(), pwd_hash, salt, role, now)
        )
        user_id = cursor.lastrowid
        conn.commit()
        return {"id": user_id, "username": username, "email": email, "role": role}
    finally:
        conn.close()

def get_user_by_username(username: str):
    conn = get_users_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username.strip().lower(), username.strip().lower()))
    user = cursor.fetchone()
    conn.close()
    return user

def log_audit(action: str, username: str = None, user_id: int = None, details: str = None, ip_address: str = None, user_agent: str = None):
    conn = get_users_db_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute(
        "INSERT INTO audit_logs (user_id, username, action, details, ip_address, user_agent, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, username, action, details, ip_address, user_agent, now)
    )
    conn.commit()
    conn.close()

def get_recent_audit_logs(limit: int = 20):
    conn = get_users_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return logs

def get_users_stats():
    conn = get_users_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM audit_logs")
    total_audits = cursor.fetchone()[0]
    conn.close()
    return {"total_registered_users": total_users, "total_audit_events": total_audits}

