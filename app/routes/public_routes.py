import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from datetime import datetime
from app import db
from app.models import LostReport, FoundReport
from app.utils.file_utils import save_uploaded_file
from config import Config

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@public_bp.route('/report-lost', methods=['GET', 'POST'])
def report_lost():
    """Allow user to report a lost ID"""
    if request.method == 'POST':
        photo = request.files.get('photo')
        # Save file and get only the filename
        photo_filename = save_uploaded_file(photo, prefix='lost')  # ✅ store only filename

        date_lost = None
        if request.form.get('date_lost'):
            date_lost = datetime.strptime(request.form.get('date_lost'), '%Y-%m-%d').date()

        lost_report = LostReport(
            reporter_name=request.form.get('reporter_name'),
            reporter_email=request.form.get('reporter_email'),
            reporter_phone=request.form.get('reporter_phone'),
            id_number=request.form.get('id_number'),
            id_type=request.form.get('id_type'),
            owner_name=request.form.get('owner_name'),
            description=request.form.get('description'),
            photo_path=photo_filename,  # ✅ store only filename
            date_lost=date_lost,
            location_lost=request.form.get('location_lost')
        )

        db.session.add(lost_report)
        db.session.commit()
        flash('Lost ID report submitted successfully! We will contact you if it is found.', 'success')
        return redirect(url_for('public.index'))

    return render_template('report_lost.html')


@public_bp.route('/report-found', methods=['GET', 'POST'])
def report_found():
    """Allow user to report a found ID"""
    if request.method == 'POST':
        photo = request.files.get('photo')
        photo_path = save_uploaded_file(photo, prefix='found')
        date_found = None
        if request.form.get('date_found'):
            date_found = datetime.strptime(request.form.get('date_found'), '%Y-%m-%d').date()
        
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
        return redirect(url_for('public.index'))

    return render_template('report_found.html')



@public_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

