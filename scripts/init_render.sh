#!/bin/bash
# Initialization script for Render deployment
# This runs after the build to set up the database

echo "Initializing database..."

# Wait for database to be ready
sleep 2

# Initialize database tables
python -c "
from app import create_app
from app.models import db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"

# Seed initial data
python scripts/seed_data.py

echo "Database initialization complete!"

