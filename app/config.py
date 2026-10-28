import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security & Sessions
SECRET_KEY = os.getenv("SECRET_KEY", "biswa-cyber-vault-quantum-teal-secret-key-2026-v2")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Dual Database Segregation
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database 1: User authentication, credentials, sessions, and visitor audit logs
USERS_DB_PATH = DATA_DIR / "users_auth.db"

# Database 2: Personal footprint dossier, public records, repositories, and AI knowledge
DOSSIER_DB_PATH = DATA_DIR / "dossier_data.db"

# Verified Subject Identity
SUBJECT_NAME = "BISWAJEET SHADANGI"
SUBJECT_HANDLE = "Pshypher-Techie"
SUBJECT_EMAIL = "biswajeetshadangi98@gmail.com"
SUBJECT_PHONE = "+91 7847881225"
SUBJECT_LOCATION = "Koraput, Odisha, India"
SUBJECT_COLLEGE = "VITAM (Vignan Institute of Technology and Management)"
SUBJECT_UNIVERSITY = "BPUT (Biju Patnaik University of Technology, Odisha)"
SUBJECT_QUALIFICATION = "B.Tech in Computer Science & Engineering (CSE) - 2nd Year"

LINKEDIN_URL = "https://www.linkedin.com/in/biswajeet-shadangi-701590447"
INSTAGRAM_URL = "https://www.instagram.com/_pshypher_12_"
TWITTER_URL = "https://x.com/BISWAJEET140222"
GITHUB_URL = "https://github.com/Pshypher-Techie"

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
