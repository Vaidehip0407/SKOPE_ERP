# Deployment Guide

This guide covers deploying the Retail Management System to production.

## 📋 Pre-Deployment Checklist

### Security
- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Review and restrict API access

### Database
- [ ] Use PostgreSQL for production
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Test database migrations

### Environment
- [ ] Set production environment variables
- [ ] Disable debug mode
- [ ] Configure logging
- [ ] Set up monitoring

## 🐳 Docker Deployment (Recommended)

### Create Dockerfile for Backend

`backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for Frontend

`frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: rms_db
      POSTGRES_USER: rms_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - rms_network

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://rms_user:${DB_PASSWORD}@db:5432/rms_db
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
    networks:
      - rms_network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - rms_network

volumes:
  postgres_data:

networks:
  rms_network:
    driver: bridge
```

### Deploy with Docker Compose

```bash
# Create .env file
echo "DB_PASSWORD=your-secure-password" > .env
echo "SECRET_KEY=your-secret-key" >> .env

# Build and start services
docker-compose up -d

# Initialize database
docker-compose exec backend python init_db.py

# View logs
docker-compose logs -f
```

## 🖥️ Traditional Server Deployment

### Backend Deployment (Linux)

#### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y
```

#### 2. Setup PostgreSQL

```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE rms_db;
CREATE USER rms_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE rms_db TO rms_user;
\q
EOF
```

#### 3. Deploy Backend

```bash
# Create application directory
sudo mkdir -p /opt/rms/backend
cd /opt/rms/backend

# Copy files
sudo cp -r /path/to/backend/* .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://rms_user:your-secure-password@localhost:5432/rms_db
SECRET_KEY=your-generated-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# Initialize database
python init_db.py
```

#### 4. Create Systemd Service

`/etc/systemd/system/rms-backend.service`:
```ini
[Unit]
Description=RMS Backend API
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/rms/backend
Environment="PATH=/opt/rms/backend/venv/bin"
ExecStart=/opt/rms/backend/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable rms-backend
sudo systemctl start rms-backend
sudo systemctl status rms-backend
```

### Frontend Deployment

#### 1. Build Frontend

```bash
cd frontend
npm install
npm run build
```

#### 2. Deploy with Nginx

```bash
# Install Nginx
sudo apt install nginx -y

# Copy build files
sudo mkdir -p /var/www/rms
sudo cp -r dist/* /var/www/rms/
```

#### 3. Configure Nginx

`/etc/nginx/sites-available/rms`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/rms;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/rms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Enable HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## ☁️ Cloud Platform Deployment

### AWS Deployment

#### Using Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
cd backend
eb init -p python-3.11 rms-backend
```

3. Create environment:
```bash
eb create rms-prod
```

4. Deploy:
```bash
eb deploy
```

### Google Cloud Platform

#### Using Cloud Run

1. Install gcloud CLI

2. Build and push container:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/rms-backend
```

3. Deploy:
```bash
gcloud run deploy rms-backend \
  --image gcr.io/PROJECT_ID/rms-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

1. Install Heroku CLI

2. Create Procfile:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

3. Deploy:
```bash
heroku create rms-app
git push heroku main
heroku run python init_db.py
```

## 🔒 Security Hardening

### Backend Security

1. **Environment Variables**
```bash
# Use strong SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Database Security**
- Use SSL connections
- Restrict database access by IP
- Regular backups
- Encrypted passwords

3. **API Security**
- Enable rate limiting
- Use HTTPS only
- Implement API versioning
- Log all access

### Frontend Security

1. **Content Security Policy**
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

2. **Security Headers**
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
```

## 📊 Monitoring

### Application Monitoring

Install monitoring tools:
```bash
pip install prometheus-client
```

### Database Monitoring

```bash
# PostgreSQL monitoring
sudo apt install postgresql-contrib
```

### Log Management

Configure centralized logging:
```python
# backend/app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10000000,
    backupCount=10
)
```

## 🔄 Backup Strategy

### Database Backups

Create backup script `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -U rms_user rms_db > $BACKUP_DIR/rms_backup_$TIMESTAMP.sql
# Keep only last 30 days
find $BACKUP_DIR -name "rms_backup_*.sql" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /opt/rms/backup.sh
```

## 🚀 CI/CD Pipeline

### GitHub Actions Example

`.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          # Your deployment commands
          
      - name: Deploy Frontend
        run: |
          cd frontend
          npm install
          npm run build
          # Deploy to hosting
```

## 📝 Post-Deployment

### 1. Verify Deployment
- [ ] Check API health endpoint
- [ ] Test login functionality
- [ ] Verify database connectivity
- [ ] Test all major features

### 2. Monitor Performance
- [ ] Set up monitoring dashboards
- [ ] Configure alerts
- [ ] Review logs regularly

### 3. Documentation
- [ ] Update deployment documentation
- [ ] Document any custom configurations
- [ ] Create runbooks for common issues

## 🆘 Troubleshooting

### Common Issues

**Issue**: Database connection failed
**Solution**: Check DATABASE_URL, network connectivity, and PostgreSQL service status

**Issue**: 502 Bad Gateway
**Solution**: Check backend service status, logs, and Nginx configuration

**Issue**: Static files not loading
**Solution**: Verify Nginx configuration and file permissions

### Rollback Procedure

1. Stop services
2. Restore database backup
3. Deploy previous version
4. Restart services
5. Verify functionality

## 📞 Support

For deployment issues:
- Check logs: `journalctl -u rms-backend -f`
- Review Nginx logs: `/var/log/nginx/error.log`
- Database logs: `/var/log/postgresql/`

---

**Important**: Always test deployment procedures in a staging environment before production!

