import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import LostReport, FoundReport
from app.utils.email_utils import send_email_notification

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard',endpoint='admin_dashboard')
@login_required
def dashboard():
    """Admin dashboard with filters and search"""
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

    return render_template('admin_dashboard.html',
                           lost_reports=lost_reports,
                           found_reports=found_reports)


@admin_bp.route('/verify-lost/<int:report_id>', methods=['GET', 'POST'])
@login_required
def verify_lost(report_id):
    """Verify or match a lost ID report"""
    report = LostReport.query.get_or_404(report_id)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'verify':
            report.status = 'verified'
            flash('Lost report verified successfully!', 'success')

        elif action == 'match':
            found_id = request.form.get('found_report_id')
            if found_id:
                found_report = FoundReport.query.get(int(found_id))
                if found_report:
                    # update statuses
                    report.matched_with = found_report.id
                    found_report.matched_with = report.id
                    report.status = found_report.status = 'matched'

                    # email notifications
                    subject_owner = "Good News! Your Lost ID Card Has Been Found"
                    msg_owner = f"""
                    <p>Dear {report.reporter_name},</p>
                    <p>Your lost <strong>{report.id_type}</strong> has been found!</p>
                    <p><strong>ID Number:</strong> {report.id_number}</p>
                    <p><strong>Found Location:</strong> {found_report.location_found or 'N/A'}</p>
                    <p>Our admin team will contact you soon for recovery details.</p>
                    """

                    send_email_notification(report.reporter_email, report.reporter_name, subject_owner, msg_owner)

                    subject_finder = "Thank You for Reporting a Found ID Card"
                    msg_finder = f"""
                    <p>Dear {found_report.finder_name},</p>
                    <p>The ID card you reported has been successfully matched with its owner!</p>
                    <p><strong>ID Type:</strong> {found_report.id_type}</p>
                    <p>Our admin team will contact you soon to arrange return.</p>
                    """

                    send_email_notification(found_report.finder_email, found_report.finder_name, subject_finder, msg_finder)
                    flash('Lost and Found reports matched successfully!', 'success')

        elif action == 'recovered':
            report.status = 'recovered'
            flash('Report marked as recovered!', 'success')

        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    potential_matches = FoundReport.query.filter(
        FoundReport.status.in_(['reported', 'verified']),
        db.or_(
            FoundReport.id_number == report.id_number,
            FoundReport.owner_name.contains(report.owner_name)
        )
    ).all()

    return render_template('verify_lost.html', report=report, potential_matches=potential_matches)


@admin_bp.route('/verify-found/<int:report_id>', methods=['GET', 'POST'])
@login_required
def verify_found(report_id):
    """Verify or match a found ID report"""
    report = FoundReport.query.get_or_404(report_id)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'verify':
            report.status = 'verified'
            flash('Found report verified successfully!', 'success')

        elif action == 'match':
            lost_id = request.form.get('lost_report_id')
            if lost_id:
                lost_report = LostReport.query.get(int(lost_id))
                if lost_report:
                    report.matched_with = lost_report.id
                    lost_report.matched_with = report.id
                    report.status = lost_report.status = 'matched'

                    subject_owner = "Good News! Your Lost ID Card Has Been Found"
                    msg_owner = f"""
                    <p>Dear {lost_report.reporter_name},</p>
                    <p>Your lost <strong>{lost_report.id_type}</strong> has been found!</p>
                    <p><strong>ID Number:</strong> {lost_report.id_number}</p>
                    <p><strong>Found Location:</strong> {report.location_found or 'N/A'}</p>
                    """

                    send_email_notification(lost_report.reporter_email, lost_report.reporter_name, subject_owner, msg_owner)

                    subject_finder = "Thank You for Reporting a Found ID Card"
                    msg_finder = f"""
                    <p>Dear {report.finder_name},</p>
                    <p>The ID card you found has been matched with its owner!</p>
                    <p><strong>ID Type:</strong> {report.id_type}</p>
                    """

                    send_email_notification(report.finder_email, report.finder_name, subject_finder, msg_finder)
                    flash('Reports matched successfully!', 'success')

        elif action == 'recovered':
            report.status = 'recovered'
            flash('Report marked as recovered!', 'success')

        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    potential_matches = LostReport.query.filter(
        LostReport.status.in_(['reported', 'verified']),
        db.or_(
            LostReport.id_number == report.id_number,
            LostReport.owner_name.contains(report.owner_name)
        )
    ).all()

    return render_template('verify_found.html', report=report, potential_matches=potential_matches)
