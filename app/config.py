import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security & Sessions
SECRET_KEY = os.getenv("SECRET_KEY", "biswa-cyber-vault-quantum-teal-secret-key-2026-v1")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Dual Database Segregation
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database 1: User authentication, credentials, sessions, and visitor audit logs
USERS_DB_PATH = DATA_DIR / "users_auth.db"

# Database 2: Personal footprint dossier, public records, repositories, and AI knowledge
DOSSIER_DB_PATH = DATA_DIR / "dossier_data.db"

# Target Subject Profile Info
SUBJECT_NAME = "Biswajeet Shadangi"
SUBJECT_HANDLE = "Pshypher-Techie"
SUBJECT_EMAIL = "biswajeetshadangi98@gmail.com"
SUBJECT_LOCATION = "Odisha, India"

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

