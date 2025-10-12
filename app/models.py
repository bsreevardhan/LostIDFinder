from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LostReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_name = db.Column(db.String(100), nullable=False)
    reporter_email = db.Column(db.String(120), nullable=False)
    reporter_phone = db.Column(db.String(20))
    id_number = db.Column(db.String(50), nullable=False)
    id_type = db.Column(db.String(50), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    photo_path = db.Column(db.String(200))
    date_lost = db.Column(db.Date)
    location_lost = db.Column(db.String(200))
    status = db.Column(db.String(20), default='reported')
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    matched_with = db.Column(db.Integer, db.ForeignKey('found_report.id'), nullable=True)

class FoundReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    finder_name = db.Column(db.String(100), nullable=False)
    finder_email = db.Column(db.String(120), nullable=False)
    finder_phone = db.Column(db.String(20))
    id_number = db.Column(db.String(50))
    id_type = db.Column(db.String(50), nullable=False)
    owner_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    photo_path = db.Column(db.String(200))
    date_found = db.Column(db.Date)
    location_found = db.Column(db.String(200))
    status = db.Column(db.String(20), default='reported')
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    matched_with = db.Column(db.Integer, db.ForeignKey('lost_report.id'), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))
