import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the Base class
db = SQLAlchemy(model_class=Base)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "quantum_agriculture_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database, using SQLite for development
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quantum_agriculture.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'info'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    # Import models for table creation
    import models  # noqa: F401
    
    # Create all tables
    db.create_all()
    
    # Create admin user if it doesn't exist
    from werkzeug.security import generate_password_hash
    admin_email = 'farmhub04@gmail.com'
    
    # First check by email
    admin = User.query.filter_by(email=admin_email).first()
    
    # If not found by email, check for existing admin user
    admin_user = User.query.filter_by(username='admin').first()
    
    if admin:
        # Email exists, make sure it's an admin
        if not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
            logging.info(f'User {admin_email} set as admin')
    elif admin_user:
        # Username 'admin' exists but with a different email
        admin_user.email = admin_email
        admin_user.is_admin = True
        db.session.commit()
        logging.info(f'Admin user updated with email {admin_email}')
    else:
        # Create new admin user
        admin = User(
            username='farmhub_admin',
            email=admin_email,
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            first_name='Admin',
            last_name='User',
            city='Coimbatore',
            state='Tamil Nadu'
        )
        db.session.add(admin)
        db.session.commit()
        logging.info('Admin user created successfully')
