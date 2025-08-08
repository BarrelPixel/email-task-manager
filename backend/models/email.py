from extensions import db
from datetime import datetime

class Email(db.Model):
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Gmail metadata
    gmail_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    thread_id = db.Column(db.String(255), nullable=True, index=True)
    
    # Email content
    subject = db.Column(db.String(500), nullable=False)
    sender = db.Column(db.String(255), nullable=False, index=True)
    sender_email = db.Column(db.String(255), nullable=False, index=True)
    body = db.Column(db.Text, nullable=True)
    snippet = db.Column(db.Text, nullable=True)
    
    # Processing status
    processed = db.Column(db.Boolean, default=False, index=True)
    processed_at = db.Column(db.DateTime, nullable=True, index=True)
    
    # Timestamps
    received_at = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Email {self.gmail_id}: {self.subject[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'gmail_id': self.gmail_id,
            'thread_id': self.thread_id,
            'subject': self.subject,
            'sender': self.sender,
            'sender_email': self.sender_email,
            'body': self.body,
            'snippet': self.snippet,
            'processed': self.processed,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'received_at': self.received_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def mark_processed(self):
        self.processed = True
        self.processed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
