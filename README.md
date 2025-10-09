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
- **Email Notifications**: Automatic email alerts to lost ID owners and finders when matches are made (via Brevo API)

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM) - Development only
- **Authentication**: Flask-Login
- **Security**: Flask-WTF (CSRF Protection)
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

- **CSRF Protection**: All forms protected with Flask-WTF CSRF tokens
- **Password Security**: Secure password hashing with Werkzeug
- **Session Management**: Session-based authentication with Flask-Login
- **File Upload Validation**: Type and size validation for uploaded files
- **Access Control**: Admin-only access to verification features
- **Secret Management**: Environment-based secret key configuration

## Production Deployment

⚠️ **Important**: The current implementation uses SQLite and local file storage, which are **NOT suitable for Google App Engine Standard Environment**.

For production deployment, you **must** migrate to:
- **Database**: Cloud SQL (PostgreSQL)
- **File Storage**: Google Cloud Storage

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions and migration guide.

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
- `BREVO_API_KEY`: Brevo (Sendinblue) API key for email notifications (optional)
- `SENDER_EMAIL`: Email address to send notifications from (default: noreply@idrecovery.com)
- `SENDER_NAME`: Sender name for email notifications (default: ID Recovery System)

### Email Notification Setup

The system supports email notifications via Brevo (formerly Sendinblue) API. Brevo offers a free tier with 300 emails/day.

**To enable email notifications:**

1. Sign up for a free account at [Brevo](https://www.brevo.com/)
2. Get your API key from Settings → SMTP & API
3. Add the API key as an environment variable or secret:
   ```bash
   export BREVO_API_KEY=your_api_key_here
   ```
4. (Optional) Configure sender email and name:
   ```bash
   export SENDER_EMAIL=your-email@example.com
   export SENDER_NAME="Your Organization"
   ```

**Note**: Email notifications are automatically sent when:
- Lost and found reports are successfully matched
- Both the lost ID owner and the finder receive notification emails

## License

© 2025 Digital ID Recovery System. All rights reserved.
