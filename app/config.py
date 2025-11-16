import os
from pathlib import Path

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }
    
    # Session security
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # Telegram Bot Token (for verification)
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or ''
    
    # Admin
    ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN') or 'admin-token-change-me'
    
    # Game settings
    MAX_PLAYS_PER_HOUR = int(os.environ.get('MAX_PLAYS_PER_HOUR', '10'))
    DEFAULT_CRYSTAL_COST = int(os.environ.get('DEFAULT_CRYSTAL_COST', '6'))
    
    # TON Payout (placeholder)
    TON_WALLET_PRIVATE_KEY = os.environ.get('TON_WALLET_PRIVATE_KEY') or ''
    TON_NETWORK = os.environ.get('TON_NETWORK', 'testnet')
    
    # Production settings
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    TESTING = False
    
    # Logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', '0') == '1'
    
    @staticmethod
    def init_app(app):
        """Initialize app with config"""
        pass

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def check_production(cls):
        """Check if production environment is properly configured"""
        errors = []
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            errors.append("SECRET_KEY must be changed in production")
        if cls.ADMIN_TOKEN == 'admin-token-change-me':
            errors.append("ADMIN_TOKEN must be changed in production")
        if 'sqlite' in cls.SQLALCHEMY_DATABASE_URI:
            errors.append("Use PostgreSQL in production, not SQLite")
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        return errors

