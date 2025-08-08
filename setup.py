#!/usr/bin/env python3
"""
Setup script for Email Task Manager
This script helps set up the development environment and configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def create_env_file(backend_dir):
    """Create .env file for backend"""
    env_content = """# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-this-in-production

# Database
DATABASE_URL=sqlite:///email_task_manager.db

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/api/auth/google/callback

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Gmail API Configuration
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly

# Application Configuration
TASK_PROCESSING_INTERVAL=900
MAX_EMAILS_PER_PROCESS=50
"""
    
    env_path = backend_dir / '.env'
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"Created {env_path}")
    else:
        print(f"{env_path} already exists")

def setup_backend():
    """Set up the backend"""
    print("Setting up backend...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("Backend directory not found!")
        return False
    
    # Create virtual environment
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", cwd=backend_dir):
            return False
    
    # Install dependencies
    print("Installing Python dependencies...")
    pip_cmd = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip"
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Create .env file
    create_env_file(backend_dir)
    
    print("Backend setup complete!")
    return True

def setup_frontend():
    """Set up the frontend"""
    print("Setting up frontend...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("Frontend directory not found!")
        return False
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("Frontend setup complete!")
    return True

def main():
    """Main setup function"""
    print("Email Task Manager Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Python 3.8+ is required!")
        return
    
    # Check Node.js
    if not run_command("node --version"):
        print("Node.js is required but not found!")
        return
    
    # Check npm
    if not run_command("npm --version"):
        print("npm is required but not found!")
        return
    
    # Setup backend
    if not setup_backend():
        print("Backend setup failed!")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("Frontend setup failed!")
        return
    
    print("\n" + "=" * 30)
    print("Setup complete!")
    print("\nNext steps:")
    print("1. Configure your Google OAuth credentials")
    print("2. Get an OpenAI API key")
    print("3. Update the .env file in the backend directory")
    print("4. Run the backend: cd backend && python app.py")
    print("5. Run the frontend: cd frontend && npm start")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main()
