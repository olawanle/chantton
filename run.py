#!/usr/bin/env python3
"""
Main entry point for the Flask application
"""
from app import create_app
from app.config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    # For production, use gunicorn instead
    if os.environ.get('FLASK_ENV') == 'production':
        print("Running in production mode. Use gunicorn to start the server.")
        print("Command: gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'")
    else:
        app.run(host='0.0.0.0', port=port, debug=debug)

