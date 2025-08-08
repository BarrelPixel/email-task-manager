from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import base64
import email
import os
from run import db
from models.email import Email
from models.task import Task
from models.user import User
from services.gmail_service import GmailService
from services.ai_service import AIService
from utils import ValidationError, validate_email_content, validate_task_data, ratelimit

emails_bp = Blueprint('emails', __name__)

@emails_bp.route('/process', methods=['POST'])
@jwt_required()
@ratelimit(limit=5, window=300, per='user')  # 5 requests per 5 minutes per user
def process_emails():
    """Process new emails for the current user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.gmail_connected:
        return jsonify({'error': 'Gmail not connected'}), 400
    
    try:
        # Initialize services
        gmail_service = GmailService(user)
        ai_service = AIService()
        
        # Get unprocessed emails from Gmail with limit
        max_emails = int(os.getenv('MAX_EMAILS_PER_PROCESS', 50))
        new_emails = gmail_service.get_unprocessed_emails(max_results=max_emails)
        
        processed_count = 0
        tasks_created = 0
        
        for email_data in new_emails:
            # Check if email already exists
            existing_email = Email.query.filter_by(gmail_id=email_data['gmail_id'], user_id=current_user_id).first()
            if existing_email:
                continue
            
            # Validate and sanitize email content
            try:
                validated_content = validate_email_content(
                    email_data['subject'], 
                    email_data.get('body', '')
                )
            except ValidationError as e:
                continue  # Skip invalid emails
            
            # Create email record
            email_record = Email(
                user_id=current_user_id,
                gmail_id=email_data['gmail_id'],
                thread_id=email_data.get('thread_id'),
                subject=validated_content['subject'],
                sender=email_data['sender'][:255],  # Truncate sender
                sender_email=email_data['sender_email'][:255],  # Truncate sender email
                body=validated_content['body'],
                snippet=email_data.get('snippet', '')[:500],  # Truncate snippet
                received_at=email_data['received_at']
            )
            db.session.add(email_record)
            db.session.flush()  # Get the email ID
            
            # Process email with AI to extract tasks
            tasks = ai_service.extract_tasks(email_data['subject'], email_data.get('body', ''), email_data['sender'])
            
            # Create task records with validation
            for task_data in tasks:
                try:
                    validated_task = validate_task_data(
                        task_data.get('description', ''),
                        task_data.get('priority'),
                        task_data.get('category')
                    )
                    
                    task = Task(
                        user_id=current_user_id,
                        email_id=email_record.id,
                        description=validated_task['description'],
                        sender=email_data['sender'][:255],  # Truncate sender
                        priority=validated_task['priority'],
                        category=validated_task['category']
                    )
                    db.session.add(task)
                    tasks_created += 1
                except ValidationError:
                    continue  # Skip invalid tasks
            
            email_record.mark_processed()
            processed_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Emails processed successfully',
            'emails_processed': processed_count,
            'tasks_created': tasks_created
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@emails_bp.route('/', methods=['GET'])
@jwt_required()
def get_emails():
    """Get processed emails for the current user"""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    processed = request.args.get('processed', type=str)
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Build query
    query = Email.query.filter_by(user_id=current_user_id)
    
    if processed is not None:
        if processed.lower() == 'true':
            query = query.filter_by(processed=True)
        elif processed.lower() == 'false':
            query = query.filter_by(processed=False)
    
    # Apply pagination and ordering
    emails = query.order_by(Email.received_at.desc()).limit(limit).offset(offset).all()
    
    return jsonify({
        'emails': [email.to_dict() for email in emails],
        'total': query.count()
    })

@emails_bp.route('/<int:email_id>', methods=['GET'])
@jwt_required()
def get_email(email_id):
    """Get a specific email by ID"""
    current_user_id = get_jwt_identity()
    
    email_record = Email.query.filter_by(id=email_id, user_id=current_user_id).first()
    if not email_record:
        return jsonify({'error': 'Email not found'}), 404
    
    return jsonify(email_record.to_dict())

@emails_bp.route('/<int:email_id>/tasks', methods=['GET'])
@jwt_required()
def get_email_tasks(email_id):
    """Get tasks associated with a specific email"""
    current_user_id = get_jwt_identity()
    
    email_record = Email.query.filter_by(id=email_id, user_id=current_user_id).first()
    if not email_record:
        return jsonify({'error': 'Email not found'}), 404
    
    tasks = Task.query.filter_by(email_id=email_id, user_id=current_user_id).all()
    
    return jsonify({
        'email': email_record.to_dict(),
        'tasks': [task.to_dict() for task in tasks]
    })

@emails_bp.route('/stats')
@jwt_required()
def get_email_stats():
    """Get email processing statistics"""
    current_user_id = get_jwt_identity()
    
    # Total emails
    total_emails = Email.query.filter_by(user_id=current_user_id).count()
    
    # Processed emails
    processed_emails = Email.query.filter_by(user_id=current_user_id, processed=True).count()
    
    # Emails with tasks
    emails_with_tasks = db.session.query(Email).join(Task).filter_by(user_id=current_user_id).distinct().count()
    
    # Recent emails (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_emails = Email.query.filter_by(user_id=current_user_id).filter(Email.received_at >= week_ago).count()
    
    return jsonify({
        'total_emails': total_emails,
        'processed_emails': processed_emails,
        'emails_with_tasks': emails_with_tasks,
        'recent_emails': recent_emails,
        'processing_rate': (processed_emails / total_emails * 100) if total_emails > 0 else 0
    })
