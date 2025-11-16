#!/usr/bin/env python3
"""
Render initialization script
Run this after deployment to initialize the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db

def init_database():
    """Initialize database tables and seed data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Import and run seed data
        try:
            from scripts.seed_data import seed_data
            print("Seeding initial data...")
            seed_data()
            print("✓ Seed data loaded")
        except Exception as e:
            print(f"Warning: Could not seed data: {e}")
        
        print("\n✓ Database initialization complete!")

if __name__ == '__main__':
    init_database()

