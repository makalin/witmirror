from sqlalchemy.orm import Session
from models import Analysis, User
from typing import List, Dict, Optional
import requests
import json
from datetime import datetime, timedelta

class IntegrationManager:
    def __init__(self, db: Session):
        self.db = db
    
    def get_reddit_comments(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """Fetch recent comments from Reddit API"""
        try:
            # Reddit API endpoint (requires authentication in production)
            url = f"https://www.reddit.com/r/{subreddit}/comments.json"
            headers = {
                'User-Agent': 'WitMirror/1.0'
            }
            
            response = requests.get(url, headers=headers, params={'limit': limit})
            response.raise_for_status()
            
            data = response.json()
            comments = []
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                comments.append({
                    'id': post_data.get('id'),
                    'text': post_data.get('body', ''),
                    'author': post_data.get('author'),
                    'score': post_data.get('score', 0),
                    'created_utc': post_data.get('created_utc'),
                    'subreddit': post_data.get('subreddit'),
                    'platform': 'reddit'
                })
            
            return comments
        except Exception as e:
            print(f"Reddit API error: {e}")
            return []
    
    def get_twitter_mentions(self, username: str, count: int = 10) -> List[Dict]:
        """Fetch Twitter mentions (requires Twitter API v2)"""
        try:
            # This would require Twitter API v2 credentials
            # For demo purposes, returning mock data
            return [
                {
                    'id': f'tweet_{i}',
                    'text': f'Mock tweet mention {i}',
                    'author': f'user_{i}',
                    'created_at': datetime.now().isoformat(),
                    'platform': 'twitter'
                }
                for i in range(count)
            ]
        except Exception as e:
            print(f"Twitter API error: {e}")
            return []
    
    def analyze_social_media_sentiment(self, platform: str, query: str, limit: int = 50) -> Dict:
        """Analyze sentiment across social media platforms"""
        comments = []
        
        if platform == 'reddit':
            comments = self.get_reddit_comments(query, limit)
        elif platform == 'twitter':
            comments = self.get_twitter_mentions(query, limit)
        
        if not comments:
            return {
                'platform': platform,
                'query': query,
                'total_comments': 0,
                'sentiment_distribution': {},
                'top_negative_comments': [],
                'recommended_responses': []
            }
        
        # Analyze sentiment for each comment
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        negative_comments = []
        
        for comment in comments:
            # Simple sentiment analysis (in production, use proper NLP)
            text = comment['text'].lower()
            negative_words = ['hate', 'stupid', 'dumb', 'terrible', 'awful', 'horrible']
            positive_words = ['love', 'great', 'amazing', 'wonderful', 'excellent']
            
            if any(word in text for word in negative_words):
                sentiment_counts['negative'] += 1
                if len(negative_comments) < 5:  # Top 5 negative comments
                    negative_comments.append(comment)
            elif any(word in text for word in positive_words):
                sentiment_counts['positive'] += 1
            else:
                sentiment_counts['neutral'] += 1
        
        # Generate recommended responses for negative comments
        recommended_responses = []
        for comment in negative_comments[:3]:  # Top 3 for responses
            recommended_responses.append({
                'original_text': comment['text'],
                'wisdom_response': self._generate_wisdom_for_comment(comment['text']),
                'platform': comment['platform']
            })
        
        return {
            'platform': platform,
            'query': query,
            'total_comments': len(comments),
            'sentiment_distribution': sentiment_counts,
            'top_negative_comments': negative_comments,
            'recommended_responses': recommended_responses
        }
    
    def _generate_wisdom_for_comment(self, text: str) -> str:
        """Generate wisdom response for a comment"""
        wisdom_options = [
            "The mirror often blames the face it reflects.",
            "Politeness is free; rudeness always collects interest.",
            "A gentle word turns away wrath, but harsh words stir up anger.",
            "The wise speak because they have something to say; fools speak because they have to say something.",
            "When you point a finger at others, three fingers point back at you."
        ]
        
        import random
        return random.choice(wisdom_options)
    
    def create_discord_webhook(self, webhook_url: str, user_id: int) -> Dict:
        """Create Discord webhook integration"""
        # In production, store webhook URLs in database
        return {
            'webhook_url': webhook_url,
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
    
    def send_discord_notification(self, webhook_url: str, message: str, wisdom: str) -> bool:
        """Send notification to Discord webhook"""
        try:
            payload = {
                'content': f"**New Wisdom Generated**\n\n**Original:** {message}\n**Wisdom:** {wisdom}",
                'username': 'WitMirror',
                'avatar_url': 'https://example.com/witmirror-avatar.png'
            }
            
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 204
        except Exception as e:
            print(f"Discord webhook error: {e}")
            return False
    
    def get_integration_stats(self, user_id: int) -> Dict:
        """Get integration usage statistics for a user"""
        # Get user's analysis history
        analyses = self.db.query(Analysis).filter(Analysis.user_id == user_id).all()
        
        platform_usage = {}
        for analysis in analyses:
            platform = analysis.platform
            if platform in platform_usage:
                platform_usage[platform] += 1
            else:
                platform_usage[platform] = 1
        
        return {
            'total_analyses': len(analyses),
            'platform_usage': platform_usage,
            'most_used_platform': max(platform_usage.items(), key=lambda x: x[1])[0] if platform_usage else None,
            'integration_status': {
                'reddit': True,  # Would check actual integration status
                'twitter': False,
                'discord': True
            }
        }
    
    def export_user_data(self, user_id: int, format: str = 'json') -> Dict:
        """Export user's analysis history"""
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
