from flask import Blueprint, request, jsonify, session, render_template
from app.models import db, Claim, Prize, AuditLog, Game, User
from app.services.ton_payout import send_payout
from app.config import Config
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin():
    """Check if user is admin"""
    admin_token = request.headers.get('X-Admin-Token') or request.args.get('token')
    if admin_token != Config.ADMIN_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 403
    return None

@bp.route('/dashboard')
def dashboard():
    """Admin dashboard page"""
    # Allow access to dashboard page, but API endpoints require token
    return render_template('admin/dashboard.html')

@bp.route('/claims', methods=['GET'])
def list_claims():
    """List all claims"""
    error = require_admin()
    if error:
        return error
    
    status = request.args.get('status', 'pending')
    claims = Claim.query.filter_by(status=status).order_by(Claim.created_at.desc()).limit(100).all()
    
    result = []
    for claim in claims:
        game = Game.query.get(claim.game_id)
        user = User.query.get(claim.user_id)
        prize = game.prize if game else None
        
        result.append({
            'id': claim.id,
            'game_id': claim.game_id,
            'user': {
                'id': user.id if user else None,
                'username': user.username if user else None,
                'display_name': user.display_name if user else None
            },
            'prize': {
                'name': prize.name if prize else None,
                'type': prize.type if prize else None,
                'meta': prize.meta if prize else {}
            },
            'status': claim.status,
            'payout_tx': claim.payout_tx,
            'created_at': claim.created_at.isoformat()
        })
    
    return jsonify({'claims': result})

@bp.route('/payout/<int:claim_id>', methods=['POST'])
def payout(claim_id):
    """Process payout for a claim"""
    error = require_admin()
    if error:
        return error
    
    claim = Claim.query.get_or_404(claim_id)
    if claim.status != 'pending':
        return jsonify({'error': 'Claim not pending'}), 400
    
    game = Game.query.get(claim.game_id)
    prize = game.prize if game else None
    
    if not prize or prize.type != 'ton':
        return jsonify({'error': 'Invalid prize type for payout'}), 400
    
    # Get payout address from request or prize meta
    data = request.get_json() or {}
    to_address = data.get('to_address') or prize.meta.get('payout_address')
    
    if not to_address:
        return jsonify({'error': 'Missing payout address'}), 400
    
    amount = prize.meta.get('amount', 0)
    
    # Send payout (mock for now)
    tx_hash = send_payout(to_address, amount)
    
    # Update claim
    claim.status = 'paid'
    claim.payout_tx = tx_hash
    claim.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log audit
    audit = AuditLog(
        actor='admin',
        action='payout',
        meta={'claim_id': claim_id, 'tx_hash': tx_hash, 'amount': amount}
    )
    db.session.add(audit)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'claim_id': claim_id,
        'tx_hash': tx_hash
    })

@bp.route('/claim/<int:claim_id>/approve', methods=['POST'])
def approve_claim(claim_id):
    """Approve a claim"""
    error = require_admin()
    if error:
        return error
    
    claim = Claim.query.get_or_404(claim_id)
    claim.status = 'approved'
    claim.updated_at = datetime.utcnow()
    db.session.commit()
    
    audit = AuditLog(
        actor='admin',
        action='approve_claim',
        meta={'claim_id': claim_id}
    )
    db.session.add(audit)
    db.session.commit()
    
    return jsonify({'ok': True})

@bp.route('/claim/<int:claim_id>/reject', methods=['POST'])
def reject_claim(claim_id):
    """Reject a claim"""
    error = require_admin()
    if error:
        return error
    
    claim = Claim.query.get_or_404(claim_id)
    claim.status = 'rejected'
    claim.updated_at = datetime.utcnow()
    db.session.commit()
    
    audit = AuditLog(
        actor='admin',
        action='reject_claim',
        meta={'claim_id': claim_id}
    )
    db.session.add(audit)
    db.session.commit()
    
    return jsonify({'ok': True})

@bp.route('/prize', methods=['POST'])
def add_prize():
    """Add or update a prize"""
    error = require_admin()
    if error:
        return error
    
    data = request.get_json()
    
    prize_id = data.get('id')
    if prize_id:
        prize = Prize.query.get_or_404(prize_id)
    else:
        prize = Prize()
    
    prize.name = data.get('name', prize.name)
    prize.type = data.get('type', prize.type)
    prize.meta = data.get('meta', prize.meta or {})
    prize.probability = data.get('probability', prize.probability)
    prize.is_active = data.get('is_active', prize.is_active if prize.id else True)
    
    if not prize.id:
        db.session.add(prize)
    db.session.commit()
    
    audit = AuditLog(
        actor='admin',
        action='add_prize' if not prize_id else 'update_prize',
        meta={'prize_id': prize.id}
    )
    db.session.add(audit)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'prize': {
            'id': prize.id,
            'name': prize.name,
            'type': prize.type,
            'meta': prize.meta,
            'probability': float(prize.probability)
        }
    })

@bp.route('/prizes', methods=['GET'])
def list_prizes():
    """List all prizes"""
    error = require_admin()
    if error:
        return error
    
    prizes = Prize.query.order_by(Prize.created_at.desc()).all()
    return jsonify({
        'prizes': [{
            'id': p.id,
            'name': p.name,
            'type': p.type,
            'meta': p.meta,
            'probability': float(p.probability),
            'is_active': p.is_active
        } for p in prizes]
    })

