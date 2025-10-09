# Digital Lost ID Card Recovery System

## Project Overview

A Flask-based web application designed to streamline the process of recovering lost ID cards (student/staff). The system allows users to report lost IDs and finders to report found IDs, while administrators can verify reports and match them to facilitate recovery.

## Current State

**Status**: Fully functional and ready for deployment

**Last Updated**: October 9, 2025

## Key Features Implemented

1. **Lost ID Reporting**
   - Users can report lost ID cards with detailed information
   - Photo upload support for identification
   - Contact information collection for notifications

2. **Found ID Reporting**
   - Finders can report found ID cards
   - Photo upload capability
   - Detailed description fields

3. **Admin Dashboard**
   - Secure login system with password hashing
   - View all lost and found reports
   - Search and filter functionality (by ID number, name, status, type)
   - Tabbed interface for lost vs found reports

4. **Verification System**
   - Admin can verify reports for authenticity
   - Automatic matching suggestions based on ID details
   - Manual matching capability
   - Status tracking: reported → verified → matched → recovered

5. **Photo Management**
   - Secure file upload with validation
   - Image preview in verification interface
   - Side-by-side comparison of lost/found photos

## Technology Stack

- **Backend**: Flask (Python 3.11)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: Bootstrap 5, Responsive design
- **File Storage**: Local filesystem with Pillow image processing
- **Deployment**: Google App Engine ready

## Project Architecture

### Database Models

1. **Admin**: User authentication for admin panel
2. **LostReport**: Stores lost ID card reports
3. **FoundReport**: Stores found ID card reports
4. **Relationships**: Matched reports are linked via foreign keys

### File Structure

```
/
├── app.py                      # Main Flask application
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Homepage
│   ├── login.html             # Admin login
│   ├── report_lost.html       # Lost ID form
│   ├── report_found.html      # Found ID form
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── verify_lost.html       # Lost report verification
│   └── verify_found.html      # Found report verification
├── static/
│   ├── css/                   # Custom stylesheets
│   ├── js/                    # JavaScript files
│   └── uploads/               # Uploaded photos
├── app.yaml                   # Google App Engine config
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## Configuration

### Environment Variables

- `SESSION_SECRET`: Secret key for Flask sessions (set in production)

### Default Admin Credentials

- **Username**: admin
- **Password**: admin123
- **Important**: Change password immediately after first login!

## Deployment

### Local Development

1. Run: `python app.py`
2. Initialize DB: Visit `/init-db`
3. Access: `http://localhost:5000`

### Google App Engine Deployment

1. Update `SESSION_SECRET` in `app.yaml`
2. Run: `gcloud app deploy`
3. Initialize DB: Visit `https://your-app.appspot.com/init-db`

## Workflow

The Flask app runs on port 5000 with debug mode enabled for development.

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- File upload validation (types and size)
- Admin-only access control
- CSRF protection via Flask

## User Preferences

None specified yet.

## Recent Changes

**October 9, 2025**
- Initial project setup
- Implemented core features: reporting, admin dashboard, verification
- Created responsive UI with Bootstrap 5
- Configured Google App Engine deployment
- Added search and filter functionality
- Implemented photo upload and matching system
- **Added CSRF protection using Flask-WTF** for all forms
- Created comprehensive deployment guide (DEPLOYMENT.md)
- Added security warnings for production deployment
- Documented Cloud SQL and Cloud Storage migration requirements
- **Added email notification system using Brevo API**:
  - Automatic emails to lost ID owners when matches are found
  - Thank you emails to finders
  - HTML-formatted professional notification templates
  - Free tier support (300 emails/day with Brevo)

## Future Enhancements

- SMS notifications via Twilio
- Advanced analytics dashboard
- QR code generation for quick ID lookup
- Multi-admin role management
- Database migration to PostgreSQL for production
