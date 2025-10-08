from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from models import Analysis, User
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import json

class CommentHistoryManager:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_history(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get user's comment analysis history"""
        analyses = self.db.query(Analysis).filter(
            Analysis.user_id == user_id
        ).order_by(desc(Analysis.created_at)).offset(offset).limit(limit).all()
        
        return [
            {
                'id': analysis.id,
                'original_text': analysis.original_text,
                'sentiment': analysis.sentiment,
                'confidence': analysis.confidence,
                'detected_emotions': json.loads(analysis.detected_emotions) if analysis.detected_emotions else [],
                'toxicity_score': analysis.toxicity_score,
                'wisdom_response': analysis.wisdom_response,
                'style': analysis.style,
                'platform': analysis.platform,
                'model_used': analysis.model_used,
                'processing_time': analysis.processing_time,
                'created_at': analysis.created_at.isoformat()
            }
            for analysis in analyses
        ]
    
    def get_history_stats(self, user_id: int) -> Dict:
        """Get statistics for user's comment history"""
        analyses = self.db.query(Analysis).filter(Analysis.user_id == user_id).all()
        
        if not analyses:
            return {
                'total_analyses': 0,
                'avg_confidence': 0,
                'avg_toxicity': 0,
                'sentiment_distribution': {},
                'style_preferences': {},
                'platform_usage': {},
                'most_common_emotions': [],
                'time_analysis': {}
            }
        
        # Calculate statistics
        total_analyses = len(analyses)
        avg_confidence = sum(a.confidence for a in analyses) / total_analyses
        avg_toxicity = sum(a.toxicity_score for a in analyses) / total_analyses
        
        # Sentiment distribution
        sentiment_counts = {}
        for analysis in analyses:
            sentiment = analysis.sentiment
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        # Style preferences
        style_counts = {}
        for analysis in analyses:
            style = analysis.style
            style_counts[style] = style_counts.get(style, 0) + 1
        
        # Platform usage
        platform_counts = {}
        for analysis in analyses:
            platform = analysis.platform
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        # Most common emotions
        emotion_counts = {}
        for analysis in analyses:
            emotions = json.loads(analysis.detected_emotions) if analysis.detected_emotions else []
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        most_common_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Time analysis (analyses per day of week)
        time_analysis = {}
        for analysis in analyses:
            day_of_week = analysis.created_at.strftime('%A')
            time_analysis[day_of_week] = time_analysis.get(day_of_week, 0) + 1
        
        return {
            'total_analyses': total_analyses,
            'avg_confidence': round(avg_confidence, 2),
            'avg_toxicity': round(avg_toxicity, 2),
            'sentiment_distribution': sentiment_counts,
            'style_preferences': style_counts,
            'platform_usage': platform_counts,
            'most_common_emotions': [{'emotion': emotion, 'count': count} for emotion, count in most_common_emotions],
            'time_analysis': time_analysis
        }
    
    def search_history(self, user_id: int, query: str, filters: Dict = None) -> List[Dict]:
        """Search through user's comment history"""
        query_obj = self.db.query(Analysis).filter(Analysis.user_id == user_id)
        
        # Text search
        if query:
            query_obj = query_obj.filter(Analysis.original_text.contains(query))
        
        # Apply filters
        if filters:
            if 'sentiment' in filters:
                query_obj = query_obj.filter(Analysis.sentiment == filters['sentiment'])
            if 'platform' in filters:
                query_obj = query_obj.filter(Analysis.platform == filters['platform'])
            if 'style' in filters:
                query_obj = query_obj.filter(Analysis.style == filters['style'])
            if 'date_from' in filters:
                query_obj = query_obj.filter(Analysis.created_at >= filters['date_from'])
            if 'date_to' in filters:
                query_obj = query_obj.filter(Analysis.created_at <= filters['date_to'])
        
        analyses = query_obj.order_by(desc(Analysis.created_at)).all()
        
        return [
            {
                'id': analysis.id,
                'original_text': analysis.original_text,
                'sentiment': analysis.sentiment,
                'confidence': analysis.confidence,
                'wisdom_response': analysis.wisdom_response,
                'style': analysis.style,
                'platform': analysis.platform,
                'created_at': analysis.created_at.isoformat()
            }
            for analysis in analyses
        ]
    
    def get_favorite_responses(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's most effective wisdom responses"""
        # This would require a rating system in production
        # For now, return recent high-confidence responses
        analyses = self.db.query(Analysis).filter(
            and_(
                Analysis.user_id == user_id,
                Analysis.confidence >= 0.8
            )
        ).order_by(desc(Analysis.confidence)).limit(limit).all()
        
        return [
            {
                'id': analysis.id,
                'original_text': analysis.original_text,
                'wisdom_response': analysis.wisdom_response,
                'confidence': analysis.confidence,
                'style': analysis.style,
                'platform': analysis.platform,
                'created_at': analysis.created_at.isoformat()
            }
            for analysis in analyses
        ]
    
    def get_trending_topics(self, user_id: int, days: int = 30) -> List[Dict]:
        """Get trending topics from user's analysis history"""
        start_date = datetime.now() - timedelta(days=days)
        
        analyses = self.db.query(Analysis).filter(
            and_(
                Analysis.user_id == user_id,
                Analysis.created_at >= start_date
            )
        ).all()
        
        # Simple keyword extraction (in production, use proper NLP)
        keywords = {}
        for analysis in analyses:
            text = analysis.original_text.lower()
            # Simple keyword extraction
            words = text.split()
            for word in words:
                if len(word) > 3:  # Filter short words
                    keywords[word] = keywords.get(word, 0) + 1
        
        trending_topics = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [
            {'topic': topic, 'frequency': count}
            for topic, count in trending_topics
        ]
    
    def export_history(self, user_id: int, format: str = 'json') -> Dict:
        """Export user's complete analysis history"""
        analyses = self.db.query(Analysis).filter(Analysis.user_id == user_id).all()
        
        export_data = {
            'user_id': user_id,
            'export_date': datetime.now().isoformat(),
            'total_analyses': len(analyses),
            'analyses': []
        }
        
        for analysis in analyses:
            export_data['analyses'].append({
                'id': analysis.id,
                'original_text': analysis.original_text,
                'sentiment': analysis.sentiment,
                'confidence': analysis.confidence,
                'detected_emotions': json.loads(analysis.detected_emotions) if analysis.detected_emotions else [],
                'toxicity_score': analysis.toxicity_score,
                'wisdom_response': analysis.wisdom_response,
                'style': analysis.style,
                'platform': analysis.platform,
                'model_used': analysis.model_used,
                'processing_time': analysis.processing_time,
                'created_at': analysis.created_at.isoformat()
            })
        
        return export_data
    
    def delete_analysis(self, user_id: int, analysis_id: int) -> bool:
        """Delete a specific analysis from user's history"""
        analysis = self.db.query(Analysis).filter(
            and_(
                Analysis.id == analysis_id,
                Analysis.user_id == user_id
            )
        ).first()
        
        if not analysis:
            return False
        
        self.db.delete(analysis)
        self.db.commit()
        return True
    
    def bulk_delete_analyses(self, user_id: int, analysis_ids: List[int]) -> int:
        """Bulk delete analyses from user's history"""
        deleted_count = self.db.query(Analysis).filter(
            and_(
                Analysis.id.in_(analysis_ids),
                Analysis.user_id == user_id
            )
        ).delete(synchronize_session=False)
        
        self.db.commit()
        return deleted_count
