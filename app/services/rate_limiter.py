from app.models import db, Game
from app.config import Config
from datetime import datetime, timedelta

def check_rate_limit(user_id: int) -> bool:
    """Check if user has exceeded play rate limit"""
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent_plays = Game.query.filter(
        Game.user_id == user_id,
        Game.created_at >= one_hour_ago
    ).count()
    
    return recent_plays < Config.MAX_PLAYS_PER_HOUR

