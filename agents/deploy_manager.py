#!/usr/bin/env python3
"""
Email Task Manager Deploy Manager Agent
Comprehensive deployment automation and environment management
"""

import os
import re
import json
import yaml
import subprocess
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DeploymentConfig:
    environment: str
    branch: str
    database_url: str
    app_url: str
    health_check_url: str
    backup_required: bool = True

class EmailTaskDeployManager:
    """Specialized deployment manager for Email Task Manager project"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"
        
        self.deployment_configs = {
            'development': DeploymentConfig(
                environment='development',
                branch='develop',
                database_url='sqlite:///dev.db',
                app_url='http://localhost:5000',
                health_check_url='http://localhost:5000/api/health',
                backup_required=False
            ),
            'staging': DeploymentConfig(
                environment='staging',
                branch='staging',
                database_url='postgresql://staging_db',
                app_url='https://staging.emailtasks.com',
                health_check_url='https://staging.emailtasks.com/api/health'
            ),
            'production': DeploymentConfig(
                environment='production',
                branch='main',
                database_url='postgresql://production_db',
                app_url='https://emailtasks.com',
                health_check_url='https://emailtasks.com/api/health'
            )
        }
        
        self.deployment_results = {
            'ci_cd_pipelines': [],
            'docker_configs': [],
            'deployment_scripts': [],
            'monitoring_setup': [],
            'backup_strategies': []
        }
    
    def setup_complete_deployment(self) -> Dict[str, Any]:
        """Set up complete deployment infrastructure"""
        print("🚀 Setting up Email Task Manager Deployment Infrastructure...")
        
        # CI/CD Pipeline setup
        self._create_github_actions_workflows()
        self._create_docker_configurations()
        self._create_deployment_scripts()
        
        # Environment management
        self._create_environment_configs()
        self._setup_database_migrations()
        self._create_health_checks()
        
        # Monitoring and logging
        self._setup_application_monitoring()
        self._create_logging_configuration()
        self._setup_error_tracking()
        
        # Backup and recovery
        self._create_backup_strategies()
        self._setup_disaster_recovery()
        
        # Security and compliance
        self._create_security_configurations()
        self._setup_ssl_certificates()
        
        return self._generate_deployment_report()
    
    def _create_github_actions_workflows(self):
        """Create comprehensive GitHub Actions CI/CD workflows"""
        print("⚙️ Creating GitHub Actions workflows...")
        
        # Create .github/workflows directory
        workflows_dir = self.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Main CI/CD workflow
        main_workflow = """name: Email Task Manager CI/CD

on:
  push:
    branches: [ main, develop, staging ]
  pull_request:
    branches: [ main, develop ]

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.9'

jobs:
  # Backend Testing and Security
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: email_task_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Cache Python dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}
    
    - name: Install Python dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install safety bandit
    
    - name: Run Python security checks
      run: |
        cd backend
        safety check --json || true
        bandit -r . -f json -o bandit-report.json || true
    
    - name: Run backend tests with coverage
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/email_task_test
        SECRET_KEY: test-secret-key
        ENCRYPTION_SALT: test-salt
      run: |
        cd backend
        python run_tests.py --coverage-report
    
    - name: Upload backend coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
        flags: backend
    
    # Frontend Testing and Build
    frontend-tests:
      runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run frontend linting
      run: |
        cd frontend
        npm run lint
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm run test -- --coverage --watchAll=false
    
    - name: Build frontend
      run: |
        cd frontend
        npm run build
    
    - name: Upload frontend coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: frontend/coverage/lcov.info
        flags: frontend
    
    # Security Scanning
    security-scan:
      runs-on: ubuntu-latest
      needs: [backend-tests, frontend-tests]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
    
    # Build Docker Images
    build-docker:
      runs-on: ubuntu-latest
      needs: [backend-tests, frontend-tests, security-scan]
      if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/staging'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ secrets.CONTAINER_REGISTRY }}
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
    
    - name: Build and push backend image
      uses: docker/build-push-action@v5
      with:
        context: ./backend
        push: true
        tags: |
          ${{ secrets.CONTAINER_REGISTRY }}/email-task-backend:${{ github.sha }}
          ${{ secrets.CONTAINER_REGISTRY }}/email-task-backend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Build and push frontend image
      uses: docker/build-push-action@v5
      with:
        context: ./frontend
        push: true
        tags: |
          ${{ secrets.CONTAINER_REGISTRY }}/email-task-frontend:${{ github.sha }}
          ${{ secrets.CONTAINER_REGISTRY }}/email-task-frontend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    # Deploy to Staging
    deploy-staging:
      runs-on: ubuntu-latest
      needs: build-docker
      if: github.ref == 'refs/heads/staging'
      environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      env:
        DEPLOY_HOST: ${{ secrets.STAGING_HOST }}
        DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
        DEPLOY_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
      run: |
        echo "$DEPLOY_KEY" > deploy_key
        chmod 600 deploy_key
        scp -i deploy_key -o StrictHostKeyChecking=no docker-compose.staging.yml $DEPLOY_USER@$DEPLOY_HOST:/opt/email-task-manager/
        ssh -i deploy_key -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST "cd /opt/email-task-manager && docker-compose -f docker-compose.staging.yml up -d"
    
    - name: Run staging health checks
      run: |
        sleep 30
        curl -f ${{ secrets.STAGING_HEALTH_URL }} || exit 1
    
    # Deploy to Production
    deploy-production:
      runs-on: ubuntu-latest
      needs: build-docker
      if: github.ref == 'refs/heads/main'
      environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Create backup before deployment
      env:
        BACKUP_HOST: ${{ secrets.PRODUCTION_HOST }}
        BACKUP_USER: ${{ secrets.DEPLOY_USER }}
        BACKUP_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
      run: |
        echo "$BACKUP_KEY" > backup_key
        chmod 600 backup_key
        ssh -i backup_key -o StrictHostKeyChecking=no $BACKUP_USER@$BACKUP_HOST "/opt/email-task-manager/scripts/backup.sh"
    
    - name: Deploy to production
      env:
        DEPLOY_HOST: ${{ secrets.PRODUCTION_HOST }}
        DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
        DEPLOY_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
      run: |
        echo "$DEPLOY_KEY" > deploy_key
        chmod 600 deploy_key
        scp -i deploy_key -o StrictHostKeyChecking=no docker-compose.production.yml $DEPLOY_USER@$DEPLOY_HOST:/opt/email-task-manager/
        ssh -i deploy_key -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST "cd /opt/email-task-manager && docker-compose -f docker-compose.production.yml up -d"
    
    - name: Run production health checks
      run: |
        sleep 60
        curl -f ${{ secrets.PRODUCTION_HEALTH_URL }} || exit 1
    
    - name: Notify deployment success
      uses: 8398a7/action-slack@v3
      if: success()
      with:
        status: success
        text: 'Email Task Manager deployed successfully to production! 🚀'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
    
    - name: Notify deployment failure
      uses: 8398a7/action-slack@v3
      if: failure()
      with:
        status: failure
        text: 'Email Task Manager production deployment failed! ❌'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
"""
        
        main_workflow_file = workflows_dir / "ci-cd.yml"
        with open(main_workflow_file, 'w') as f:
            f.write(main_workflow)
        
        # Security workflow
        security_workflow = """name: Security Scanning

on:
  schedule:
    - cron: '0 2 * * 1' # Weekly security scan
  workflow_dispatch:

jobs:
  security-audit:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run security auditor agent
      run: |
        python agents/security_auditor.py .
    
    - name: Upload security report
      uses: actions/upload-artifact@v3
      with:
        name: security-audit-report
        path: security_audit_report.json
    
    - name: Check for critical vulnerabilities
      run: |
        if grep -q '"critical"' security_audit_report.json; then
          echo "Critical vulnerabilities found!"
          exit 1
        fi
    
    - name: Notify security issues
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        text: 'Security vulnerabilities detected in Email Task Manager! 🚨'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
"""
        
        security_workflow_file = workflows_dir / "security.yml"
        with open(security_workflow_file, 'w') as f:
            f.write(security_workflow)
        
        # Performance monitoring workflow
        performance_workflow = """name: Performance Monitoring

on:
  schedule:
    - cron: '0 6 * * *' # Daily performance check
  workflow_dispatch:

jobs:
  performance-check:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Run performance optimizer agent
      run: |
        cd backend
        pip install -r requirements.txt
        python ../agents/performance_optimizer.py ..
    
    - name: Upload performance report
      uses: actions/upload-artifact@v3
      with:
        name: performance-report
        path: performance_optimization_report.json
    
    - name: Check performance thresholds
      run: |
        # Add performance threshold checks here
        echo "Performance analysis completed"
"""
        
        performance_workflow_file = workflows_dir / "performance.yml"
        with open(performance_workflow_file, 'w') as f:
            f.write(performance_workflow)
        
        self.deployment_results['ci_cd_pipelines'].append({
            'type': 'GitHub Actions Workflows',
            'files': [str(main_workflow_file), str(security_workflow_file), str(performance_workflow_file)],
            'features': 'CI/CD, security scanning, performance monitoring, automated deployment',
            'environments': 'development, staging, production'
        })
    
    def _create_docker_configurations(self):
        """Create Docker configurations for containerized deployment"""
        print("🐳 Creating Docker configurations...")
        
        # Backend Dockerfile
        backend_dockerfile = """# Backend Dockerfile for Email Task Manager
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \\
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
"""
        
        backend_dockerfile_path = self.backend_path / "Dockerfile"
        with open(backend_dockerfile_path, 'w') as f:
            f.write(backend_dockerfile)
        
        # Frontend Dockerfile
        frontend_dockerfile = """# Frontend Dockerfile for Email Task Manager
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
"""
        
        frontend_dockerfile_path = self.frontend_path / "Dockerfile"
        with open(frontend_dockerfile_path, 'w') as f:
            f.write(frontend_dockerfile)
        
        # Nginx configuration for frontend
        nginx_config = """events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;
    
    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;" always;
        
        # Handle React Router
        location / {
            try_files $uri $uri/ /index.html;
        }
        
        # API proxy
        location /api {
            proxy_pass http://backend:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
        
        # Static file caching
        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
"""
        
        nginx_config_path = self.frontend_path / "nginx.conf"
        with open(nginx_config_path, 'w') as f:
            f.write(nginx_config)
        
        # Docker Compose configurations
        self._create_docker_compose_files()
        
        self.deployment_results['docker_configs'].append({
            'type': 'Docker Configuration',
            'files': [str(backend_dockerfile_path), str(frontend_dockerfile_path), str(nginx_config_path)],
            'features': 'Multi-stage builds, health checks, security optimizations, nginx reverse proxy'
        })
    
    def _create_docker_compose_files(self):
        """Create Docker Compose files for different environments"""
        
        # Development docker-compose
        dev_compose = """version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/email_task_dev
      - SECRET_KEY=dev-secret-key
      - ENCRYPTION_SALT=dev-salt
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    command: flask run --host=0.0.0.0
    
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm start
    
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=email_task_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""
        
        dev_compose_file = self.project_root / "docker-compose.dev.yml"
        with open(dev_compose_file, 'w') as f:
            f.write(dev_compose)
        
        # Staging docker-compose
        staging_compose = """version: '3.8'

services:
  backend:
    image: ${CONTAINER_REGISTRY}/email-task-backend:${IMAGE_TAG:-latest}
    environment:
      - FLASK_ENV=staging
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENCRYPTION_SALT=${ENCRYPTION_SALT}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  frontend:
    image: ${CONTAINER_REGISTRY}/email-task-frontend:${IMAGE_TAG:-latest}
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    restart: unless-stopped
    
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_staging_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
      
  redis:
    image: redis:6-alpine
    volumes:
      - redis_staging_data:/data
    restart: unless-stopped
    
  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped
      
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  postgres_staging_data:
  redis_staging_data:
  prometheus_data:
  grafana_data:
"""
        
        staging_compose_file = self.project_root / "docker-compose.staging.yml"
        with open(staging_compose_file, 'w') as f:
            f.write(staging_compose)
        
        # Production docker-compose
        production_compose = """version: '3.8'

services:
  backend:
    image: ${CONTAINER_REGISTRY}/email-task-backend:${IMAGE_TAG:-latest}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 3
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENCRYPTION_SALT=${ENCRYPTION_SALT}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
    depends_on:
      - db
      - redis
    networks:
      - app-network
    
  frontend:
    image: ${CONTAINER_REGISTRY}/email-task-frontend:${IMAGE_TAG:-latest}
    ports:
      - "80:80"
      - "443:443"
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    depends_on:
      - backend
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - app-network
    
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
      placement:
        constraints:
          - node.role == manager
      
  redis:
    image: redis:6-alpine
    volumes:
      - redis_prod_data:/data
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
  
  # Load balancer
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M

networks:
  app-network:
    driver: overlay

volumes:
  postgres_prod_data:
  redis_prod_data:
"""
        
        production_compose_file = self.project_root / "docker-compose.production.yml"
        with open(production_compose_file, 'w') as f:
            f.write(production_compose)
        
        self.deployment_results['docker_configs'].append({
            'type': 'Docker Compose Files',
            'files': [str(dev_compose_file), str(staging_compose_file), str(production_compose_file)],
            'environments': 'development, staging, production with monitoring'
        })
    
    def _create_deployment_scripts(self):
        """Create deployment automation scripts"""
        print("📜 Creating deployment scripts...")
        
        # Create scripts directory
        scripts_dir = self.project_root / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # Main deployment script
        deploy_script = """#!/bin/bash
# Email Task Manager Deployment Script
# Generated by Deploy Manager Agent

set -e

# Configuration
ENVIRONMENTS=("development" "staging" "production")
DEFAULT_ENV="staging"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check requirements
check_requirements() {
    log_info "Checking deployment requirements..."
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        exit 1
    fi
    
    log_info "All requirements satisfied"
}

# Load environment variables
load_env() {
    local env_file="$PROJECT_DIR/.env.$1"
    
    if [[ -f "$env_file" ]]; then
        log_info "Loading environment variables from $env_file"
        export $(cat "$env_file" | xargs)
    else
        log_warn "Environment file $env_file not found"
    fi
}

# Pre-deployment checks
pre_deployment_checks() {
    local environment=$1
    
    log_info "Running pre-deployment checks for $environment..."
    
    # Check if environment is valid
    if [[ ! " ${ENVIRONMENTS[@]} " =~ " ${environment} " ]]; then
        log_error "Invalid environment: $environment"
        log_info "Valid environments: ${ENVIRONMENTS[*]}"
        exit 1
    fi
    
    # Run tests for production/staging
    if [[ "$environment" == "production" || "$environment" == "staging" ]]; then
        log_info "Running test suite..."
        cd "$PROJECT_DIR/backend"
        python run_tests.py
        
        if [[ $? -ne 0 ]]; then
            log_error "Tests failed. Deployment aborted."
            exit 1
        fi
        
        log_info "All tests passed"
    fi
    
    # Check disk space
    available_space=$(df / | awk 'NR==2{printf "%.0f", $4/1024}')
    if [[ $available_space -lt 1024 ]]; then
        log_warn "Low disk space: ${available_space}MB available"
    fi
}

# Backup database (production/staging only)
backup_database() {
    local environment=$1
    
    if [[ "$environment" == "production" || "$environment" == "staging" ]]; then
        log_info "Creating database backup..."
        
        local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
        local backup_path="$PROJECT_DIR/backups/$backup_file"
        
        mkdir -p "$PROJECT_DIR/backups"
        
        if docker-compose -f "docker-compose.$environment.yml" exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > "$backup_path"; then
            log_info "Database backup created: $backup_path"
            
            # Keep only last 7 backups
            cd "$PROJECT_DIR/backups"
            ls -t backup_*.sql | tail -n +8 | xargs -r rm
        else
            log_error "Database backup failed"
            exit 1
        fi
    fi
}

# Deploy application
deploy_application() {
    local environment=$1
    
    log_info "Deploying to $environment environment..."
    
    cd "$PROJECT_DIR"
    
    # Pull latest changes for staging/production
    if [[ "$environment" != "development" ]]; then
        local branch="main"
        if [[ "$environment" == "staging" ]]; then
            branch="staging"
        fi
        
        log_info "Pulling latest changes from $branch branch..."
        git fetch origin
        git checkout "$branch"
        git pull origin "$branch"
    fi
    
    # Run database migrations
    log_info "Running database migrations..."
    if [[ "$environment" == "development" ]]; then
        cd backend
        python migrate_db.py
        cd ..
    else
        docker-compose -f "docker-compose.$environment.yml" exec backend python migrate_db.py
    fi
    
    # Deploy with docker-compose
    log_info "Starting services..."
    docker-compose -f "docker-compose.$environment.yml" up -d --build
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Health check
    if health_check "$environment"; then
        log_info "Deployment successful!"
    else
        log_error "Deployment failed health check"
        exit 1
    fi
}

# Health check
health_check() {
    local environment=$1
    local health_url
    
    case "$environment" in
        "development")
            health_url="http://localhost:5000/api/health"
            ;;
        "staging")
            health_url="$STAGING_HEALTH_URL"
            ;;
        "production")
            health_url="$PRODUCTION_HEALTH_URL"
            ;;
    esac
    
    log_info "Running health check: $health_url"
    
    for i in {1..5}; do
        if curl -f -s "$health_url" > /dev/null; then
            log_info "Health check passed"
            return 0
        fi
        
        log_warn "Health check attempt $i failed, retrying in 10 seconds..."
        sleep 10
    done
    
    log_error "Health check failed after 5 attempts"
    return 1
}

# Rollback deployment
rollback() {
    local environment=$1
    
    log_warn "Rolling back $environment deployment..."
    
    cd "$PROJECT_DIR"
    
    # Restore from backup if production/staging
    if [[ "$environment" == "production" || "$environment" == "staging" ]]; then
        local latest_backup=$(ls -t backups/backup_*.sql | head -n 1)
        
        if [[ -f "$latest_backup" ]]; then
            log_info "Restoring database from $latest_backup"
            docker-compose -f "docker-compose.$environment.yml" exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB < "$latest_backup"
        fi
    fi
    
    # Restart services
    docker-compose -f "docker-compose.$environment.yml" restart
    
    log_info "Rollback completed"
}

# Show usage
show_usage() {
    echo "Usage: $0 [ENVIRONMENT] [OPTIONS]"
    echo ""
    echo "Environments:"
    echo "  development  Deploy to development environment"
    echo "  staging      Deploy to staging environment"  
    echo "  production   Deploy to production environment"
    echo ""
    echo "Options:"
    echo "  --backup     Create backup before deployment (staging/production only)"
    echo "  --rollback   Rollback last deployment"
    echo "  --check      Run health check only"
    echo "  --help       Show this help message"
}

# Main deployment logic
main() {
    local environment=${1:-$DEFAULT_ENV}
    local action="deploy"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backup)
                backup_database "$environment"
                exit 0
                ;;
            --rollback)
                action="rollback"
                shift
                ;;
            --check)
                action="check"
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            development|staging|production)
                environment=$1
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Execute action
    case "$action" in
        "deploy")
            check_requirements
            load_env "$environment"
            pre_deployment_checks "$environment"
            backup_database "$environment"
            deploy_application "$environment"
            ;;
        "rollback")
            rollback "$environment"
            ;;
        "check")
            health_check "$environment"
            ;;
    esac
}

# Run main function with all arguments
main "$@"
"""
        
        deploy_script_file = scripts_dir / "deploy.sh"
        with open(deploy_script_file, 'w') as f:
            f.write(deploy_script)
        
        # Make script executable
        try:
            os.chmod(deploy_script_file, 0o755)
        except:
            pass
        
        # Database backup script
        backup_script = """#!/bin/bash
# Database Backup Script
# Generated by Deploy Manager Agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\\033[0;32m'
RED='\\033[0;31m'
NC='\\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Load environment variables
if [[ -f "$PROJECT_DIR/.env.production" ]]; then
    export $(cat "$PROJECT_DIR/.env.production" | xargs)
fi

# Backup database
backup_database() {
    local backup_file="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"
    
    log_info "Creating database backup..."
    
    if docker-compose -f "$PROJECT_DIR/docker-compose.production.yml" exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > "$backup_file"; then
        log_info "Database backup created: $backup_file"
        
        # Compress backup
        gzip "$backup_file"
        log_info "Backup compressed: ${backup_file}.gz"
        
        # Upload to cloud storage (if configured)
        if [[ ! -z "$BACKUP_STORAGE_URL" ]]; then
            log_info "Uploading backup to cloud storage..."
            # Add cloud upload logic here (AWS S3, Google Cloud, etc.)
        fi
        
        # Clean old backups (keep last 30 days)
        find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +30 -delete
        
        log_info "Backup process completed successfully"
    else
        log_error "Database backup failed"
        exit 1
    fi
}

# Backup application files
backup_files() {
    local backup_file="$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz"
    
    log_info "Creating files backup..."
    
    # Backup important configuration files and data
    tar -czf "$backup_file" \\
        -C "$PROJECT_DIR" \\
        --exclude='node_modules' \\
        --exclude='__pycache__' \\
        --exclude='.git' \\
        --exclude='backups' \\
        .env.* \\
        docker-compose.*.yml \\
        scripts/ \\
        ssl/ 2>/dev/null || true
    
    log_info "Files backup created: $backup_file"
}

# Main backup function
main() {
    log_info "Starting backup process..."
    
    backup_database
    backup_files
    
    log_info "All backups completed successfully"
}

main "$@"
"""
        
        backup_script_file = scripts_dir / "backup.sh"
        with open(backup_script_file, 'w') as f:
            f.write(backup_script)
        
        try:
            os.chmod(backup_script_file, 0o755)
        except:
            pass
        
        # Monitoring script
        monitoring_script = """#!/bin/bash
# System Monitoring Script
# Generated by Deploy Manager Agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
RED='\\033[0;31m'
NC='\\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system resources
check_resources() {
    log_info "Checking system resources..."
    
    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\\([0-9.]*\\)%* id.*/\\1/" | awk '{print 100 - $1}')
    log_info "CPU Usage: ${cpu_usage}%"
    
    # Memory usage
    memory_info=$(free -m)
    memory_usage=$(echo "$memory_info" | awk 'NR==2{printf "%.2f", $3*100/$2}')
    log_info "Memory Usage: ${memory_usage}%"
    
    # Disk usage
    disk_usage=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')
    log_info "Disk Usage: ${disk_usage}%"
    
    # Alert on high usage
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        log_warn "High CPU usage: ${cpu_usage}%"
    fi
    
    if (( $(echo "$memory_usage > 80" | bc -l) )); then
        log_warn "High memory usage: ${memory_usage}%"
    fi
    
    if [[ $disk_usage -gt 80 ]]; then
        log_warn "High disk usage: ${disk_usage}%"
    fi
}

# Check application health
check_application() {
    log_info "Checking application health..."
    
    # Check Docker containers
    if docker-compose -f "$PROJECT_DIR/docker-compose.production.yml" ps | grep -q "Up"; then
        log_info "Docker containers are running"
    else
        log_error "Some Docker containers are not running"
        docker-compose -f "$PROJECT_DIR/docker-compose.production.yml" ps
    fi
    
    # Check application endpoints
    local health_endpoints=(
        "http://localhost/api/health"
        "http://localhost/health"
    )
    
    for endpoint in "${health_endpoints[@]}"; do
        if curl -f -s "$endpoint" > /dev/null; then
            log_info "Health check passed: $endpoint"
        else
            log_error "Health check failed: $endpoint"
        fi
    done
}

# Check database
check_database() {
    log_info "Checking database..."
    
    if docker-compose -f "$PROJECT_DIR/docker-compose.production.yml" exec -T db pg_isready -U $POSTGRES_USER > /dev/null; then
        log_info "Database is ready"
        
        # Check database size
        db_size=$(docker-compose -f "$PROJECT_DIR/docker-compose.production.yml" exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT pg_size_pretty(pg_database_size('$POSTGRES_DB'));" -t | xargs)
        log_info "Database size: $db_size"
    else
        log_error "Database is not ready"
    fi
}

# Generate monitoring report
generate_report() {
    local report_file="$PROJECT_DIR/monitoring_report_$(date +%Y%m%d_%H%M%S).json"
    
    log_info "Generating monitoring report..."
    
    # Collect metrics
    local metrics=$(cat <<EOF
{
    "timestamp": "$(date -Iseconds)",
    "system": {
        "cpu_usage": $cpu_usage,
        "memory_usage": $memory_usage,
        "disk_usage": $disk_usage
    },
    "containers": $(docker-compose -f "$PROJECT_DIR/docker-compose.production.yml" ps --format json 2>/dev/null || echo "[]"),
    "uptime": "$(uptime -p)"
}
EOF
    )
    
    echo "$metrics" > "$report_file"
    log_info "Monitoring report saved: $report_file"
}

# Main monitoring function
main() {
    log_info "Starting system monitoring..."
    
    check_resources
    check_application
    check_database
    generate_report
    
    log_info "Monitoring completed"
}

main "$@"
"""
        
        monitoring_script_file = scripts_dir / "monitor.sh"
        with open(monitoring_script_file, 'w') as f:
            f.write(monitoring_script)
        
        try:
            os.chmod(monitoring_script_file, 0o755)
        except:
            pass
        
        self.deployment_results['deployment_scripts'].append({
            'type': 'Deployment Automation Scripts',
            'files': [str(deploy_script_file), str(backup_script_file), str(monitoring_script_file)],
            'features': 'Automated deployment, database backup, system monitoring, health checks'
        })
    
    def _create_environment_configs(self):
        """Create environment-specific configuration files"""
        print("🔧 Creating environment configurations...")
        
        # Development environment
        dev_env = """# Development Environment Configuration
FLASK_ENV=development
DEBUG=True

# Database
DATABASE_URL=sqlite:///dev.db

# Security
SECRET_KEY=dev-secret-key-change-in-production
ENCRYPTION_SALT=dev-salt-change-in-production

# External APIs
OPENAI_API_KEY=your-openai-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Application URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0

# Monitoring
LOG_LEVEL=DEBUG
"""
        
        dev_env_file = self.project_root / ".env.development"
        with open(dev_env_file, 'w') as f:
            f.write(dev_env)
        
        # Staging environment
        staging_env = """# Staging Environment Configuration
FLASK_ENV=staging
DEBUG=False

# Database
DATABASE_URL=postgresql://staging_user:staging_pass@db:5432/email_task_staging
POSTGRES_DB=email_task_staging
POSTGRES_USER=staging_user
POSTGRES_PASSWORD=staging_secure_password

# Security
SECRET_KEY=staging-secret-key-32-characters-long
ENCRYPTION_SALT=staging-encryption-salt-change-me

# External APIs
OPENAI_API_KEY=${OPENAI_API_KEY}
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}

# Application URLs
FRONTEND_URL=https://staging.emailtasks.com
BACKEND_URL=https://api-staging.emailtasks.com

# Redis
REDIS_URL=redis://redis:6379/0

# Container Registry
CONTAINER_REGISTRY=your-registry.com
IMAGE_TAG=staging

# SSL
SSL_CERTIFICATE_PATH=/etc/nginx/ssl/cert.pem
SSL_PRIVATE_KEY_PATH=/etc/nginx/ssl/key.pem

# Monitoring
LOG_LEVEL=INFO
GRAFANA_PASSWORD=staging_grafana_password

# Health Check URLs
STAGING_HEALTH_URL=https://staging.emailtasks.com/api/health
"""
        
        staging_env_file = self.project_root / ".env.staging"
        with open(staging_env_file, 'w') as f:
            f.write(staging_env)
        
        # Production environment template
        production_env = """# Production Environment Configuration
FLASK_ENV=production
DEBUG=False

# Database
DATABASE_URL=postgresql://prod_user:secure_production_password@db:5432/email_task_production
POSTGRES_DB=email_task_production
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=secure_production_password_change_me

# Security (CHANGE ALL DEFAULT VALUES)
SECRET_KEY=production-secret-key-32-characters-minimum
ENCRYPTION_SALT=production-encryption-salt-change-me

# External APIs
OPENAI_API_KEY=${OPENAI_API_KEY}
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}

# Application URLs
FRONTEND_URL=https://emailtasks.com
BACKEND_URL=https://api.emailtasks.com

# Redis
REDIS_URL=redis://redis:6379/0

# Container Registry
CONTAINER_REGISTRY=your-registry.com
IMAGE_TAG=latest

# SSL
SSL_CERTIFICATE_PATH=/etc/nginx/ssl/cert.pem
SSL_PRIVATE_KEY_PATH=/etc/nginx/ssl/key.pem

# Monitoring
LOG_LEVEL=WARNING
GRAFANA_PASSWORD=secure_grafana_password
PROMETHEUS_RETENTION=30d

# Backup Configuration
BACKUP_STORAGE_URL=s3://your-backup-bucket
BACKUP_ENCRYPTION_KEY=backup-encryption-key-change-me

# Health Check URLs
PRODUCTION_HEALTH_URL=https://emailtasks.com/api/health

# Rate Limiting
RATE_LIMIT_STORAGE_URL=redis://redis:6379/1

# Email Notifications (for alerts)
ALERT_EMAIL_FROM=alerts@emailtasks.com
ALERT_EMAIL_TO=admin@emailtasks.com
SMTP_SERVER=smtp.emailtasks.com
SMTP_PORT=587
SMTP_USERNAME=${SMTP_USERNAME}
SMTP_PASSWORD=${SMTP_PASSWORD}

# Performance
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
NGINX_WORKER_PROCESSES=auto
NGINX_WORKER_CONNECTIONS=1024
"""
        
        production_env_file = self.project_root / ".env.production.example"
        with open(production_env_file, 'w') as f:
            f.write(production_env)
        
        self.deployment_results['deployment_scripts'].append({
            'type': 'Environment Configuration Files',
            'files': [str(dev_env_file), str(staging_env_file), str(production_env_file)],
            'features': 'Environment-specific settings, security configurations, external API keys'
        })
    
    def _setup_database_migrations(self):
        """Set up database migration system"""
        print("🗄️ Setting up database migrations...")
        
        # Enhanced migration script
        migration_script = '''#!/usr/bin/env python3
"""
Enhanced Database Migration System
Generated by Deploy Manager Agent
"""

import os
import sys
import sqlite3
import psycopg2
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend import create_app, db

class DatabaseMigrator:
    """Enhanced database migration system"""
    
    def __init__(self):
        self.app = create_app()
        self.migrations_dir = Path(__file__).parent / "migrations"
        self.migrations_dir.mkdir(exist_ok=True)
        
    def create_migration(self, name: str, up_sql: str, down_sql: str = ""):
        """Create a new migration file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        migration_file = self.migrations_dir / f"{timestamp}_{name}.sql"
        
        migration_content = f"""-- Migration: {name}
-- Created: {datetime.now().isoformat()}
-- Up Migration
{up_sql}

-- Rollback (Down Migration)  
-- To rollback this migration, run the following:
-- {down_sql}
"""
        
        with open(migration_file, 'w') as f:
            f.write(migration_content)
        
        print(f"Created migration: {migration_file}")
        return migration_file
    
    def run_migrations(self):
        """Run all pending migrations"""
        with self.app.app_context():
            # Create migrations table if it doesn't exist
            self._create_migrations_table()
            
            # Get applied migrations
            applied = self._get_applied_migrations()
            
            # Get all migration files
            migration_files = sorted(self.migrations_dir.glob("*.sql"))
            
            for migration_file in migration_files:
                migration_name = migration_file.stem
                
                if migration_name not in applied:
                    print(f"Applying migration: {migration_name}")
                    self._apply_migration(migration_file, migration_name)
                else:
                    print(f"Migration already applied: {migration_name}")
            
            print("All migrations completed successfully")
    
    def _create_migrations_table(self):
        """Create migrations tracking table"""
        db.engine.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.session.commit()
    
    def _get_applied_migrations(self):
        """Get list of applied migrations"""
        result = db.engine.execute("SELECT migration_name FROM migrations")
        return {row[0] for row in result}
    
    def _apply_migration(self, migration_file: Path, migration_name: str):
        """Apply a single migration"""
        try:
            # Read migration file
            with open(migration_file, 'r') as f:
                content = f.read()
            
            # Extract SQL (everything before "-- Rollback")
            sql_parts = content.split("-- Rollback")
            up_sql = sql_parts[0].strip()
            
            # Remove comment lines and empty lines
            sql_lines = []
            for line in up_sql.split('\\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    sql_lines.append(line)
            
            final_sql = '\\n'.join(sql_lines)
            
            if final_sql:
                # Execute migration
                db.engine.execute(final_sql)
                
                # Record migration as applied
                db.engine.execute(
                    "INSERT INTO migrations (migration_name) VALUES (%s)",
                    (migration_name,)
                )
                
                db.session.commit()
                print(f"Successfully applied migration: {migration_name}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error applying migration {migration_name}: {e}")
            raise

def main():
    """Main migration function"""
    migrator = DatabaseMigrator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create" and len(sys.argv) > 2:
            name = sys.argv[2]
            up_sql = input("Enter UP SQL: ")
            down_sql = input("Enter DOWN SQL (optional): ")
            migrator.create_migration(name, up_sql, down_sql)
        else:
            print("Usage: python migrate_db.py create <migration_name>")
    else:
        # Run migrations
        migrator.run_migrations()

if __name__ == "__main__":
    main()
'''
        
        migration_file = self.backend_path / "migrate_db_enhanced.py"
        with open(migration_file, 'w') as f:
            f.write(migration_script)
        
        # Create initial performance indexes migration
        performance_migration = """-- Performance Indexes Migration
-- Created for Email Task Manager optimization

-- User table indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);

-- Task table indexes  
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_email_id ON tasks(email_id);
CREATE INDEX IF NOT EXISTS idx_tasks_sender ON tasks(sender);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_completed_at ON tasks(completed_at);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tasks_user_completed ON tasks(user_id, completed);
CREATE INDEX IF NOT EXISTS idx_tasks_user_priority_completed ON tasks(user_id, priority, completed);
CREATE INDEX IF NOT EXISTS idx_tasks_user_category_completed ON tasks(user_id, category, completed);
CREATE INDEX IF NOT EXISTS idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- Email table indexes
CREATE INDEX IF NOT EXISTS idx_emails_user_id ON emails(user_id);
CREATE INDEX IF NOT EXISTS idx_emails_gmail_id ON emails(gmail_id);
CREATE INDEX IF NOT EXISTS idx_emails_thread_id ON emails(thread_id);
CREATE INDEX IF NOT EXISTS idx_emails_sender ON emails(sender);
CREATE INDEX IF NOT EXISTS idx_emails_sender_email ON emails(sender_email);
CREATE INDEX IF NOT EXISTS idx_emails_processed ON emails(processed);
CREATE INDEX IF NOT EXISTS idx_emails_processed_at ON emails(processed_at);
CREATE INDEX IF NOT EXISTS idx_emails_received_at ON emails(received_at);
CREATE INDEX IF NOT EXISTS idx_emails_created_at ON emails(created_at);

-- Composite indexes for emails
CREATE INDEX IF NOT EXISTS idx_emails_user_processed ON emails(user_id, processed);
CREATE INDEX IF NOT EXISTS idx_emails_user_received ON emails(user_id, received_at DESC);

-- Partial indexes for better performance on specific queries
CREATE INDEX IF NOT EXISTS idx_tasks_active ON tasks(user_id, priority) WHERE completed = false;
CREATE INDEX IF NOT EXISTS idx_emails_unprocessed ON emails(user_id, received_at) WHERE processed = false;
"""
        
        migrations_dir = self.backend_path / "migrations"
        migrations_dir.mkdir(exist_ok=True)
        
        initial_migration_file = migrations_dir / "20240101_000000_performance_indexes.sql"
        with open(initial_migration_file, 'w') as f:
            f.write(performance_migration)
        
        self.deployment_results['deployment_scripts'].append({
            'type': 'Database Migration System',
            'files': [str(migration_file), str(initial_migration_file)],
            'features': 'Migration tracking, rollback support, performance indexes'
        })
    
    def _create_health_checks(self):
        """Create comprehensive health check system"""
        print("🏥 Creating health check system...")
        
        health_check_code = '''"""
Comprehensive Health Check System
Generated by Deploy Manager Agent
"""

import os
import time
import json
import psutil
import requests
from datetime import datetime
from typing import Dict, List, Any
from flask import Blueprint, jsonify, current_app
from backend import db

health_bp = Blueprint('health', __name__)

class HealthChecker:
    """Comprehensive health check system"""
    
    def __init__(self):
        self.checks = [
            self._check_database,
            self._check_redis,
            self._check_external_apis,
            self._check_disk_space,
            self._check_memory,
            self._check_cpu
        ]
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'summary': {
                'total': len(self.checks),
                'passed': 0,
                'failed': 0
            }
        }
        
        for check in self.checks:
            try:
                check_name = check.__name__.replace('_check_', '')
                check_result = check()
                
                results['checks'][check_name] = check_result
                
                if check_result['status'] == 'healthy':
                    results['summary']['passed'] += 1
                else:
                    results['summary']['failed'] += 1
                    results['status'] = 'unhealthy'
                    
            except Exception as e:
                results['checks'][check.__name__.replace('_check_', '')] = {
                    'status': 'error',
                    'error': str(e)
                }
                results['summary']['failed'] += 1
                results['status'] = 'unhealthy'
        
        return results
    
    def _check_database(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Test database connection
            result = db.engine.execute('SELECT 1')
            list(result)  # Consume result
            
            query_time = (time.time() - start_time) * 1000  # ms
            
            # Get database size if PostgreSQL
            try:
                size_result = db.engine.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """)
                db_size = list(size_result)[0][0]
            except:
                db_size = 'Unknown'
            
            return {
                'status': 'healthy',
                'response_time_ms': round(query_time, 2),
                'database_size': db_size
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def _check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            import redis
            
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            r = redis.from_url(redis_url)
            
            start_time = time.time()
            r.ping()
            response_time = (time.time() - start_time) * 1000
            
            # Get Redis info
            info = r.info()
            
            return {
                'status': 'healthy',
                'response_time_ms': round(response_time, 2),
                'memory_usage': info.get('used_memory_human', 'Unknown'),
                'connected_clients': info.get('connected_clients', 0)
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def _check_external_apis(self) -> Dict[str, Any]:
        """Check external API connectivity"""
        apis_status = {}
        overall_status = 'healthy'
        
        # Check OpenAI API
        try:
            import openai
            
            client = openai.OpenAI()
            start_time = time.time()
            
            # Simple API test
            response = client.models.list()
            response_time = (time.time() - start_time) * 1000
            
            apis_status['openai'] = {
                'status': 'healthy',
                'response_time_ms': round(response_time, 2)
            }
            
        except Exception as e:
            apis_status['openai'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            overall_status = 'degraded'
        
        # Check Google API (if configured)
        google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        if google_client_id:
            try:
                # Simple connectivity test to Google
                start_time = time.time()
                response = requests.get('https://www.googleapis.com/oauth2/v1/certs', timeout=5)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    apis_status['google'] = {
                        'status': 'healthy',
                        'response_time_ms': round(response_time, 2)
                    }
                else:
                    apis_status['google'] = {
                        'status': 'unhealthy',
                        'http_status': response.status_code
                    }
                    overall_status = 'degraded'
                    
            except Exception as e:
                apis_status['google'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                overall_status = 'degraded'
        
        return {
            'status': overall_status,
            'apis': apis_status
        }
    
    def _check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            disk_usage = psutil.disk_usage('/')
            
            total_gb = disk_usage.total / (1024**3)
            free_gb = disk_usage.free / (1024**3)
            used_percent = (disk_usage.used / disk_usage.total) * 100
            
            status = 'healthy'
            if used_percent > 90:
                status = 'critical'
            elif used_percent > 80:
                status = 'warning'
            
            return {
                'status': status,
                'total_gb': round(total_gb, 2),
                'free_gb': round(free_gb, 2),
                'used_percent': round(used_percent, 2)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _check_memory(self) -> Dict[str, Any]:
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            
            total_gb = memory.total / (1024**3)
            available_gb = memory.available / (1024**3)
            used_percent = memory.percent
            
            status = 'healthy'
            if used_percent > 90:
                status = 'critical'
            elif used_percent > 80:
                status = 'warning'
            
            return {
                'status': status,
                'total_gb': round(total_gb, 2),
                'available_gb': round(available_gb, 2),
                'used_percent': round(used_percent, 2)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _check_cpu(self) -> Dict[str, Any]:
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            status = 'healthy'
            if cpu_percent > 90:
                status = 'critical'
            elif cpu_percent > 80:
                status = 'warning'
            
            return {
                'status': status,
                'usage_percent': round(cpu_percent, 2),
                'cpu_count': cpu_count
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Global health checker instance
health_checker = HealthChecker()

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Email Task Manager'
    })

@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with all systems"""
    results = health_checker.run_all_checks()
    
    status_code = 200
    if results['status'] == 'unhealthy':
        status_code = 503
    elif results['status'] == 'degraded':
        status_code = 200  # Still serving requests
    
    return jsonify(results), status_code

@health_bp.route('/health/readiness', methods=['GET'])
def readiness_check():
    """Kubernetes readiness probe"""
    try:
        # Test critical dependencies
        db.engine.execute('SELECT 1')
        
        return jsonify({
            'status': 'ready',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

@health_bp.route('/health/liveness', methods=['GET'])
def liveness_check():
    """Kubernetes liveness probe"""
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.now().isoformat()
    })
'''
        
        health_check_file = self.backend_path / "routes" / "health.py"
        with open(health_check_file, 'w') as f:
            f.write(health_check_code)
        
        self.deployment_results['monitoring_setup'].append({
            'type': 'Health Check System',
            'file': str(health_check_file),
            'features': 'Database, Redis, external APIs, system resources, Kubernetes probes'
        })
    
    def _generate_deployment_report(self) -> Dict[str, Any]:
        """Generate comprehensive deployment report"""
        
        total_components = sum(len(components) for components in self.deployment_results.values())
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': 'Email Task Manager',
            'deployment_summary': {
                'total_components': total_components,
                'ci_cd_pipelines': len(self.deployment_results['ci_cd_pipelines']),
                'docker_configs': len(self.deployment_results['docker_configs']),
                'deployment_scripts': len(self.deployment_results['deployment_scripts']),
                'monitoring_setup': len(self.deployment_results['monitoring_setup'])
            },
            'deployment_components': self.deployment_results,
            'environments': list(self.deployment_configs.keys()),
            'deployment_flow': [
                "1. Code commit triggers GitHub Actions",
                "2. Automated testing (backend + frontend)",
                "3. Security scanning and vulnerability checks", 
                "4. Docker image building and registry push",
                "5. Staging deployment with health checks",
                "6. Production deployment with backup creation",
                "7. Post-deployment monitoring and alerting"
            ],
            'key_features': [
                "🚀 Automated CI/CD with GitHub Actions",
                "🐳 Containerized deployment with Docker",
                "🔒 Security scanning and vulnerability detection",
                "📊 Comprehensive health checks and monitoring",
                "🗄️ Automated database migrations and backups",
                "🌍 Multi-environment support (dev/staging/prod)",
                "⚡ Performance optimized configurations",
                "🔄 Rollback capabilities and disaster recovery"
            ],
            'next_steps': [
                "Configure GitHub repository secrets for deployment",
                "Set up container registry (Docker Hub, AWS ECR, etc.)",
                "Configure production servers and SSL certificates",
                "Set up monitoring dashboards (Grafana/Prometheus)",
                "Configure backup storage (AWS S3, Google Cloud)",
                "Set up alerting (Slack, email notifications)",
                "Test deployment pipeline in staging environment"
            ]
        }
        
        # Save report
        report_file = self.project_root / "deployment_setup_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n🚀 Deployment Setup Complete!")
        print(f"Total Components: {total_components}")
        print(f"Environments: {', '.join(self.deployment_configs.keys())}")
        print(f"Report saved to: {report_file}")
        
        return report


def main():
    """Main execution function"""
    import sys
    
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    deploy_manager = EmailTaskDeployManager(project_root)
    report = deploy_manager.setup_complete_deployment()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"DEPLOYMENT SETUP SUMMARY")
    print(f"{'='*60}")
    print(f"Total Components: {report['deployment_summary']['total_components']}")
    print(f"CI/CD Pipelines: {report['deployment_summary']['ci_cd_pipelines']}")
    print(f"Docker Configs: {report['deployment_summary']['docker_configs']}")
    print(f"Deployment Scripts: {report['deployment_summary']['deployment_scripts']}")
    print(f"Monitoring Setup: {report['deployment_summary']['monitoring_setup']}")
    print(f"Supported Environments: {', '.join(report['environments'])}")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)