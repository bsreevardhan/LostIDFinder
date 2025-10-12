from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import Config
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()  # create instance

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)  # 🔹 Important!

    from app.routes.public_routes import public_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    return app
