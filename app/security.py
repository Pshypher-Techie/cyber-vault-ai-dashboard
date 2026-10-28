from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database_users import get_user_by_username

security_bearer = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

async def get_current_user(
    request: Request,
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
) -> dict:
    token = None
    
    # 1. Check Authorization Bearer header
    if auth_credentials:
        token = auth_credentials.credentials
        
    # 2. Check Cookie
    if not token and "access_token" in request.cookies:
        cookie_val = request.cookies.get("access_token")
        if cookie_val.startswith("Bearer "):
            token = cookie_val.split("Bearer ")[1].strip()
        else:
            token = cookie_val.strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cyber-Vault Access Denied: Missing or invalid authentication token. Please sign in.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cyber-Vault Access Denied: Token expired or invalid signature.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cyber-Vault Access Denied: Invalid token payload.",
        )

    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cyber-Vault Access Denied: User account not found.",
        )

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

