# Digital Lost ID Card Recovery System

A Flask-based web application for managing lost and found ID cards with secure admin verification.

## Features

- **Report Lost ID**: Users can report lost ID cards with photos and details
- **Report Found ID**: Finders can report found ID cards to help return them
- **Admin Dashboard**: Secure admin interface for verifying and matching reports
- **Search & Filter**: Advanced filtering by status, type, and search terms
- **Status Tracking**: Track reports through stages (reported, verified, matched, recovered)
- **Photo Upload**: Support for ID card photo uploads
- **Automatic Matching**: System suggests potential matches based on ID details

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5
- **File Upload**: Werkzeug
- **Image Processing**: Pillow

## Setup Instructions

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python app.py
```
Visit `/init-db` to create the database and default admin user.

3. Run the application:
```bash
python app.py
```

Default admin credentials:
- Username: `admin`
- Password: `admin123`

**Important**: Change the default password immediately after first login!

### Google App Engine Deployment

1. Install Google Cloud SDK

2. Update `app.yaml` with your production secret key

3. Deploy to Google App Engine:
```bash
gcloud app deploy
```

4. Initialize the database by visiting:
```
https://your-app.appspot.com/init-db
```

## Usage

### For Users

1. **Report Lost ID**: Navigate to "Report Lost ID" and fill in the details with a photo
2. **Report Found ID**: Navigate to "Report Found ID" and upload the found ID card photo
3. You will be notified via the contact information provided

### For Admins

1. Login at `/login` with admin credentials
2. View all reports in the dashboard
3. Verify reports to confirm authenticity
4. Match lost and found reports
5. Mark reports as recovered once the ID is returned

## Security Features

- Secure password hashing with Werkzeug
- Session-based authentication with Flask-Login
- File upload validation
- Admin-only access to verification features
- Environment-based secret key configuration

## Status Workflow

1. **Reported**: Initial submission by user
2. **Verified**: Admin confirms report authenticity
3. **Matched**: Lost and found reports are matched
4. **Recovered**: ID successfully returned to owner

## File Structure

```
.
├── app.py                  # Main application file
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── report_lost.html
│   ├── report_found.html
│   ├── admin_dashboard.html
│   ├── verify_lost.html
│   └── verify_found.html
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   └── uploads/           # Uploaded photos
├── requirements.txt        # Python dependencies
├── app.yaml               # Google App Engine config
└── .gcloudignore          # GCP deployment ignore file
```

## Environment Variables

- `SESSION_SECRET`: Secret key for session management (set in production)

## License

© 2025 Digital ID Recovery System. All rights reserved.
