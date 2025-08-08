import re
import html
from flask import jsonify
from functools import wraps

class ValidationError(Exception):
    """Custom validation exception"""
    pass

def sanitize_text(text: str, max_length: int = None) -> str:
    """Sanitize text input to prevent XSS"""
    if not text:
        return ""
    
    # HTML escape
    sanitized = html.escape(text.strip())
    
    # Truncate if max_length specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_priority(priority: str) -> bool:
    """Validate task priority"""
    valid_priorities = ['High', 'Medium', 'Low']
    return priority in valid_priorities

def validate_category(category: str) -> bool:
    """Validate task category"""
    valid_categories = [
        'Follow-up', 'Meeting Prep', 'Purchase', 'General', 
        'Review', 'Approval', 'Schedule', 'Research'
    ]
    return category in valid_categories

def validate_json_input(required_fields: list = None, optional_fields: list = None):
    """Decorator to validate JSON input"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            # Check if request has JSON
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            # Check required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': f'Missing required fields: {", ".join(missing_fields)}'
                    }), 400
            
            # Validate allowed fields
            if optional_fields or required_fields:
                allowed_fields = set((required_fields or []) + (optional_fields or []))
                extra_fields = set(data.keys()) - allowed_fields
                if extra_fields:
                    return jsonify({
                        'error': f'Unexpected fields: {", ".join(extra_fields)}'
                    }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_email_content(subject: str, body: str) -> dict:
    """Validate and sanitize email content"""
    errors = []
    
    # Validate subject
    if not subject or len(subject.strip()) == 0:
        errors.append('Subject is required')
    elif len(subject) > 500:
        errors.append('Subject too long (max 500 characters)')
    
    # Validate body length (prevent huge AI processing costs)
    if body and len(body) > 50000:  # 50KB limit
        errors.append('Email body too long (max 50KB)')
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return {
        'subject': sanitize_text(subject, 500),
        'body': sanitize_text(body, 50000) if body else ""
    }

def validate_task_data(description: str, priority: str = None, category: str = None) -> dict:
    """Validate and sanitize task data"""
    errors = []
    
    # Validate description
    if not description or len(description.strip()) == 0:
        errors.append('Task description is required')
    elif len(description) > 1000:
        errors.append('Task description too long (max 1000 characters)')
    
    # Validate priority
    if priority and not validate_priority(priority):
        errors.append('Invalid priority. Must be High, Medium, or Low')
    
    # Validate category
    if category and not validate_category(category):
        errors.append('Invalid category')
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return {
        'description': sanitize_text(description, 1000),
        'priority': priority or 'Medium',
        'category': category or 'General'
    }