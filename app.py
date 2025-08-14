import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# SQLAlchemy with a Declarative Base so models can inherit from Base
db = SQLAlchemy(model_class=Base)


def create_app():
    """Factory to create and configure the Flask app."""
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Secret (use an env var in production; fallback is intentionally development-only)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

    # If the app is behind a proxy (Render, nginx, etc.) ProxyFix helps Flask
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # DATABASE_URL compatibility: Render and some providers use postgres:// — SQLAlchemy
    # prefers postgresql:// with some drivers. Convert automatically if needed.
    database_url = os.environ.get("DATABASE_URL", "sqlite:///harmony_hands.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # File upload settings
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'कृपया प्रवेश करा / Please login to access this page.'

    @login_manager.user_loader
    def load_user(user_id):
        # Import inside function to avoid circular imports
        from models import User
        return User.query.get(int(user_id))

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # By default create tables automatically for quick deploys. You can skip this by
    # setting the SKIP_DB_CREATE env var (1/true/yes).
    with app.app_context():
        import models  # noqa: F401 (ensure models are registered)
        skip_create = os.environ.get('SKIP_DB_CREATE', '').lower() in ('1', 'true', 'yes')
        if not skip_create:
            db.create_all()
            logger.info('Database tables created/ensured')
        else:
            logger.info('SKIP_DB_CREATE set — skipping db.create_all()')

    # Import routes after extensions are initialized
    try:
        from routes import *  # noqa: E402,F401
    except Exception as e:
        logger.warning('Could not import routes: %s', e)

    return app


# Create the actual app instance used by WSGI servers (gunicorn) and Flask CLI
app = create_app()

if __name__ == '__main__':
    # Local development server
    port = int(os.environ.get('PORT', 5000))
    debug_flag = os.environ.get('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug_flag)
