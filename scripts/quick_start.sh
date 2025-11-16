#!/bin/bash
# Quick start script for local development

echo "Setting up Crystal Game..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env and set your TELEGRAM_BOT_TOKEN and ADMIN_TOKEN"
fi

# Initialize database
echo "Initializing database..."
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"

# Seed data
echo "Seeding initial data..."
python scripts/seed_data.py

echo ""
echo "Setup complete! Run 'python run.py' to start the server."
echo "Then set up your Telegram bot with BotFather (see README.md)"

