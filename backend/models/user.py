from extensions import db
from utils.encryption import token_encryption
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    gmail_connected = db.Column(db.Boolean, default=False)
    _gmail_access_token = db.Column('gmail_access_token', db.Text, nullable=True)
    _gmail_refresh_token = db.Column('gmail_refresh_token', db.Text, nullable=True)
    gmail_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    emails = db.relationship('Email', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @hybrid_property
    def gmail_access_token(self):
        """Decrypt and return access token"""
        if self._gmail_access_token:
            return token_encryption.decrypt_token(self._gmail_access_token)
        return None
    
    @gmail_access_token.setter
    def gmail_access_token(self, value):
        """Encrypt and store access token"""
        if value:
            self._gmail_access_token = token_encryption.encrypt_token(value)
        else:
            self._gmail_access_token = None
    
    @hybrid_property
    def gmail_refresh_token(self):
        """Decrypt and return refresh token"""
        if self._gmail_refresh_token:
            return token_encryption.decrypt_token(self._gmail_refresh_token)
        return None
    
    @gmail_refresh_token.setter
    def gmail_refresh_token(self, value):
        """Encrypt and store refresh token"""
        if value:
            self._gmail_refresh_token = token_encryption.encrypt_token(value)
        else:
            self._gmail_refresh_token = None

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'gmail_connected': self.gmail_connected,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
