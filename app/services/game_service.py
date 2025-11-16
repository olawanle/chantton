import random
from decimal import Decimal
from app.models import db, Game, Prize, Claim, User
from app.services.rate_limiter import check_rate_limit
from datetime import datetime, timedelta

def play_game(user_id: int) -> dict:
    """
    Execute a game play for a user.
    Returns: {ok: bool, game_id: int, result: dict, reward_id: int or None}
    """
    # Check rate limit
    if not check_rate_limit(user_id):
        return {
            'ok': False,
            'error': 'Rate limit exceeded. Please try again later.'
        }
    
    # Get all active prizes
    prizes = Prize.query.filter_by(is_active=True).all()
    if not prizes:
        return {
            'ok': False,
            'error': 'No prizes available'
        }
    
    # Calculate total probability weight
    total_weight = sum(float(p.probability) for p in prizes)
    
    if total_weight == 0:
        return {
            'ok': False,
            'error': 'Invalid prize configuration'
        }
    
    # Select prize based on probability
    rand = random.random() * total_weight
    cumulative = 0
    selected_prize = None
    
    for prize in prizes:
        cumulative += float(prize.probability)
        if rand <= cumulative:
            selected_prize = prize
            break
    
    # If no prize selected (edge case), select first prize
    if not selected_prize:
        selected_prize = prizes[0]
    
    # Create game record
    game = Game(
        user_id=user_id,
        result={
            'won': selected_prize is not None,
            'prize_name': selected_prize.name if selected_prize else None,
            'prize_type': selected_prize.type if selected_prize else None
        },
        reward_id=selected_prize.id if selected_prize else None
    )
    
    db.session.add(game)
    db.session.flush()
    
    # If prize requires payout, create claim
    claim = None
    if selected_prize and selected_prize.type in ['ton', 'coupon']:
        claim = Claim(
            game_id=game.id,
            user_id=user_id,
            status='pending'
        )
        db.session.add(claim)
    
    db.session.commit()
    
    return {
        'ok': True,
        'game_id': game.id,
        'result': game.result,
        'reward_id': selected_prize.id if selected_prize else None,
        'claim_id': claim.id if claim else None
    }

