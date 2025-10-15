# Digital Lost ID Card Recovery System

A **Flask-based web application** for managing lost and found ID cards with secure admin verification and automatic email notifications via SMTP.

---

## 🚀 Features

- **Report Lost ID** – Users can report lost ID cards with photos and details  
- **Report Found ID** – Finders can report found ID cards to help return them  
- **Admin Dashboard** – Secure admin interface for verifying and matching reports  
- **Search & Filter** – Advanced filtering by status, type, and search terms  
- **Status Tracking** – Track reports through stages (*Reported → Verified → Matched → Recovered*)  
- **Photo Upload** – Upload and manage ID card photos securely  
- **Automatic Matching** – Suggests potential matches between lost and found reports  
- **Email Notifications** – Sends automatic alerts via SMTP when matches are made  

---

## 🧩 Technology Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Flask (Python) |
| **Database** | SQLite (SQLAlchemy ORM) – for development |
| **Authentication** | Flask-Login |
| **Security** | Flask-WTF (CSRF Protection) |
| **Frontend** | Bootstrap 5 |
| **File Uploads** | Werkzeug |
| **Image Processing** | Pillow |
| **Email Service** | SMTP (Gmail or any SMTP server) |

---

## ⚙️ Setup Instructions

### 🖥️ Local Development

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Database**

   ```bash
   python app.py
   ```
   Visit `/init-db` in your browser to create the database and default admin user.

3. **Run the Application**

   ```bash
   python app.py
   ```

***

### 🔐 Default Admin Credentials

```
Username: admin
Password: admin123
```
⚠️ Change the default password immediately after your first login.

***

## ☁️ Google App Engine Deployment

1. Install Google Cloud SDK.
2. Update `app.yaml` with your production secret key.
3. Deploy to App Engine:

   ```bash
   gcloud app deploy
   ```

4. Initialize the database by visiting:

   ```
   https://your-app.appspot.com/init-db
   ```

***

## 🧭 Usage Guide

### 👤 For Users

- Go to “Report Lost ID” to submit details with a photo.
- Go to “Report Found ID” to upload found ID details.
- Track your report status directly through the platform.

### 🔐 For Admins

- Login at `/login` using admin credentials.
- Verify reports for authenticity.
- Match verified lost and found reports.
- Mark reports as “Recovered” after confirmation.

***

## ✉️ Email Notification Setup (SMTP)

The system automatically sends emails when a lost and found report are matched.

#### Configuration Steps

1. Enable “Less Secure Apps” or create an App Password (for Gmail).
2. Add these environment variables or include them in a `.env` file:

   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   SENDER_EMAIL=your_email@gmail.com
   SENDER_NAME="Digital ID Recovery System"
   ```

Emails sent to:
- The owner of the lost ID
- The person who found the ID

💡 Works with any SMTP-compatible provider (Gmail, Outlook, Zoho Mail, etc.)

***

## 🔒 Security Features

- CSRF Protection – Secured forms via Flask-WTF tokens
- Password Hashing – Safe credential storage using Werkzeug
- Session Management – Managed via Flask-Login
- File Upload Validation – Type and size restrictions
- Access Control – Admin-only restricted routes
- Environment-based Secrets – Sensitive credentials stored securely

***

## 🧱 Production Deployment Notes

⚠️ SQLite and local file storage are **not ideal for production**.

For cloud deployment:
- **Database:** Use Cloud SQL (PostgreSQL)
- **File Storage:** Use Google Cloud Storage

Refer to `DEPLOYMENT.md` for detailed instructions.

***

## 🔄 Status Workflow

| Stage     | Description                            |
|-----------|----------------------------------------|
| Reported  | User submits lost/found report         |
| Verified  | Admin validates authenticity           |
| Matched   | System/admin links related reports     |
| Recovered | ID successfully returned to owner      |

***

## 📁 Project Structure

```
.
├── app.py                  # Main Flask app
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── report_lost.html
│   ├── report_found.html
│   ├── admin_dashboard.html
│   ├── verify_lost.html
│   └── verify_found.html
├── static/                 # Static assets
│   ├── css/
│   ├── js/
│   └── uploads/            # Uploaded photos
├── requirements.txt        # Python dependencies
├── app.yaml                # GAE configuration
└── .gcloudignore           # GCP ignore file
```

***

## 🔧 Environment Variables

| Variable        | Description                                |
|-----------------|--------------------------------------------|
| SESSION_SECRET  | Secret key for session management          |
| SMTP_SERVER     | SMTP server host (e.g., smtp.gmail.com)    |
| SMTP_PORT       | SMTP port (e.g., 587)                      |
| SMTP_USERNAME   | Email address for SMTP login               |
| SMTP_PASSWORD   | Email password or app password             |
| SENDER_EMAIL    | Sender email address                       |
| SENDER_NAME     | Display name for the sender                |

***

## 📜 License

© 2025 Digital Lost ID Card Recovery System. All rights reserved.

***


```
