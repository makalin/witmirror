from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    preferences = Column(JSON, default={})

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Optional user association
    original_text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    detected_emotions = Column(JSON, nullable=False)
    toxicity_score = Column(Float, nullable=False)
    wisdom_response = Column(Text, nullable=False)
    style = Column(String(20), default="classic")
    platform = Column(String(20), default="general")
    model_used = Column(String(50), default="gpt-4")
    processing_time = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    user_agent = Column(Text)

class WisdomTemplate(Base):
    __tablename__ = "wisdom_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    style = Column(String(20), nullable=False)
    template = Column(Text, nullable=False)
    variables = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True)
    name = Column(String(100))
    user_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    rate_limit = Column(Integer, default=1000)  # requests per hour
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)

class RateLimit(Base):
    __tablename__ = "rate_limits"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(255), index=True)  # IP or API key
    requests_count = Column(Integer, default=0)
    window_start = Column(DateTime, default=datetime.utcnow)
    is_blocked = Column(Boolean, default=False)

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_processing_time = Column(Float, default=0.0)
    unique_users = Column(Integer, default=0)
    top_emotions = Column(JSON, default={})
    platform_usage = Column(JSON, default={})
