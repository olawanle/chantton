from flask import Blueprint, request, jsonify, session
from app.models import db, User, Task, UserTask
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def get_current_user():
    """Get current user from session"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)

@bp.route('', methods=['GET'])
def list_tasks():
    """Get list of available tasks"""
    tasks = Task.query.filter_by(is_active=True).all()
    
    user = get_current_user()
    completed_task_ids = set()
    if user:
        completed = UserTask.query.filter_by(
            user_id=user.id,
            completed=True
        ).all()
        completed_task_ids = {ut.task_id for ut in completed}
    
    return jsonify({
        'tasks': [{
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'action_type': t.action_type,
            'action_meta': t.action_meta,
            'reward_points': t.reward_points,
            'completed': t.id in completed_task_ids
        } for t in tasks]
    })

@bp.route('/check', methods=['POST'])
def check_task():
    """Verify and complete a task"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    task_id = data.get('task_id')
    
    if not task_id:
        return jsonify({'error': 'Missing task_id'}), 400
    
    task = Task.query.get_or_404(task_id)
    
    # Check if already completed
    user_task = UserTask.query.filter_by(
        user_id=user.id,
        task_id=task_id
    ).first()
    
    if user_task and user_task.completed:
        return jsonify({
            'ok': True,
            'message': 'Task already completed',
            'completed': True
        })
    
    # TODO: Implement actual verification based on action_type
    # For now, just mark as completed
    # In production, verify:
    # - subscribe: Check Telegram Bot API for channel membership
    # - boost: Verify boost action
    # - join: Check group membership
    
    if not user_task:
        user_task = UserTask(
            user_id=user.id,
            task_id=task_id,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.session.add(user_task)
    else:
        user_task.completed = True
        user_task.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Task completed',
        'reward_points': task.reward_points,
        'completed': True
    })

