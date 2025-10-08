from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import os
from models import User, ApiKey
from sqlalchemy.orm import Session

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), db: Session = Depends(get_db)):
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None

def verify_api_key(api_key: str, db: Session) -> Optional[ApiKey]:
    key_obj = db.query(ApiKey).filter(ApiKey.key == api_key, ApiKey.is_active == True).first()
    if key_obj:
        key_obj.last_used = datetime.utcnow()
        db.commit()
    return key_obj

def check_rate_limit(identifier: str, limit: int, db: Session) -> bool:
    """Check if identifier has exceeded rate limit"""
    now = datetime.utcnow()
    window_start = now - timedelta(hours=1)
    
    rate_limit = db.query(RateLimit).filter(
        RateLimit.identifier == identifier,
        RateLimit.window_start >= window_start
    ).first()
    
    if not rate_limit:
        rate_limit = RateLimit(identifier=identifier, requests_count=0, window_start=now)
        db.add(rate_limit)
    
    if rate_limit.is_blocked:
        return False
    
    rate_limit.requests_count += 1
    
    if rate_limit.requests_count > limit:
        rate_limit.is_blocked = True
        db.commit()
        return False
    
    db.commit()
    return True
