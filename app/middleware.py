"""
Production middleware for security and error handling
"""
from flask import request, jsonify, g
from functools import wraps
import time
import logging
from app.config import Config

logger = logging.getLogger(__name__)

def setup_security_headers(app):
    """Add security headers to all responses"""
    @app.after_request
    def set_security_headers(response):
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Only add HSTS in production with HTTPS
        if not app.debug and request.is_secure:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # CSP for Telegram WebApp
        if request.path.startswith('/admin'):
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://telegram.org; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
        else:
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://telegram.org; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.telegram.org;"
        
        return response

def rate_limit(max_per_minute=60):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple in-memory rate limiting (use Redis in production)
            if not hasattr(g, 'rate_limit_store'):
                g.rate_limit_store = {}
            
            client_id = request.remote_addr
            current_time = time.time()
            
            if client_id in g.rate_limit_store:
                requests, last_reset = g.rate_limit_store[client_id]
                if current_time - last_reset > 60:  # Reset every minute
                    g.rate_limit_store[client_id] = [1, current_time]
                else:
                    requests += 1
                    if requests > max_per_minute:
                        logger.warning(f"Rate limit exceeded for {client_id}")
                        return jsonify({'error': 'Rate limit exceeded'}), 429
                    g.rate_limit_store[client_id] = [requests, last_reset]
            else:
                g.rate_limit_store[client_id] = [1, current_time]
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def setup_logging(app):
    """Configure logging for production"""
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

def setup_error_handlers(app):
    """Setup error handlers"""
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/') or request.accept_mimetypes.accept_json:
            return jsonify({'error': 'Not found'}), 404
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}', exc_info=True)
        if request.path.startswith('/api/') or request.accept_mimetypes.accept_json:
            return jsonify({'error': 'Internal server error'}), 500
        from flask import render_template
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        if request.path.startswith('/api/') or request.accept_mimetypes.accept_json:
            return jsonify({'error': 'Forbidden'}), 403
        from flask import render_template
        return render_template('errors/403.html'), 403

