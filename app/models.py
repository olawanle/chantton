from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import BigInteger, Numeric

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    tg_user_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), unique=True, nullable=False, index=True)
    username = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    games = db.relationship('Game', backref='user', lazy=True)
    claims = db.relationship('Claim', backref='user', lazy=True)

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    user_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=False)
    result = db.Column(JSONB().with_variant(db.JSON, 'sqlite'))
    reward_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('prizes.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prize = db.relationship('Prize', backref='games', lazy=True)
    claim = db.relationship('Claim', backref='game', uselist=False, lazy=True)

class Prize(db.Model):
    __tablename__ = 'prizes'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'ton', 'coupon', 'points'
    meta = db.Column(JSONB().with_variant(db.JSON, 'sqlite'), default={})
    probability = db.Column(Numeric(10, 8), nullable=False)  # 0..1
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Claim(db.Model):
    __tablename__ = 'claims'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    game_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, approved, paid, rejected
    payout_tx = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    actor = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    meta = db.Column(JSONB().with_variant(db.JSON, 'sqlite'), default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    action_type = db.Column(db.String(100), nullable=False)  # 'subscribe', 'boost', 'join', etc.
    action_meta = db.Column(JSONB().with_variant(db.JSON, 'sqlite'), default={})  # channel_id, etc.
    reward_points = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserTask(db.Model):
    __tablename__ = 'user_tasks'
    
    id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), primary_key=True)
    user_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(BigInteger().with_variant(db.Integer, 'sqlite'), db.ForeignKey('tasks.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='user_tasks')
    task = db.relationship('Task', backref='user_tasks')

