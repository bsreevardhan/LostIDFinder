import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///id_recovery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Absolute path to uploads folder inside app/static/uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ensure folder exists

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Lost ID Finder', os.getenv('MAIL_USERNAME'))
    SENDER_NAME = 'Lost ID Finder System'
