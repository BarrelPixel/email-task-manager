"""Rate limiting utilities for API endpoints"""
import time
from functools import wraps
from flask import jsonify, request, g
import threading
from collections import defaultdict, deque

# Import Flask JWT extensions at module level
try:
    from flask_jwt_extended import get_jwt_identity, jwt_required
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.clients = defaultdict(deque)
        self.lock = threading.Lock()
    
    def is_allowed(self, client_id: str, limit: int, window: int) -> bool:
        """Check if client is within rate limit"""
        with self.lock:
            now = time.time()
            
            # Clean old entries
            while (self.clients[client_id] and 
                   self.clients[client_id][0] < now - window):
                self.clients[client_id].popleft()
            
            # Check if limit exceeded
            if len(self.clients[client_id]) >= limit:
                return False
            
            # Add current request
            self.clients[client_id].append(now)
            return True

# Global rate limiter instance
rate_limiter = RateLimiter()

def ratelimit(limit: int, window: int = 60, per: str = 'ip'):
    """
    Rate limiting decorator
    
    Args:
        limit: Number of requests allowed
        window: Time window in seconds (default 60s)
        per: Rate limit per ('ip' or 'user')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Determine client identifier
            if per == 'user' and JWT_AVAILABLE:
                try:
                    client_id = f"user_{get_jwt_identity()}"
                except:
                    client_id = f"ip_{request.remote_addr}"
            else:
                client_id = f"ip_{request.remote_addr}"
            
            # Check rate limit
            if not rate_limiter.is_allowed(client_id, limit, window):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Limit: {limit} per {window} seconds'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator