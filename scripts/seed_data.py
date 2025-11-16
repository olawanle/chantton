#!/usr/bin/env python3
"""
Seed database with initial data (prizes and tasks)
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models import db, Prize, Task
from decimal import Decimal

def seed_data():
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        # Prize.query.delete()
        # Task.query.delete()
        
        # Add prizes
        prizes = [
            {
                'name': 'Scared Cat',
                'type': 'points',
                'meta': {'points': 100, 'image_path': 'images/scared_cat.png'},
                'probability': Decimal('0.30')  # 30%
            },
            {
                'name': 'Skull Flow',
                'type': 'points',
                'meta': {'points': 200, 'image_path': 'images/skull_flow.png'},
                'probability': Decimal('0.25')  # 25%
            },
            {
                'name': 'Small TON Prize',
                'type': 'ton',
                'meta': {'amount': 0.1, 'payout_address': ''},
                'probability': Decimal('0.15')  # 15%
            },
            {
                'name': 'Medium TON Prize',
                'type': 'ton',
                'meta': {'amount': 1.0, 'payout_address': ''},
                'probability': Decimal('0.05')  # 5%
            },
            {
                'name': 'Coupon Code',
                'type': 'coupon',
                'meta': {'code': 'WELCOME10', 'discount': 10},
                'probability': Decimal('0.20')  # 20%
            },
            {
                'name': 'No Prize',
                'type': 'points',
                'meta': {'points': 0},
                'probability': Decimal('0.05')  # 5% (low chance of no prize)
            }
        ]
        
        for prize_data in prizes:
            existing = Prize.query.filter_by(name=prize_data['name']).first()
            if not existing:
                prize = Prize(**prize_data)
                db.session.add(prize)
                print(f"Added prize: {prize_data['name']}")
            else:
                print(f"Prize already exists: {prize_data['name']}")
        
        # Add tasks
        tasks = [
            {
                'name': 'Subscribe channel',
                'description': 'Subscribe to our Telegram channel',
                'action_type': 'subscribe',
                'action_meta': {'channel_id': '@your_channel'},
                'reward_points': 1
            },
            {
                'name': 'Boost channel',
                'description': 'Boost our Telegram channel',
                'action_type': 'boost',
                'action_meta': {'channel_id': '@your_channel'},
                'reward_points': 1
            },
            {
                'name': 'Join community',
                'description': 'Join our Telegram community',
                'action_type': 'join',
                'action_meta': {'group_id': '@your_group'},
                'reward_points': 1
            },
            {
                'name': 'Subscribe to gift news',
                'description': 'Subscribe to gift news channel',
                'action_type': 'subscribe',
                'action_meta': {'channel_id': '@gift_news'},
                'reward_points': 1
            }
        ]
        
        for task_data in tasks:
            existing = Task.query.filter_by(name=task_data['name']).first()
            if not existing:
                task = Task(**task_data)
                db.session.add(task)
                print(f"Added task: {task_data['name']}")
            else:
                print(f"Task already exists: {task_data['name']}")
        
        db.session.commit()
        print("\nSeed data completed!")

if __name__ == '__main__':
    seed_data()

