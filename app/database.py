from app.models import db
from app.config import Config

def init_db():
    """Initialize database tables"""
    db.create_all()

