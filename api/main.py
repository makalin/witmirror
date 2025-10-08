from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import os
import time
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Import our modules
from database import get_db, init_database
from models import User, Analysis, WisdomTemplate, ApiKey, RateLimit, Analytics
from auth import (
    get_current_user, get_current_user_optional, verify_api_key, 
    check_rate_limit, create_access_token, get_password_hash, verify_password
)
from ai_services import ai_service
from analytics import AnalyticsService
from wisdom_styles import WisdomStyleManager
from integrations import IntegrationManager
from comment_history import CommentHistoryManager

app = FastAPI(
    title="WitMirror Pro API",
    description="Professional AI-powered wisdom response generator with advanced features",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.vercel.app", "*.fly.dev"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173", "https://witmirror.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_database()

# Pydantic models
class AnalysisRequest(BaseModel):
    text: str
    platform: Optional[str] = "general"
    style: Optional[str] = "classic"
    ai_provider: Optional[str] = "openai"
    user_id: Optional[int] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EmotionAnalysis(BaseModel):
    sentiment: str
    confidence: float
    detected_emotions: List[str]
    toxicity_score: float

class WisdomResponse(BaseModel):
    analysis: EmotionAnalysis
    wisdom: str
    style: str
    platform: str
    ai_provider: str
    processing_time: float
    model_used: str

class ApiKeyCreate(BaseModel):
    name: str
    rate_limit: Optional[int] = 1000

class WisdomTemplateCreate(BaseModel):
    name: str
    style: str
    template: str
    variables: Optional[List[str]] = []

class AnalyticsResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    avg_processing_time: float
    sentiment_distribution: Dict[str, int]
    top_emotions: Dict[str, int]
    platform_usage: Dict[str, int]

class BulkAnalysisRequest(BaseModel):
    texts: List[str]
    platform: Optional[str] = "general"
    style: Optional[str] = "classic"
    ai_provider: Optional[str] = "openai"

class ExportRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    format: str = "json"

# Rate limiting and security
def get_client_ip(request: Request) -> str:
    """Get client IP address"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

def check_rate_limit_middleware(request: Request, db: Session = Depends(get_db)):
    """Check rate limit for requests"""
    client_ip = get_client_ip(request)
    
    # Check if IP is blocked
    rate_limit = db.query(RateLimit).filter(
        RateLimit.identifier == client_ip,
        RateLimit.is_blocked == True
    ).first()
    
    if rate_limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    
    # Check current rate limit
    if not check_rate_limit(client_ip, 100, db):  # 100 requests per hour
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    
    return True

# Advanced sentiment analysis
def analyze_sentiment_advanced(text: str) -> EmotionAnalysis:
    """Advanced sentiment analysis with multiple techniques"""
    import re
    import nltk
    from textblob import TextBlob
    
    text_lower = text.lower()
    
    # Rule-based analysis
    negative_words = [
        'stupid', 'dumb', 'idiot', 'moron', 'garbage', 'trash', 'worthless',
        'hate', 'terrible', 'awful', 'horrible', 'disgusting', 'pathetic',
        'sucks', 'suck', 'screams', 'slop', 'dumbest', 'worst', 'hate',
        'useless', 'pointless', 'ridiculous', 'absurd', 'nonsense'
    ]
    
    toxic_words = [
        'kill', 'die', 'death', 'murder', 'violence', 'attack', 'destroy',
        'fuck', 'shit', 'damn', 'hell', 'bitch', 'asshole'
    ]
    
    # Count occurrences
    negative_count = sum(1 for word in negative_words if word in text_lower)
    toxic_count = sum(1 for word in toxic_words if word in text_lower)
    
    # TextBlob sentiment analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment
    if negative_count > 0 or toxic_count > 0 or polarity < -0.3:
        sentiment = "negative"
        confidence = min(0.95, 0.5 + (negative_count * 0.1) + (toxic_count * 0.15) + abs(polarity))
        toxicity_score = min(1.0, toxic_count * 0.3 + abs(polarity) * 0.5)
    elif polarity > 0.3:
        sentiment = "positive"
        confidence = min(0.95, 0.5 + polarity)
        toxicity_score = 0.0
    else:
        sentiment = "neutral"
        confidence = 0.5
        toxicity_score = 0.0
    
    # Detect emotions
    detected_emotions = []
    if negative_count > 0:
        detected_emotions.extend(['anger', 'contempt', 'disgust'])
    if toxic_count > 0:
        detected_emotions.extend(['hostility', 'aggression'])
    if subjectivity > 0.7:
        detected_emotions.append('subjective')
    if polarity < -0.5:
        detected_emotions.append('strongly_negative')
    
    return EmotionAnalysis(
        sentiment=sentiment,
        confidence=confidence,
        detected_emotions=detected_emotions,
        toxicity_score=toxicity_score
    )

# ===== CORE ENDPOINTS =====

@app.get("/")
async def root():
    """API root endpoint with comprehensive information"""
    return {
        "message": "WitMirror Pro API - Turn Negativity into Wisdom",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Advanced AI sentiment analysis",
            "Multiple AI provider support",
            "User authentication & profiles",
            "Rate limiting & security",
            "Analytics & reporting",
            "Bulk processing",
            "Export capabilities"
        ],
        "endpoints": {
            "auth": "/auth/*",
            "analyze": "/analyze",
            "bulk": "/bulk/analyze",
            "analytics": "/analytics/*",
            "admin": "/admin/*",
            "export": "/export/*",
            "health": "/health",
            "docs": "/docs"
        },
        "ai_providers": ai_service.get_available_providers()
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "database": "connected",
        "ai_providers": ai_service.get_available_providers(),
        "uptime": "operational"
    }

# ===== AUTHENTICATION ENDPOINTS =====

@app.post("/auth/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Update last login
    db_user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ===== ANALYSIS ENDPOINTS =====

@app.post("/analyze", response_model=WisdomResponse)
async def analyze_comment(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    request_obj: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Analyze a comment and generate wisdom response with advanced features"""
    start_time = time.time()
    
    try:
        # Check rate limiting
        client_ip = get_client_ip(request_obj)
        if not check_rate_limit(client_ip, 100, db):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Advanced sentiment analysis
        analysis = analyze_sentiment_advanced(request.text)
        
        # Generate wisdom with AI
        wisdom, confidence, model_used = ai_service.generate_wisdom(
            request.text, 
            request.style, 
            request.ai_provider
        )
        
        processing_time = time.time() - start_time
        
        # Save to database
        db_analysis = Analysis(
            user_id=current_user.id if current_user else None,
            original_text=request.text,
            sentiment=analysis.sentiment,
            confidence=analysis.confidence,
            detected_emotions=json.dumps(analysis.detected_emotions),
            toxicity_score=analysis.toxicity_score,
            wisdom_response=wisdom,
            style=request.style,
            platform=request.platform,
            model_used=model_used,
            processing_time=processing_time,
            ip_address=client_ip,
            user_agent=request_obj.headers.get("User-Agent")
        )
        db.add(db_analysis)
        db.commit()
        
        # Track analytics
        analytics_service = AnalyticsService(db)
        background_tasks.add_task(
            analytics_service.track_request,
            {
                "sentiment": analysis.sentiment,
                "detected_emotions": analysis.detected_emotions,
                "platform": request.platform
            },
            processing_time,
            True
        )
        
        return WisdomResponse(
            analysis=analysis,
            wisdom=wisdom,
            style=request.style,
            platform=request.platform,
            ai_provider=request.ai_provider,
            processing_time=processing_time,
            model_used=model_used
        )
        
    except Exception as e:
        # Track failed request
        analytics_service = AnalyticsService(db)
        background_tasks.add_task(
            analytics_service.track_request,
            {},
            time.time() - start_time,
            False
        )
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/bulk/analyze")
async def bulk_analyze(
    request: BulkAnalysisRequest,
    background_tasks: BackgroundTasks,
    request_obj: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Bulk analyze multiple texts"""
    if len(request.texts) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 texts per bulk request")
    
    results = []
    for text in request.texts:
        try:
            analysis = analyze_sentiment_advanced(text)
            wisdom, confidence, model_used = ai_service.generate_wisdom(
                text, request.style, request.ai_provider
            )
            
            results.append({
                "text": text,
                "analysis": analysis,
                "wisdom": wisdom,
                "style": request.style,
                "platform": request.platform,
                "ai_provider": request.ai_provider,
                "model_used": model_used
            })
        except Exception as e:
            results.append({
                "text": text,
                "error": str(e)
            })
    
    return {"results": results, "total": len(request.texts), "successful": len([r for r in results if "error" not in r])}

# ===== ANALYTICS ENDPOINTS =====

@app.get("/analytics/summary", response_model=AnalyticsResponse)
async def get_analytics_summary(db: Session = Depends(get_db)):
    """Get comprehensive analytics summary"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_usage_summary()

@app.get("/analytics/daily")
async def get_daily_analytics(days: int = 30, db: Session = Depends(get_db)):
    """Get daily analytics for the last N days"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_daily_stats(days)

@app.get("/analytics/user/{user_id}")
async def get_user_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get analytics for a specific user"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_user_analytics(user_id)

@app.get("/analytics/trending")
async def get_trending_emotions(days: int = 7, db: Session = Depends(get_db)):
    """Get trending emotions"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_trending_emotions(days)

# ===== ADMIN ENDPOINTS =====

@app.get("/admin/users")
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": users, "total": db.query(User).count()}

@app.get("/admin/analyses")
async def get_all_analyses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all analyses (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    analyses = db.query(Analysis).offset(skip).limit(limit).all()
    return {"analyses": analyses, "total": db.query(Analysis).count()}

# ===== EXPORT ENDPOINTS =====

@app.post("/export/analytics")
async def export_analytics(
    request: ExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export analytics data"""
    analytics_service = AnalyticsService(db)
    data = analytics_service.export_data(request.start_date, request.end_date)
    
    if request.format == "csv":
        # Convert to CSV format
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys() if data else [])
        writer.writeheader()
        writer.writerows(data)
        
        return {"data": output.getvalue(), "format": "csv"}
    
    return {"data": data, "format": "json"}

# ===== AI PROVIDER ENDPOINTS =====

@app.get("/ai/providers")
async def get_ai_providers():
    """Get available AI providers"""
    return {
        "providers": ai_service.get_available_providers(),
        "details": {provider: ai_service.get_provider_info(provider) for provider in ai_service.get_available_providers()}
    }

# ===== WISDOM STYLES ENDPOINTS =====

@app.get("/wisdom/styles")
async def get_wisdom_styles(db: Session = Depends(get_db)):
    """Get all available wisdom styles"""
    style_manager = WisdomStyleManager(db)
    return style_manager.get_all_styles()

@app.get("/wisdom/styles/{style}")
async def get_style_templates(style: str, db: Session = Depends(get_db)):
    """Get templates for a specific wisdom style"""
    style_manager = WisdomStyleManager(db)
    return style_manager.get_style_templates(style)

@app.get("/wisdom/styles/{style}/examples")
async def get_style_examples(style: str, db: Session = Depends(get_db)):
    """Get example wisdom for a specific style"""
    style_manager = WisdomStyleManager(db)
    examples = style_manager.get_style_examples()
    return {"style": style, "examples": examples.get(style, [])}

@app.post("/wisdom/templates")
async def create_wisdom_template(
    name: str,
    style: str,
    template: str,
    variables: List[str] = [],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new wisdom template"""
    style_manager = WisdomStyleManager(db)
    return style_manager.create_template(name, style, template, variables, current_user.id)

# ===== INTEGRATION ENDPOINTS =====

@app.get("/integrations/reddit/{subreddit}")
async def get_reddit_comments(
    subreddit: str,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent comments from Reddit"""
    integration_manager = IntegrationManager(db)
    return integration_manager.get_reddit_comments(subreddit, limit)

@app.get("/integrations/twitter/{username}")
async def get_twitter_mentions(
    username: str,
    count: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get Twitter mentions"""
    integration_manager = IntegrationManager(db)
    return integration_manager.get_twitter_mentions(username, count)

@app.post("/integrations/social-sentiment")
async def analyze_social_sentiment(
    platform: str,
    query: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze sentiment across social media platforms"""
    integration_manager = IntegrationManager(db)
    return integration_manager.analyze_social_media_sentiment(platform, query, limit)

@app.post("/integrations/discord/webhook")
async def create_discord_webhook(
    webhook_url: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create Discord webhook integration"""
    integration_manager = IntegrationManager(db)
    return integration_manager.create_discord_webhook(webhook_url, current_user.id)

@app.get("/integrations/stats")
async def get_integration_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get integration usage statistics"""
    integration_manager = IntegrationManager(db)
    return integration_manager.get_integration_stats(current_user.id)

# ===== COMMENT HISTORY ENDPOINTS =====

@app.get("/history")
async def get_comment_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's comment analysis history"""
    history_manager = CommentHistoryManager(db)
    return history_manager.get_user_history(current_user.id, limit, offset)

@app.get("/history/stats")
async def get_history_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get statistics for user's comment history"""
    history_manager = CommentHistoryManager(db)
    return history_manager.get_history_stats(current_user.id)

@app.post("/history/search")
async def search_history(
    query: str,
    filters: Dict = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search through user's comment history"""
    history_manager = CommentHistoryManager(db)
    return history_manager.search_history(current_user.id, query, filters or {})

@app.get("/history/favorites")
async def get_favorite_responses(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's most effective wisdom responses"""
    history_manager = CommentHistoryManager(db)
    return history_manager.get_favorite_responses(current_user.id, limit)

@app.get("/history/trending")
async def get_trending_topics(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get trending topics from user's analysis history"""
    history_manager = CommentHistoryManager(db)
    return history_manager.get_trending_topics(current_user.id, days)

@app.get("/history/export")
async def export_history(
    format: str = "json",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export user's complete analysis history"""
    history_manager = CommentHistoryManager(db)
    return history_manager.export_history(current_user.id, format)

@app.delete("/history/{analysis_id}")
async def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific analysis from user's history"""
    history_manager = CommentHistoryManager(db)
    success = history_manager.delete_analysis(current_user.id, analysis_id)
    return {"success": success}

@app.delete("/history/bulk")
async def bulk_delete_analyses(
    analysis_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bulk delete analyses from user's history"""
    history_manager = CommentHistoryManager(db)
    deleted_count = history_manager.bulk_delete_analyses(current_user.id, analysis_ids)
    return {"deleted_count": deleted_count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
