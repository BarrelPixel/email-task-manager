# Deployment Guide

This guide will help you deploy the Email Task Manager application to production.

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (for production)
- Google Cloud Platform account
- OpenAI API key

## 1. Backend Deployment

### 1.1 Environment Setup

1. **Create a production environment file** (`backend/.env`):
```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-strong-production-secret-key-here-min-32-chars

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://username:password@localhost:5432/email_task_manager

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/auth/google/callback

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Gmail API Configuration
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly

# Application Configuration
TASK_PROCESSING_INTERVAL=900  # 15 minutes in seconds
MAX_EMAILS_PER_PROCESS=50
FRONTEND_URL=https://yourdomain.com

# Security Configuration (CRITICAL - Change in production)
ENCRYPTION_SALT=your-unique-encryption-salt-change-this-in-production
```

### 1.2 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `https://yourdomain.com/api/auth/google/callback`
7. Download the credentials and update your `.env` file

### 1.3 Database Setup

1. **Install PostgreSQL**:
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

2. **Create database**:
```bash
sudo -u postgres psql
CREATE DATABASE email_task_manager;
CREATE USER email_task_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE email_task_manager TO email_task_user;
\q
```

3. **Update DATABASE_URL** in your `.env` file

### 1.4 Application Deployment

#### Option A: Using Gunicorn (Recommended)

1. **Install Gunicorn**:
```bash
pip install gunicorn
```

2. **Create Gunicorn configuration** (`backend/gunicorn.conf.py`):
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

3. **Run with Gunicorn**:
```bash
cd backend
gunicorn -c gunicorn.conf.py run:app
```

#### Option B: Using Docker

1. **Create Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]
```

2. **Build and run**:
```bash
docker build -t email-task-manager-backend .
docker run -p 5000:5000 --env-file .env email-task-manager-backend
```

## 2. Frontend Deployment

### 2.1 Build for Production

1. **Update environment variables** (`frontend/.env`):
```bash
REACT_APP_API_URL=https://yourdomain.com/api
```

2. **Build the application**:
```bash
cd frontend
npm run build
```

### 2.2 Deploy to Web Server

#### Option A: Nginx

1. **Install Nginx**:
```bash
# Ubuntu/Debian
sudo apt-get install nginx

# macOS
brew install nginx
```

2. **Configure Nginx** (`/etc/nginx/sites-available/email-task-manager`):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /path/to/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable the site**:
```bash
sudo ln -s /etc/nginx/sites-available/email-task-manager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Option B: Using Docker

1. **Create Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

2. **Create nginx.conf**:
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 3. SSL/HTTPS Setup

### 3.1 Using Let's Encrypt

1. **Install Certbot**:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Obtain SSL certificate**:
```bash
sudo certbot --nginx -d yourdomain.com
```

3. **Auto-renewal**:
```bash
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 4. Monitoring and Logging

### 4.1 Application Logs

1. **Configure logging** in `backend/app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/email_task_manager.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Email Task Manager startup')
```

### 4.2 Health Checks

1. **Health check endpoint** (included):
```bash
curl https://yourdomain.com/api/health
```

2. **Performance testing**:
```bash
# Test backend functionality
python test_app.py

# Check database indexes
python migrate_db.py
```

## 5. Security Considerations

### Critical Security Updates
1. **Token Encryption**: OAuth tokens are now encrypted in the database using PBKDF2
2. **Input Validation**: All user inputs are sanitized and validated to prevent XSS
3. **Rate Limiting**: Email processing limited to 5 requests per 5 minutes per user
4. **CORS Configuration**: Properly configured with specific allowed origins
5. **Session Security**: Secure session cookies with httpOnly and SameSite flags

### Production Security Checklist
1. **Environment Variables**: Never commit sensitive data to version control
2. **Database Security**: Use strong passwords and limit database access
3. **Encryption Keys**: Change ENCRYPTION_SALT and SECRET_KEY from defaults
4. **HTTPS**: Always use HTTPS in production
5. **Database Indexes**: Run `python migrate_db.py` to add performance indexes
6. **Monitoring**: Set up logging and monitoring for security events

### New Security Environment Variables
```bash
# Required for production security
SECRET_KEY=your-very-strong-secret-key-minimum-32-characters
ENCRYPTION_SALT=your-unique-salt-for-token-encryption
FRONTEND_URL=https://yourdomain.com
```

## 6. Backup Strategy

1. **Database Backups**:
```bash
# Create backup script
#!/bin/bash
pg_dump email_task_manager > backup_$(date +%Y%m%d_%H%M%S).sql
```

2. **Application Backups**:
- Backup configuration files
- Backup uploaded files (if any)
- Backup logs

## 7. Scaling Considerations

1. **Load Balancing**: Use multiple application instances behind a load balancer
2. **Database Scaling**: Consider read replicas for high read loads
3. **Caching**: Implement Redis for session storage and caching
4. **CDN**: Use a CDN for static assets

## 8. Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure CORS is configured for your domain
2. **Database Connection**: Check database credentials and network access
3. **OAuth Issues**: Verify redirect URIs match exactly
4. **API Errors**: Check logs for detailed error messages

### Log Locations

- Application logs: `backend/logs/email_task_manager.log`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`

## 9. Maintenance

1. **Regular Updates**: Keep dependencies updated
2. **Security Patches**: Apply security updates promptly
3. **Performance Monitoring**: Monitor application performance
4. **Backup Verification**: Regularly test backup restoration

For additional support, refer to the main README.md file or create an issue in the project repository.
