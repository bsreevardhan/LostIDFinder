from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate   # ✅ Import Flask-Migrate
from config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()   # ✅ Create Migrate instance

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)  # ✅ Initialize Flask-Migrate with app & db

    # Register blueprints
    from app.routes.public_routes import public_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    return app
