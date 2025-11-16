from flask import Blueprint, render_template, request, jsonify, session
from app.models import db, User, Game, Prize
from app.services.telegram_auth import validate_telegram_auth
from app.config import Config

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Main crystal screen"""
    return render_template('index.html')

@bp.route('/leaderboard')
def leaderboard():
    """Leaderboard screen"""
    return render_template('leaderboard.html')

@bp.route('/profile')
def profile():
    """Profile/Collection screen"""
    return render_template('profile.html')

@bp.route('/tasks')
def tasks():
    """Tasks screen"""
    return render_template('tasks.html')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@bp.route('/prizes')
def get_prizes():
    """Get active prizes"""
    prizes = Prize.query.filter_by(is_active=True).all()
    return jsonify({
        'prizes': [{
            'id': p.id,
            'name': p.name,
            'type': p.type,
            'meta': p.meta,
            'probability': float(p.probability)
        } for p in prizes]
    })

@bp.route('/wins')
def get_wins():
    """Get recent wins for carousel"""
    wins = db.session.query(Game, User, Prize).join(
        User, Game.user_id == User.id
    ).outerjoin(
        Prize, Game.reward_id == Prize.id
    ).filter(
        Game.reward_id.isnot(None)
    ).order_by(
        Game.created_at.desc()
    ).limit(10).all()
    
    return jsonify({
        'wins': [{
            'game_id': game.id,
            'user': {
                'id': user.id,
                'username': user.username or user.display_name or 'Anonymous',
                'display_name': user.display_name
            },
            'prize': {
                'name': prize.name if prize else 'Unknown',
                'type': prize.type if prize else None,
                'meta': prize.meta if prize else {}
            },
            'created_at': game.created_at.isoformat()
        } for game, user, prize in wins]
    })

