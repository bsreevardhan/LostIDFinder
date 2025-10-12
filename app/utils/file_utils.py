import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, prefix='file'):
    """Save uploaded file to UPLOAD_FOLDER and return filename only"""
    if not file or file.filename == '':
        return None

    if allowed_file(file.filename):
        # Get the absolute path from Flask config
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)  # ensure folder exists

        # Secure filename
        filename = secure_filename(f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")

        # Save the file
        file.save(os.path.join(upload_folder, filename))

        return filename  # store only the filename
    return None
