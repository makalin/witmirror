from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import Analysis, Analytics, User
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def track_request(self, analysis_data: Dict, processing_time: float, success: bool = True):
        """Track API request for analytics"""
        # Update daily analytics
        today = datetime.utcnow().date()
        analytics = self.db.query(Analytics).filter(
            func.date(Analytics.date) == today
        ).first()
        
        if not analytics:
            analytics = Analytics(
                date=datetime.utcnow(),
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                avg_processing_time=0.0,
                unique_users=0,
                top_emotions={},
                platform_usage={}
            )
            self.db.add(analytics)
        
        analytics.total_requests += 1
        if success:
            analytics.successful_requests += 1
        else:
            analytics.failed_requests += 1
        
        # Update average processing time
        total_requests = analytics.successful_requests + analytics.failed_requests
        analytics.avg_processing_time = (
            (analytics.avg_processing_time * (total_requests - 1) + processing_time) / total_requests
        )
        
        # Update emotions tracking
        emotions = analysis_data.get('detected_emotions', [])
        for emotion in emotions:
            if emotion in analytics.top_emotions:
                analytics.top_emotions[emotion] += 1
            else:
                analytics.top_emotions[emotion] = 1
        
        # Update platform usage
        platform = analysis_data.get('platform', 'general')
        if platform in analytics.platform_usage:
            analytics.platform_usage[platform] += 1
        else:
            analytics.platform_usage[platform] = 1
        
        self.db.commit()
    
    def get_daily_stats(self, days: int = 30) -> List[Dict]:
        """Get daily statistics for the last N days"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        analytics = self.db.query(Analytics).filter(
            Analytics.date >= start_date,
            Analytics.date <= end_date
        ).order_by(Analytics.date.desc()).all()
        
        return [
            {
                "date": a.date.isoformat(),
                "total_requests": a.total_requests,
                "successful_requests": a.successful_requests,
                "failed_requests": a.failed_requests,
                "avg_processing_time": a.avg_processing_time,
                "unique_users": a.unique_users,
                "top_emotions": a.top_emotions,
                "platform_usage": a.platform_usage
            }
            for a in analytics
        ]
    
    def get_usage_summary(self) -> Dict:
        """Get overall usage summary"""
        total_analyses = self.db.query(Analytics).with_entities(
            func.sum(Analytics.total_requests),
            func.sum(Analytics.successful_requests),
            func.sum(Analytics.failed_requests),
            func.avg(Analytics.avg_processing_time)
        ).first()
        
        total_requests, successful_requests, failed_requests, avg_processing_time = total_analyses
        
        # Get sentiment distribution
        sentiment_stats = self.db.query(
            Analysis.sentiment,
            func.count(Analysis.id).label('count')
        ).group_by(Analysis.sentiment).all()
        
        # Get top emotions
        emotion_counts = {}
        analyses = self.db.query(Analysis.detected_emotions).all()
        for analysis in analyses:
            emotions = json.loads(analysis.detected_emotions) if isinstance(analysis.detected_emotions, str) else analysis.detected_emotions
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get platform usage
        platform_stats = self.db.query(
            Analysis.platform,
            func.count(Analysis.id).label('count')
        ).group_by(Analysis.platform).all()
        
        return {
            "total_requests": total_requests or 0,
            "successful_requests": successful_requests or 0,
            "failed_requests": failed_requests or 0,
            "success_rate": (successful_requests / total_requests * 100) if total_requests else 0,
            "avg_processing_time": round(avg_processing_time or 0, 2),
            "sentiment_distribution": {s.sentiment: s.count for s in sentiment_stats},
            "top_emotions": dict(sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "platform_usage": {p.platform: p.count for p in platform_stats}
        }
    
    def get_user_analytics(self, user_id: int) -> Dict:
        """Get analytics for a specific user"""
        user_analyses = self.db.query(Analysis).filter(Analysis.user_id == user_id).all()
        
        if not user_analyses:
            return {"message": "No analyses found for this user"}
        
        # Calculate user-specific metrics
        total_analyses = len(user_analyses)
        avg_confidence = sum(a.confidence for a in user_analyses) / total_analyses
        avg_toxicity = sum(a.toxicity_score for a in user_analyses) / total_analyses
        
        # Get sentiment distribution
        sentiment_counts = {}
        for analysis in user_analyses:
            sentiment_counts[analysis.sentiment] = sentiment_counts.get(analysis.sentiment, 0) + 1
        
        # Get style preferences
        style_counts = {}
        for analysis in user_analyses:
            style_counts[analysis.style] = style_counts.get(analysis.style, 0) + 1
        
        return {
            "total_analyses": total_analyses,
            "avg_confidence": round(avg_confidence, 2),
            "avg_toxicity": round(avg_toxicity, 2),
            "sentiment_distribution": sentiment_counts,
            "style_preferences": style_counts,
            "first_analysis": user_analyses[-1].created_at.isoformat(),
            "last_analysis": user_analyses[0].created_at.isoformat()
        }
    
    def get_trending_emotions(self, days: int = 7) -> List[Dict]:
        """Get trending emotions over the last N days"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        analyses = self.db.query(Analysis).filter(
            Analysis.created_at >= start_date,
            Analysis.created_at <= end_date
        ).all()
        
        emotion_counts = {}
        for analysis in analyses:
            emotions = json.loads(analysis.detected_emotions) if isinstance(analysis.detected_emotions, str) else analysis.detected_emotions
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return [
            {"emotion": emotion, "count": count}
            for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    
    def export_data(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict]:
        """Export analytics data for external analysis"""
        query = self.db.query(Analytics)
        
        if start_date:
            query = query.filter(Analytics.date >= start_date)
        if end_date:
            query = query.filter(Analytics.date <= end_date)
        
        analytics = query.all()
        
        return [
            {
                "date": a.date.isoformat(),
                "total_requests": a.total_requests,
                "successful_requests": a.successful_requests,
                "failed_requests": a.failed_requests,
                "avg_processing_time": a.avg_processing_time,
                "unique_users": a.unique_users,
                "top_emotions": a.top_emotions,
                "platform_usage": a.platform_usage
            }
            for a in analytics
        ]
