from flask import Blueprint, request, jsonify, session
from app.models import db, User
from app.services.telegram_auth import validate_telegram_auth

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/telegram', methods=['POST'])
def telegram_auth():
    """Authenticate user via Telegram WebApp initData"""
    data = request.get_json()
    init_data = data.get('initData', '')
    
    if not init_data:
        return jsonify({'error': 'Missing initData'}), 400
    
    user_data = validate_telegram_auth(init_data)
    if not user_data:
        return jsonify({'error': 'Invalid authentication'}), 401
    
    tg_user_id = user_data.get('id')
    if not tg_user_id:
        return jsonify({'error': 'Invalid user data'}), 400
    
    # Get or create user
    user = User.query.filter_by(tg_user_id=tg_user_id).first()
    if not user:
        user = User(
            tg_user_id=tg_user_id,
            username=user_data.get('username'),
            display_name=user_data.get('first_name', '') + ' ' + (user_data.get('last_name', '') or '')
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update user info
        if user_data.get('username'):
            user.username = user_data.get('username')
        if user_data.get('first_name'):
            user.display_name = user_data.get('first_name', '') + ' ' + (user_data.get('last_name', '') or '')
        db.session.commit()
    
    # Set session
    session['user_id'] = user.id
    session['tg_user_id'] = tg_user_id
    
    return jsonify({
        'ok': True,
        'user': {
            'id': user.id,
            'tg_user_id': user.tg_user_id,
            'username': user.username,
            'display_name': user.display_name
        }
    })

