from flask import Blueprint, request, jsonify, session
from app.models import db, User, Game, Claim
from app.services.game_service import play_game
from app.utils.validators import validate_positive_integer
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('game', __name__, url_prefix='/game')

def get_current_user():
    """Get current user from session"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)

@bp.route('/play', methods=['POST'])
def play():
    """Execute a game play"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Not authenticated'}), 401
        
        result = play_game(user.id)
        
        if not result.get('ok'):
            logger.warning(f"Game play failed for user {user.id}: {result.get('error')}")
            return jsonify(result), 400
        
        logger.info(f"Game play successful for user {user.id}, game_id: {result.get('game_id')}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in game play: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/user/<int:user_id>/history')
def user_history(user_id):
    """Get user's game history"""
    try:
        if not validate_positive_integer(user_id):
            return jsonify({'error': 'Invalid user ID'}), 400
        
        user = get_current_user()
        if not user or (user.id != user_id and not session.get('is_admin')):
            return jsonify({'error': 'Unauthorized'}), 403
        
        games = Game.query.filter_by(user_id=user_id).order_by(Game.created_at.desc()).limit(50).all()
        
        return jsonify({
            'games': [{
                'id': g.id,
                'result': g.result,
                'reward_id': g.reward_id,
                'created_at': g.created_at.isoformat()
            } for g in games]
        })
    except Exception as e:
        logger.error(f"Error fetching user history: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/claim/<int:game_id>', methods=['POST'])
def create_claim(game_id):
    """Create a claim for a game"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    game = Game.query.get_or_404(game_id)
    if game.user_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if game.reward_id is None:
        return jsonify({'error': 'No reward to claim'}), 400
    
    # Check if claim already exists
    existing_claim = Claim.query.filter_by(game_id=game_id).first()
    if existing_claim:
        return jsonify({
            'ok': True,
            'claim_id': existing_claim.id,
            'status': existing_claim.status
        })
    
    claim = Claim(
        game_id=game_id,
        user_id=user.id,
        status='pending'
    )
    db.session.add(claim)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'claim_id': claim.id,
        'status': claim.status
    })

