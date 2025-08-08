from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json
from datetime import datetime, timedelta
from extensions import db
from models.user import User
from utils import sanitize_text, validate_email

auth_bp = Blueprint('auth', __name__)

# Google OAuth configuration
GOOGLE_CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')]
    }
}

@auth_bp.route('/google/authorize')
def google_authorize():
    """Initiate Google OAuth flow"""
    try:
        flow = Flow.from_client_config(
            GOOGLE_CLIENT_CONFIG,
            scopes=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        session['state'] = state
        return jsonify({'authorization_url': authorization_url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        flow = Flow.from_client_config(
            GOOGLE_CLIENT_CONFIG,
            scopes=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')
        
        # Exchange authorization code for tokens
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Get user info from Google
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        # Validate and sanitize user info
        user_email = user_info.get('email', '')
        user_name = user_info.get('name', user_email)
        
        if not validate_email(user_email):
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Sanitize user data
        user_email = sanitize_text(user_email, 255)
        user_name = sanitize_text(user_name, 255)
        
        # Check if user exists, create if not
        user = User.query.filter_by(email=user_email).first()
        if not user:
            user = User(
                email=user_email,
                name=user_name,
                gmail_connected=True,
                gmail_access_token=credentials.token,
                gmail_refresh_token=credentials.refresh_token,
                gmail_token_expiry=credentials.expiry
            )
            db.session.add(user)
        else:
            # Update existing user's Gmail connection
            user.gmail_connected = True
            user.gmail_access_token = credentials.token
            user.gmail_refresh_token = credentials.refresh_token
            user.gmail_token_expiry = credentials.expiry
            user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        # Redirect to frontend with token
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/auth/callback?token={access_token}")
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout')
@jwt_required()
def logout():
    """Logout user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user:
        user.gmail_connected = False
        user.gmail_access_token = None
        user.gmail_refresh_token = None
        user.gmail_token_expiry = None
        user.updated_at = datetime.utcnow()
        db.session.commit()
    
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/refresh')
@jwt_required()
def refresh_token():
    """Refresh JWT token"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if Gmail token needs refresh
    if user.gmail_token_expiry and user.gmail_token_expiry < datetime.utcnow():
        try:
            credentials = Credentials(
                token=user.gmail_access_token,
                refresh_token=user.gmail_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
            )
            
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                
                user.gmail_access_token = credentials.token
                user.gmail_token_expiry = credentials.expiry
                user.updated_at = datetime.utcnow()
                db.session.commit()
        
        except Exception as e:
            return jsonify({'error': 'Failed to refresh Gmail token'}), 500
    
    new_token = create_access_token(identity=user.id)
    return jsonify({'access_token': new_token})
