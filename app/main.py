import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from app.config import (
    BASE_DIR, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES,
    USERS_DB_PATH, DOSSIER_DB_PATH
)
from app.database_users import (
    init_users_db, get_user_by_username, verify_password,
    create_user, log_audit, get_recent_audit_logs, get_users_stats
)
from app.database_dossier import (
    init_dossier_db, get_dossier_data, add_custom_footprint, get_dossier_stats
)
from app.security import (
    create_access_token, get_current_user
)
from app.osint_service import perform_full_osint_scan
from app.ai_service import query_ai_dossier

# Initialize dual isolated databases
init_users_db()
init_dossier_db()

app = FastAPI(
    title="CYBER-VAULT :: AI-Powered Intelligence Dossier",
    description="High-security intelligence dashboard displaying verified internet footprint and AI synthesis",
    version="1.0.0"
)

# Mount static directory
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Pydantic Request Models
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class AskAIRequest(BaseModel):
    query: str

class AddRecordRequest(BaseModel):
    platform: str
    identifier: str
    url: str
    category: str
    summary: str

class ScanRequest(BaseModel):
    handle: Optional[str] = None

# Helpers
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

# Root Route: Serves single page HTML
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = BASE_DIR / "templates" / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Cyber-Vault loading...</h1>")

# --- AUTHENTICATION ROUTES (Operates strictly on Database 1: users_auth.db) ---

@app.post("/api/auth/login")
async def login(login_req: LoginRequest, request: Request, response: Response):
    user = get_user_by_username(login_req.username)
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "Unknown")

    if not user or not verify_password(login_req.password, user["salt"], user["password_hash"]):
        log_audit(
            action="LOGIN_FAILED",
            username=login_req.username,
            details="Invalid credentials attempt",
            ip_address=client_ip,
            user_agent=user_agent
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cyber-Vault Authentication Denied: Invalid credentials."
        )

    # Issue cryptographic JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user["username"], "role": user["role"], "id": user["id"]},
        expires_delta=access_token_expires
    )

    # Set secure cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False
    )

    log_audit(
        action="LOGIN_SUCCESS",
        user_id=user["id"],
        username=user["username"],
        details=f"User signed in with role '{user['role']}'",
        ip_address=client_ip,
        user_agent=user_agent
    )

    return {
        "status": "authenticated",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@app.post("/api/auth/register")
async def register(reg_req: RegisterRequest, request: Request):
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "Unknown")

    if len(reg_req.username.strip()) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long.")
    if len(reg_req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    if "@" not in reg_req.email:
        raise HTTPException(status_code=400, detail="Invalid email format.")

    existing = get_user_by_username(reg_req.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username or email is already registered.")

    new_user = create_user(reg_req.username, reg_req.email, reg_req.password, role="viewer")
    
    log_audit(
        action="REGISTER_USER",
        user_id=new_user["id"],
        username=new_user["username"],
        details="New viewer account created in Database 1",
        ip_address=client_ip,
        user_agent=user_agent
    )

    return {
        "status": "success",
        "message": "Viewer account initialized successfully. You may now enter the vault.",
        "user": new_user
    }

@app.post("/api/auth/logout")
async def logout(response: Response, request: Request, current_user: dict = Depends(get_current_user)):
    response.delete_cookie("access_token")
    client_ip = get_client_ip(request)
    log_audit(
        action="LOGOUT",
        user_id=current_user["id"],
        username=current_user["username"],
        details="Session terminated by user",
        ip_address=client_ip
    )
    return {"status": "logged_out"}

@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"authenticated": True, "user": current_user}

# --- PROTECTED DOSSIER ROUTES (Operates strictly on Database 2: dossier_data.db) ---

@app.get("/api/dossier/all")
async def get_dossier(request: Request, current_user: dict = Depends(get_current_user)):
    data = get_dossier_data()
    log_audit(
        action="VIEW_DOSSIER",
        user_id=current_user["id"],
        username=current_user["username"],
        details="Full dossier data inspected",
        ip_address=get_client_ip(request)
    )
    return {
        "success": True,
        "dossier": data,
        "viewer": current_user
    }

@app.post("/api/dossier/scan")
async def trigger_scan(scan_req: ScanRequest, request: Request, current_user: dict = Depends(get_current_user)):
    result = perform_full_osint_scan(scan_req.handle)
    log_audit(
        action="OSINT_SCAN_TRIGGERED",
        user_id=current_user["id"],
        username=current_user["username"],
        details=f"Scan executed for target: {scan_req.handle or 'default'}",
        ip_address=get_client_ip(request)
    )
    return {
        "success": True,
        "result": result,
        "refreshed_data": get_dossier_data()
    }

@app.post("/api/dossier/custom-record")
async def add_record(rec_req: AddRecordRequest, request: Request, current_user: dict = Depends(get_current_user)):
    add_custom_footprint(
        rec_req.platform,
        rec_req.identifier,
        rec_req.url,
        rec_req.category,
        rec_req.summary
    )
    log_audit(
        action="ADD_FOOTPRINT_RECORD",
        user_id=current_user["id"],
        username=current_user["username"],
        details=f"Added custom record on {rec_req.platform}",
        ip_address=get_client_ip(request)
    )
    return {"success": True, "message": "Record appended to dossier database successfully."}

# --- PROTECTED AI QUERY ROUTE ---

@app.post("/api/ai/ask")
async def ask_ai(ai_req: AskAIRequest, request: Request, current_user: dict = Depends(get_current_user)):
    result = query_ai_dossier(ai_req.query)
    log_audit(
        action="AI_QUERY",
        user_id=current_user["id"],
        username=current_user["username"],
        details=f"Prompt: {ai_req.query[:40]}...",
        ip_address=get_client_ip(request)
    )
    return {
        "success": True,
        "data": result
    }

# --- SYSTEM & DUAL DATABASE TELEMETRY ROUTE ---

@app.get("/api/system/stats")
async def system_stats(current_user: dict = Depends(get_current_user)):
    user_db_stats = get_users_stats()
    dossier_db_stats = get_dossier_stats()
    recent_audits = get_recent_audit_logs(limit=8)
    
    return {
        "databases": {
            "database_1": {
                "name": "users_auth.db",
                "purpose": "User accounts, credentials, sessions, and visitor security audit logs",
                "stats": user_db_stats,
                "status": "ONLINE_ENCRYPTED",
                "path": str(USERS_DB_PATH.name)
            },
            "database_2": {
                "name": "dossier_data.db",
                "purpose": "Subject profile, verified internet footprint, GitHub artifacts, AI knowledge base",
                "stats": dossier_db_stats,
                "status": "ONLINE_SYNCED",
                "path": str(DOSSIER_DB_PATH.name)
            }
        },
        "audit_feed": recent_audits,
        "system_status": {
            "encryption": "PBKDF2-HMAC-SHA256 (100k rounds)",
            "auth_protocol": "JWT Bearer + HTTPOnly Cookie",
            "active_user": current_user["username"]
        }
    }

