# Google App Engine Deployment Guide

## Important: Production Deployment Considerations

### Current Limitations with Standard Environment

The current implementation uses SQLite database and local file storage, which are **not suitable for Google App Engine Standard Environment** due to the following reasons:

1. **Ephemeral Filesystem**: GAE Standard has a read-only filesystem, so SQLite database and uploaded files will be lost on restart
2. **No Persistent Storage**: Local file uploads in `static/uploads` won't persist across instances

### Recommended Production Setup

For production deployment on Google App Engine, you **must** migrate to managed services:

#### 1. Database Migration (Required)

Replace SQLite with **Cloud SQL (PostgreSQL)**:

```python
# Update app.py configuration
import os

# For production
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_socket_dir = os.environ.get('DB_SOCKET_DIR', '/cloudsql')
cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

if os.environ.get('GAE_ENV', '').startswith('standard'):
    # Production on GAE
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host={db_socket_dir}/{cloud_sql_connection_name}'
else:
    # Local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///id_recovery.db'
```

**Setup Steps**:
1. Create Cloud SQL instance:
   ```bash
   gcloud sql instances create id-recovery-db --database-version=POSTGRES_14 --tier=db-f1-micro --region=us-central1
   ```

2. Create database:
   ```bash
   gcloud sql databases create idrecovery --instance=id-recovery-db
   ```

3. Create user:
   ```bash
   gcloud sql users create dbuser --instance=id-recovery-db --password=your-secure-password
   ```

4. Update `app.yaml`:
   ```yaml
   env_variables:
     DB_USER: 'dbuser'
     DB_PASS: 'your-secure-password'
     DB_NAME: 'idrecovery'
     CLOUD_SQL_CONNECTION_NAME: 'your-project:us-central1:id-recovery-db'
     SESSION_SECRET: 'your-production-secret-key'
   
   beta_settings:
     cloud_sql_instances: 'your-project:us-central1:id-recovery-db'
   ```

5. Install psycopg2 for PostgreSQL:
   ```bash
   pip install psycopg2-binary
   ```

#### 2. File Storage Migration (Required)

Replace local file storage with **Google Cloud Storage**:

```python
# Update app.py with Cloud Storage
from google.cloud import storage
import os

storage_client = storage.Client()
bucket_name = os.environ.get('GCS_BUCKET_NAME', 'id-recovery-uploads')

def upload_to_gcs(file, filename):
    """Upload file to Google Cloud Storage"""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return blob.public_url

def get_gcs_url(filename):
    """Get public URL for file in GCS"""
    return f'https://storage.googleapis.com/{bucket_name}/{filename}'

# Update report routes to use GCS
@app.route('/report-lost', methods=['POST'])
def report_lost():
    photo = request.files.get('photo')
    photo_url = None
    
    if photo and allowed_file(photo.filename):
        filename = secure_filename(f"lost_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.filename}")
        photo_url = upload_to_gcs(photo, filename)
    
    # Store photo_url in database instead of local path
    # ...
```

**Setup Steps**:
1. Create GCS bucket:
   ```bash
   gsutil mb gs://your-project-id-recovery-uploads
   ```

2. Make bucket public (or use signed URLs for better security):
   ```bash
   gsutil iam ch allUsers:objectViewer gs://your-project-id-recovery-uploads
   ```

3. Install Cloud Storage library:
   ```bash
   pip install google-cloud-storage
   ```

4. Update `app.yaml`:
   ```yaml
   env_variables:
     GCS_BUCKET_NAME: 'your-project-id-recovery-uploads'
   ```

### Security Enhancements

#### 1. CSRF Protection (✓ Implemented)

CSRF protection is now enabled using Flask-WTF. All forms include CSRF tokens.

#### 2. File Upload Security

Add content type validation using Pillow:

```python
from PIL import Image
import io

def validate_image(file):
    """Validate that uploaded file is actually an image"""
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)  # Reset file pointer
        return True
    except:
        return False

# Update upload handlers
if photo and allowed_file(photo.filename) and validate_image(photo):
    # Process upload
```

#### 3. Environment Variables

Always use environment variables for sensitive data:

```bash
# Set secrets
gcloud secrets create session-secret --data-file=-
gcloud secrets create db-password --data-file=-
```

Update `app.yaml` to use Secret Manager:
```yaml
env_variables:
  SESSION_SECRET: 'projects/PROJECT_ID/secrets/session-secret/versions/latest'
```

### Deployment Checklist

- [ ] Migrate SQLite to Cloud SQL (PostgreSQL)
- [ ] Migrate local file storage to Cloud Storage
- [ ] Add image content validation with Pillow
- [ ] Update `app.yaml` with all environment variables
- [ ] Change default admin password
- [ ] Set strong SESSION_SECRET
- [ ] Test file uploads with Cloud Storage
- [ ] Test database persistence
- [ ] Configure auto-scaling parameters
- [ ] Set up Cloud Logging and Monitoring
- [ ] Enable Cloud Armor for DDoS protection
- [ ] Configure custom domain (optional)

### Deployment Commands

```bash
# Deploy application
gcloud app deploy

# View logs
gcloud app logs tail -s default

# Access application
gcloud app browse

# Initialize database (one-time)
curl https://your-app.appspot.com/init-db
```

### Alternative: Google App Engine Flexible Environment

If you prefer to keep SQLite and local storage (not recommended for production), consider using App Engine Flexible:

```yaml
# app.yaml for Flexible Environment
runtime: python
env: flex
runtime_config:
  python_version: 3.11

env_variables:
  SESSION_SECRET: 'your-secret-key'

resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10
```

**Note**: Flexible environment is more expensive but provides a persistent disk.

### Cost Considerations

- **Cloud SQL**: ~$7-25/month (db-f1-micro)
- **Cloud Storage**: $0.026/GB/month + operations
- **App Engine Standard**: Free tier available, then ~$0.05/hour
- **App Engine Flexible**: ~$50-100/month (always running)

### Local Development vs Production

The application automatically detects the environment:

```python
if os.environ.get('GAE_ENV', '').startswith('standard'):
    # Production configuration
else:
    # Local development configuration
```

This allows seamless development with SQLite locally while using Cloud SQL in production.
