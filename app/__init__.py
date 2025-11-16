from flask import Flask
from app.config import Config
from app.database import init_db
from app.models import db
from app.middleware import setup_security_headers, setup_logging, setup_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    # Setup production features
    setup_security_headers(app)
    setup_logging(app)
    setup_error_handlers(app)
    
    with app.app_context():
        init_db()
    
    from app.routes import main, auth, game, tasks, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(admin.bp)
    
    return app

