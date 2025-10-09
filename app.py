import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///id_recovery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/report-lost', methods=['GET', 'POST'])
def report_lost():
    if request.method == 'POST':
        photo = request.files.get('photo')
        photo_path = None
        
        if photo and allowed_file(photo.filename):
            filename = secure_filename(f"lost_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.filename}")
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
        
        date_lost = datetime.strptime(request.form.get('date_lost'), '%Y-%m-%d').date() if request.form.get('date_lost') else None
        
        lost_report = LostReport(
            reporter_name=request.form.get('reporter_name'),
            reporter_email=request.form.get('reporter_email'),
            reporter_phone=request.form.get('reporter_phone'),
            id_number=request.form.get('id_number'),
            id_type=request.form.get('id_type'),
            owner_name=request.form.get('owner_name'),
            description=request.form.get('description'),
            photo_path=photo_path,
            date_lost=date_lost,
            location_lost=request.form.get('location_lost')
        )
        
        db.session.add(lost_report)
        db.session.commit()
        
        flash('Lost ID report submitted successfully! We will contact you if it is found.', 'success')
        return redirect(url_for('index'))
    
    return render_template('report_lost.html')

@app.route('/report-found', methods=['GET', 'POST'])
def report_found():
    if request.method == 'POST':
        photo = request.files.get('photo')
        photo_path = None
        
        if photo and allowed_file(photo.filename):
            filename = secure_filename(f"found_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.filename}")
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
        
        date_found = datetime.strptime(request.form.get('date_found'), '%Y-%m-%d').date() if request.form.get('date_found') else None
        
        found_report = FoundReport(
            finder_name=request.form.get('finder_name'),
            finder_email=request.form.get('finder_email'),
            finder_phone=request.form.get('finder_phone'),
            id_number=request.form.get('id_number'),
            id_type=request.form.get('id_type'),
            owner_name=request.form.get('owner_name'),
            description=request.form.get('description'),
            photo_path=photo_path,
            date_found=date_found,
            location_found=request.form.get('location_found')
        )
        
        db.session.add(found_report)
        db.session.commit()
        
        flash('Found ID report submitted successfully! Thank you for helping.', 'success')
        return redirect(url_for('index'))
    
    return render_template('report_found.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    search_query = request.args.get('search', '')
    filter_status = request.args.get('status', '')
    filter_type = request.args.get('type', '')
    
    lost_query = LostReport.query
    found_query = FoundReport.query
    
    if search_query:
        lost_query = lost_query.filter(
            db.or_(
                LostReport.id_number.contains(search_query),
                LostReport.owner_name.contains(search_query),
                LostReport.reporter_name.contains(search_query)
            )
        )
        found_query = found_query.filter(
            db.or_(
                FoundReport.id_number.contains(search_query),
                FoundReport.owner_name.contains(search_query),
                FoundReport.finder_name.contains(search_query)
            )
        )
    
    if filter_status:
        lost_query = lost_query.filter_by(status=filter_status)
        found_query = found_query.filter_by(status=filter_status)
    
    if filter_type:
        lost_query = lost_query.filter_by(id_type=filter_type)
        found_query = found_query.filter_by(id_type=filter_type)
    
    lost_reports = lost_query.order_by(LostReport.date_reported.desc()).all()
    found_reports = found_query.order_by(FoundReport.date_reported.desc()).all()
    
    return render_template('admin_dashboard.html', lost_reports=lost_reports, found_reports=found_reports)

@app.route('/admin/verify-lost/<int:report_id>', methods=['GET', 'POST'])
@login_required
def verify_lost(report_id):
    report = LostReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'verify':
            report.status = 'verified'
            flash('Lost report verified successfully!', 'success')
        elif action == 'match':
            found_id = request.form.get('found_report_id')
            if found_id:
                report.matched_with = int(found_id)
                report.status = 'matched'
                found_report = FoundReport.query.get(int(found_id))
                if found_report:
                    found_report.matched_with = report_id
                    found_report.status = 'matched'
                flash('Reports matched successfully!', 'success')
        elif action == 'recovered':
            report.status = 'recovered'
            flash('Report marked as recovered!', 'success')
        
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    potential_matches = FoundReport.query.filter(
        FoundReport.status.in_(['reported', 'verified']),
        db.or_(
            FoundReport.id_number == report.id_number,
            FoundReport.owner_name.contains(report.owner_name)
        )
    ).all()
    
    return render_template('verify_lost.html', report=report, potential_matches=potential_matches)

@app.route('/admin/verify-found/<int:report_id>', methods=['GET', 'POST'])
@login_required
def verify_found(report_id):
    report = FoundReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'verify':
            report.status = 'verified'
            flash('Found report verified successfully!', 'success')
        elif action == 'match':
            lost_id = request.form.get('lost_report_id')
            if lost_id:
                report.matched_with = int(lost_id)
                report.status = 'matched'
                lost_report = LostReport.query.get(int(lost_id))
                if lost_report:
                    lost_report.matched_with = report_id
                    lost_report.status = 'matched'
                flash('Reports matched successfully!', 'success')
        elif action == 'recovered':
            report.status = 'recovered'
            flash('Report marked as recovered!', 'success')
        
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    potential_matches = LostReport.query.filter(
        LostReport.status.in_(['reported', 'verified']),
        db.or_(
            LostReport.id_number == report.id_number,
            LostReport.owner_name.contains(report.owner_name)
        )
    ).all()
    
    return render_template('verify_found.html', report=report, potential_matches=potential_matches)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/init-db')
def init_db():
    with app.app_context():
        db.create_all()
        
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@idrecovery.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            return 'Database initialized! Default admin created (username: admin, password: admin123)'
        
        return 'Database already initialized!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
