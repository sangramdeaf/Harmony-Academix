import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
# Render gives DATABASE_URL like `postgres://...` — SQLAlchemy expects `postgresql://`
database_url = os.environ.get("DATABASE_URL", "sqlite:///harmony_hands.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
# If your login route is defined as @app.route('/login') then keep 'login' here.
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = 'कृपया प्रवेश करा / Please login to access this page.'

@login_manager.user_loader
def load_user(user_id):
    # Import inside function to avoid circular import problems
    try:
        from models import User
        return User.query.get(int(user_id))
    except Exception as e:
        logger.exception("Error loading user: %s", e)
        return None

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with app.app_context():
    # Import models to ensure tables are created
    try:
        import models  # noqa: F401
    except Exception as e:
        logger.warning("Could not import models module: %s", e)

    # Optional skip flag if you want to run migrations manually
    skip_create = os.environ.get('SKIP_DB_CREATE', '').lower() in ('1', 'true', 'yes')
    if not skip_create:
        try:
            db.create_all()
            logger.info("Database tables created/ensured")
        except Exception as e:
            logger.exception("db.create_all() failed: %s", e)
    else:
        logger.info("SKIP_DB_CREATE set — skipping db.create_all()")

# Import routes at module level safely. Use plain import (not `from routes import *`)
# If your routes.py uses @app.route directly it will work because `app` is already defined.
try:
    import routes  # executes routes and registers routes decorated with @app.route
    logger.info("routes module imported")
except Exception as e:
    logger.exception("Could not import routes: %s", e)
