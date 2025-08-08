from extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    email_id = db.Column(db.Integer, db.ForeignKey('emails.id'), nullable=False, index=True)
    
    # Task details
    description = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(255), nullable=False, index=True)
    priority = db.Column(db.String(50), nullable=False, default='Medium', index=True)  # High, Medium, Low
    category = db.Column(db.String(100), nullable=False, default='General', index=True)
    
    # Status
    completed = db.Column(db.Boolean, default=False, index=True)
    completed_at = db.Column(db.DateTime, nullable=True, index=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    email = db.relationship('Email', backref='tasks')
    
    def __repr__(self):
        return f'<Task {self.id}: {self.description[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email_id': self.email_id,
            'description': self.description,
            'sender': self.sender,
            'priority': self.priority,
            'category': self.category,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'email': {
                'subject': self.email.subject,
                'received_at': self.email.received_at.isoformat()
            } if self.email else None
        }
    
    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
