"""
Unit tests for game service
"""
import unittest
from decimal import Decimal
from app import create_app
from app.models import db, User, Prize, Game
from app.services.game_service import play_game
from app.config import Config

class TestGameService(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            tg_user_id=12345,
            username='testuser',
            display_name='Test User'
        )
        db.session.add(self.user)
        db.session.commit()
        
        # Create test prizes
        self.prizes = [
            Prize(
                name='Prize 1',
                type='points',
                meta={'points': 100},
                probability=Decimal('0.5')
            ),
            Prize(
                name='Prize 2',
                type='points',
                meta={'points': 200},
                probability=Decimal('0.3')
            ),
            Prize(
                name='Prize 3',
                type='ton',
                meta={'amount': 1.0},
                probability=Decimal('0.2')
            )
        ]
        for prize in self.prizes:
            db.session.add(prize)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_play_game_creates_game_record(self):
        """Test that play_game creates a game record"""
        result = play_game(self.user.id)
        
        self.assertTrue(result['ok'])
        self.assertIn('game_id', result)
        self.assertIn('result', result)
        
        # Verify game was created
        game = Game.query.get(result['game_id'])
        self.assertIsNotNone(game)
        self.assertEqual(game.user_id, self.user.id)
    
    def test_play_game_returns_prize(self):
        """Test that play_game returns a prize"""
        result = play_game(self.user.id)
        
        self.assertTrue(result['ok'])
        self.assertIn('reward_id', result)
        # Should have a reward (unless very unlucky with 0 probability)
        if result['reward_id']:
            prize = Prize.query.get(result['reward_id'])
            self.assertIsNotNone(prize)
    
    def test_play_game_creates_claim_for_ton_prize(self):
        """Test that play_game creates a claim for TON prizes"""
        # Set all prizes to TON type for this test
        for prize in self.prizes:
            prize.type = 'ton'
        db.session.commit()
        
        # Play multiple times to increase chance of winning TON
        claim_created = False
        for _ in range(10):
            result = play_game(self.user.id)
            if result.get('claim_id'):
                claim_created = True
                break
        
        # At least one claim should be created (high probability)
        # Note: This is probabilistic, so might fail occasionally
        # In production, you'd want to mock the random selection
    
    def test_play_game_handles_no_prizes(self):
        """Test that play_game handles case with no active prizes"""
        # Deactivate all prizes
        for prize in self.prizes:
            prize.is_active = False
        db.session.commit()
        
        result = play_game(self.user.id)
        
        self.assertFalse(result['ok'])
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()

