#!/usr/bin/env python3
"""
Email Task Manager Performance Optimizer Agent
Comprehensive performance analysis and optimization
"""

import os
import re
import ast
import json
import time
import sqlite3
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

class EmailTaskPerformanceOptimizer:
    """Specialized performance optimizer for Email Task Manager project"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"
        self.database_path = self.backend_path / "instance" / "app.db"
        
        self.optimizations = {
            'database': [],
            'queries': [],
            'api': [],
            'caching': [],
            'frontend': [],
            'memory': [],
            'networking': []
        }
        
        self.performance_metrics = {}
        self.bottlenecks = []
        
        # Performance thresholds
        self.thresholds = {
            'query_time_ms': 100,
            'api_response_ms': 500,
            'memory_usage_mb': 100,
            'cpu_usage_percent': 80,
            'database_size_mb': 500
        }
    
    def run_complete_optimization(self) -> Dict[str, Any]:
        """Run comprehensive performance optimization"""
        print("⚡ Starting Email Task Manager Performance Optimization...")
        
        # Database optimizations
        self._analyze_database_performance()
        self._optimize_database_queries()
        self._analyze_database_indexes()
        self._optimize_database_schema()
        
        # API optimizations
        self._analyze_api_performance()
        self._optimize_api_endpoints()
        self._implement_caching_strategies()
        self._optimize_serialization()
        
        # Frontend optimizations
        self._analyze_frontend_performance()
        self._optimize_frontend_bundles()
        self._implement_lazy_loading()
        
        # System optimizations
        self._analyze_memory_usage()
        self._optimize_resource_management()
        self._implement_monitoring()
        
        return self._generate_optimization_report()
    
    def _analyze_database_performance(self):
        """Analyze database performance and identify bottlenecks"""
        print("🗄️ Analyzing database performance...")
        
        if self.database_path.exists():
            try:
                conn = sqlite3.connect(str(self.database_path))
                cursor = conn.cursor()
                
                # Check database size
                db_size = self.database_path.stat().st_size / (1024 * 1024)  # MB
                if db_size > self.thresholds['database_size_mb']:
                    self.bottlenecks.append({
                        'type': 'Database Size',
                        'severity': 'Medium',
                        'issue': f'Database size: {db_size:.2f}MB exceeds threshold',
                        'recommendation': 'Implement data archiving and cleanup'
                    })
                
                # Analyze table statistics
                tables = ['users', 'tasks', 'emails']
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        
                        self.performance_metrics[f'{table}_count'] = count
                        
                        if count > 10000:
                            self.optimizations['database'].append({
                                'type': 'Large Table',
                                'table': table,
                                'records': count,
                                'recommendation': f'Consider partitioning {table} table'
                            })
                    except sqlite3.OperationalError:
                        continue
                
                # Check for missing indexes
                self._check_query_plans(cursor)
                
                conn.close()
                
            except Exception as e:
                print(f"Database analysis error: {e}")
    
    def _check_query_plans(self, cursor):
        """Check query execution plans for optimization opportunities"""
        common_queries = [
            "SELECT * FROM tasks WHERE user_id = ? AND completed = 0",
            "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
            "SELECT * FROM emails WHERE user_id = ? AND processed = 1",
            "SELECT COUNT(*) FROM tasks WHERE user_id = ? GROUP BY priority"
        ]
        
        for query in common_queries:
            try:
                # Analyze query plan
                cursor.execute(f"EXPLAIN QUERY PLAN {query}", (1,))
                plan = cursor.fetchall()
                
                # Check for table scans
                plan_text = ' '.join([str(row) for row in plan])
                if 'SCAN TABLE' in plan_text.upper():
                    table_match = re.search(r'SCAN TABLE (\w+)', plan_text.upper())
                    if table_match:
                        table_name = table_match.group(1).lower()
                        self.optimizations['queries'].append({
                            'type': 'Table Scan Detected',
                            'query': query,
                            'table': table_name,
                            'recommendation': f'Add index on {table_name} for better performance'
                        })
                        
            except sqlite3.OperationalError:
                continue
    
    def _optimize_database_queries(self):
        """Generate optimized database queries"""
        print("🚀 Optimizing database queries...")
        
        # Create optimized query suggestions
        optimized_queries = {
            'task_statistics': '''
-- Optimized task statistics query with single aggregation
SELECT 
    COUNT(*) as total_tasks,
    SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN priority = 'High' AND completed = 0 THEN 1 ELSE 0 END) as high_priority,
    SUM(CASE WHEN priority = 'Medium' AND completed = 0 THEN 1 ELSE 0 END) as medium_priority,
    SUM(CASE WHEN priority = 'Low' AND completed = 0 THEN 1 ELSE 0 END) as low_priority
FROM tasks 
WHERE user_id = ?
''',
            'recent_tasks_paginated': '''
-- Optimized paginated recent tasks with index usage
SELECT t.*, e.subject, e.sender 
FROM tasks t
LEFT JOIN emails e ON t.email_id = e.id
WHERE t.user_id = ? 
ORDER BY t.created_at DESC 
LIMIT ? OFFSET ?
''',
            'filtered_tasks_optimized': '''
-- Optimized filtered tasks using composite indexes
SELECT * FROM tasks 
WHERE user_id = ? 
    AND (? IS NULL OR priority = ?)
    AND (? IS NULL OR category = ?)
    AND (? IS NULL OR completed = ?)
ORDER BY created_at DESC
LIMIT ? OFFSET ?
''',
            'email_processing_batch': '''
-- Optimized batch email processing
SELECT * FROM emails 
WHERE user_id = ? 
    AND processed = 0 
    AND received_at > datetime('now', '-7 days')
ORDER BY received_at DESC 
LIMIT ?
'''
        }
        
        # Write optimized queries file
        queries_file = self.backend_path / "optimized_queries.sql"
        with open(queries_file, 'w') as f:
            f.write("-- Optimized Database Queries for Email Task Manager\n")
            f.write("-- Generated by Performance Optimizer Agent\n\n")
            
            for name, query in optimized_queries.items():
                f.write(f"-- {name.replace('_', ' ').title()}\n")
                f.write(query.strip() + "\n\n")
        
        self.optimizations['queries'].append({
            'type': 'Query Optimization',
            'file': str(queries_file),
            'improvements': len(optimized_queries),
            'recommendation': 'Replace existing queries with optimized versions'
        })
    
    def _analyze_database_indexes(self):
        """Analyze and suggest additional database indexes"""
        print("📊 Analyzing database indexes...")
        
        # Check existing indexes
        if self.database_path.exists():
            try:
                conn = sqlite3.connect(str(self.database_path))
                cursor = conn.cursor()
                
                # Get existing indexes
                cursor.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'")
                existing_indexes = cursor.fetchall()
                
                self.performance_metrics['existing_indexes'] = len(existing_indexes)
                
                # Suggest missing indexes based on common query patterns
                suggested_indexes = [
                    ("idx_tasks_user_created", "CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC)"),
                    ("idx_tasks_user_priority_completed", "CREATE INDEX idx_tasks_user_priority_completed ON tasks(user_id, priority, completed)"),
                    ("idx_tasks_user_category_completed", "CREATE INDEX idx_tasks_user_category_completed ON tasks(user_id, category, completed)"),
                    ("idx_emails_user_processed", "CREATE INDEX idx_emails_user_processed ON emails(user_id, processed)"),
                    ("idx_emails_user_received", "CREATE INDEX idx_emails_user_received ON emails(user_id, received_at DESC)"),
                    ("idx_tasks_email_id", "CREATE INDEX idx_tasks_email_id ON tasks(email_id)"),
                    ("idx_emails_thread_id", "CREATE INDEX idx_emails_thread_id ON emails(thread_id)"),
                    ("idx_tasks_completed_at", "CREATE INDEX idx_tasks_completed_at ON tasks(completed_at) WHERE completed = 1")
                ]
                
                # Check which indexes are missing
                existing_index_names = {idx[0] for idx in existing_indexes if idx[0]}
                
                missing_indexes = []
                for idx_name, idx_sql in suggested_indexes:
                    if idx_name not in existing_index_names:
                        missing_indexes.append((idx_name, idx_sql))
                
                if missing_indexes:
                    # Create index optimization script
                    index_script = self.backend_path / "optimize_indexes.py"
                    self._create_index_optimization_script(missing_indexes, index_script)
                    
                    self.optimizations['database'].append({
                        'type': 'Missing Indexes',
                        'count': len(missing_indexes),
                        'script': str(index_script),
                        'recommendation': 'Run index optimization script to improve query performance'
                    })
                
                conn.close()
                
            except Exception as e:
                print(f"Index analysis error: {e}")
    
    def _create_index_optimization_script(self, missing_indexes: List[Tuple[str, str]], script_path: Path):
        """Create script to add missing database indexes"""
        script_content = '''#!/usr/bin/env python3
"""
Database Index Optimization Script
Generated by Performance Optimizer Agent
"""

import sqlite3
import os
from pathlib import Path

def optimize_database_indexes():
    """Add missing database indexes for performance"""
    backend_path = Path(__file__).parent
    db_path = backend_path / "instance" / "app.db"
    
    if not db_path.exists():
        print("Database not found. Please run the application first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Performance indexes to add
        indexes = [
'''
        
        for idx_name, idx_sql in missing_indexes:
            script_content += f'            ("{idx_name}", """{idx_sql}"""),\n'
        
        script_content += '''        ]
        
        print("🚀 Adding performance indexes...")
        
        for idx_name, idx_sql in indexes:
            try:
                cursor.execute(idx_sql)
                print(f"✅ Created index: {idx_name}")
            except sqlite3.OperationalError as e:
                if "already exists" in str(e):
                    print(f"⏭️ Index already exists: {idx_name}")
                else:
                    print(f"❌ Error creating index {idx_name}: {e}")
        
        conn.commit()
        conn.close()
        
        print("\\n📊 Index optimization complete!")
        print("Database query performance should be significantly improved.")
        
        return True
        
    except Exception as e:
        print(f"Error optimizing indexes: {e}")
        return False

if __name__ == "__main__":
    success = optimize_database_indexes()
    exit(0 if success else 1)
'''
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        try:
            os.chmod(script_path, 0o755)
        except:
            pass
    
    def _optimize_database_schema(self):
        """Optimize database schema for better performance"""
        print("🔧 Optimizing database schema...")
        
        schema_optimizations = {
            'table_optimizations': [
                {
                    'table': 'tasks',
                    'optimization': 'Add partial index on active tasks',
                    'sql': 'CREATE INDEX idx_tasks_active ON tasks(user_id, priority) WHERE completed = 0'
                },
                {
                    'table': 'emails', 
                    'optimization': 'Add composite index for email processing',
                    'sql': 'CREATE INDEX idx_emails_processing ON emails(user_id, processed, received_at)'
                },
                {
                    'table': 'users',
                    'optimization': 'Add unique index on email for faster lookups',
                    'sql': 'CREATE UNIQUE INDEX idx_users_email ON users(email)'
                }
            ],
            'data_type_optimizations': [
                {
                    'field': 'tasks.priority',
                    'current': 'VARCHAR',
                    'suggested': 'INTEGER (enum)',
                    'benefit': 'Faster comparisons and less storage'
                },
                {
                    'field': 'tasks.completed',
                    'current': 'BOOLEAN',
                    'suggested': 'INTEGER (0/1)',
                    'benefit': 'Better SQLite compatibility'
                }
            ]
        }
        
        self.optimizations['database'].append({
            'type': 'Schema Optimization',
            'optimizations': schema_optimizations,
            'recommendation': 'Review and implement schema optimizations for better performance'
        })
    
    def _analyze_api_performance(self):
        """Analyze API endpoint performance"""
        print("🔌 Analyzing API performance...")
        
        # Find route files
        route_files = list(self.backend_path.glob("routes/*.py"))
        
        api_analysis = {
            'endpoints': [],
            'bottlenecks': [],
            'optimization_opportunities': []
        }
        
        for route_file in route_files:
            content = route_file.read_text()
            
            # Find route definitions
            routes = re.findall(r'@\w+\.route\([\'"]([^\'"]+)[\'"].*?\)\s*def\s+(\w+)', content, re.DOTALL)
            
            for route_path, function_name in routes:
                endpoint_analysis = self._analyze_endpoint(route_file, route_path, function_name, content)
                api_analysis['endpoints'].append(endpoint_analysis)
                
                # Check for performance issues
                if endpoint_analysis['issues']:
                    api_analysis['bottlenecks'].extend(endpoint_analysis['issues'])
        
        self.performance_metrics['api_endpoints'] = len(api_analysis['endpoints'])
        self.performance_metrics['api_bottlenecks'] = len(api_analysis['bottlenecks'])
        
        # Generate API optimization recommendations
        self._generate_api_optimizations(api_analysis)
    
    def _analyze_endpoint(self, file_path: Path, route_path: str, function_name: str, content: str) -> Dict[str, Any]:
        """Analyze individual API endpoint for performance issues"""
        issues = []
        
        # Extract function content
        func_pattern = rf'def {function_name}\(.*?\):(.*?)(?=\n(?:def|class|\Z))'
        func_match = re.search(func_pattern, content, re.DOTALL)
        
        if func_match:
            func_content = func_match.group(1)
            
            # Check for N+1 query problems
            if func_content.count('.query.') > 1 and 'for' in func_content:
                issues.append({
                    'type': 'N+1 Query Problem',
                    'severity': 'High',
                    'description': 'Multiple database queries in loop detected',
                    'recommendation': 'Use joins or bulk operations'
                })
            
            # Check for missing pagination
            if 'all()' in func_content and 'paginate' not in func_content:
                issues.append({
                    'type': 'Missing Pagination',
                    'severity': 'Medium', 
                    'description': 'Endpoint returns all records without pagination',
                    'recommendation': 'Implement pagination to handle large datasets'
                })
            
            # Check for inefficient serialization
            if 'to_dict()' in func_content and 'for' in func_content:
                issues.append({
                    'type': 'Inefficient Serialization',
                    'severity': 'Medium',
                    'description': 'Manual serialization in loop',
                    'recommendation': 'Use batch serialization or marshmallow schemas'
                })
            
            # Check for missing caching
            if 'SELECT' in func_content.upper() and '@cache' not in func_content:
                issues.append({
                    'type': 'Missing Caching',
                    'severity': 'Low',
                    'description': 'Expensive query without caching',
                    'recommendation': 'Add caching for frequently accessed data'
                })
        
        return {
            'file': str(file_path),
            'route': route_path,
            'function': function_name,
            'issues': issues
        }
    
    def _generate_api_optimizations(self, api_analysis: Dict[str, Any]):
        """Generate API optimization recommendations"""
        
        # Create optimized route examples
        optimized_routes = self.backend_path / "optimized_routes.py"
        
        optimization_content = '''"""
Optimized API Route Examples
Generated by Performance Optimizer Agent
"""

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.orm import joinedload
from sqlalchemy import func, and_

# Optimized task listing with efficient pagination and filtering
@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks_optimized():
    """Optimized task retrieval with proper pagination and eager loading"""
    user_id = get_jwt_identity()
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    
    # Filter parameters
    priority = request.args.get('priority')
    category = request.args.get('category') 
    completed = request.args.get('completed')
    
    # Build query with eager loading
    query = Task.query.options(
        joinedload(Task.email)
    ).filter_by(user_id=user_id)
    
    # Apply filters efficiently
    if priority:
        query = query.filter(Task.priority == priority)
    if category:
        query = query.filter(Task.category == category)
    if completed is not None:
        query = query.filter(Task.completed == (completed.lower() == 'true'))
    
    # Execute paginated query
    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, 
        per_page=per_page,
        error_out=False
    )
    
    # Efficient serialization
    return jsonify({
        'tasks': [task.to_dict() for task in tasks.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': tasks.total,
            'pages': tasks.pages
        }
    })

# Optimized task statistics with single aggregated query
@tasks_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_task_stats_optimized():
    """Optimized task statistics using single aggregated query"""
    user_id = get_jwt_identity()
    
    # Single aggregated query instead of multiple queries
    stats = db.session.query(
        func.count(Task.id).label('total_tasks'),
        func.sum(func.case([(Task.completed == True, 1)], else_=0)).label('completed'),
        func.sum(func.case([
            (and_(Task.priority == 'High', Task.completed == False), 1)
        ], else_=0)).label('high_priority'),
        func.sum(func.case([
            (and_(Task.priority == 'Medium', Task.completed == False), 1)
        ], else_=0)).label('medium_priority'),
        func.sum(func.case([
            (and_(Task.priority == 'Low', Task.completed == False), 1)
        ], else_=0)).label('low_priority')
    ).filter(Task.user_id == user_id).first()
    
    return jsonify({
        'total_tasks': stats.total_tasks or 0,
        'completed_tasks': stats.completed or 0,
        'pending_by_priority': {
            'high': stats.high_priority or 0,
            'medium': stats.medium_priority or 0,
            'low': stats.low_priority or 0
        }
    })

# Optimized bulk operations
@tasks_bp.route('/bulk-complete', methods=['POST'])
@jwt_required()
def bulk_complete_tasks():
    """Optimized bulk task completion"""
    user_id = get_jwt_identity()
    task_ids = request.json.get('task_ids', [])
    
    if not task_ids:
        return jsonify({'error': 'No task IDs provided'}), 400
    
    # Bulk update instead of individual updates
    updated_count = Task.query.filter(
        Task.id.in_(task_ids),
        Task.user_id == user_id
    ).update({
        Task.completed: True,
        Task.completed_at: func.now()
    }, synchronize_session='fetch')
    
    db.session.commit()
    
    return jsonify({
        'message': f'Completed {updated_count} tasks',
        'updated_count': updated_count
    })
'''
        
        with open(optimized_routes, 'w') as f:
            f.write(optimization_content)
        
        self.optimizations['api'].append({
            'type': 'Route Optimization',
            'file': str(optimized_routes),
            'improvements': 'Pagination, eager loading, aggregated queries, bulk operations',
            'recommendation': 'Replace inefficient routes with optimized versions'
        })
    
    def _optimize_api_endpoints(self):
        """Generate API endpoint optimizations"""
        print("🚀 Optimizing API endpoints...")
        
        # Create middleware for performance monitoring
        middleware_file = self.backend_path / "middleware" / "performance.py"
        middleware_file.parent.mkdir(exist_ok=True)
        
        middleware_content = '''"""
Performance Monitoring Middleware
Generated by Performance Optimizer Agent
"""

import time
import logging
from functools import wraps
from flask import request, g

# Set up performance logger
perf_logger = logging.getLogger('performance')
perf_logger.setLevel(logging.INFO)

def monitor_performance(f):
    """Decorator to monitor API endpoint performance"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            
            # Log performance metrics
            duration = (time.time() - start_time) * 1000  # ms
            
            if duration > 500:  # Slow request threshold
                perf_logger.warning(
                    f"Slow request: {request.method} {request.path} - {duration:.2f}ms"
                )
            
            # Add performance headers
            if hasattr(result, 'headers'):
                result.headers['X-Response-Time'] = f"{duration:.2f}ms"
            
            return result
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            perf_logger.error(
                f"Error in {request.method} {request.path} - {duration:.2f}ms: {str(e)}"
            )
            raise
    
    return decorated_function

def setup_performance_monitoring(app):
    """Set up performance monitoring for Flask app"""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        duration = (time.time() - g.start_time) * 1000
        
        # Add performance headers
        response.headers['X-Response-Time'] = f"{duration:.2f}ms"
        
        # Log slow requests
        if duration > 1000:  # 1 second threshold
            perf_logger.warning(
                f"Very slow request: {request.method} {request.path} - {duration:.2f}ms"
            )
        
        return response
'''
        
        with open(middleware_file, 'w') as f:
            f.write(middleware_content)
        
        self.optimizations['api'].append({
            'type': 'Performance Monitoring',
            'file': str(middleware_file),
            'features': 'Request timing, slow request logging, performance headers',
            'recommendation': 'Add to Flask app for performance monitoring'
        })
    
    def _implement_caching_strategies(self):
        """Implement caching strategies for improved performance"""
        print("💾 Implementing caching strategies...")
        
        # Create caching utility
        caching_file = self.backend_path / "utils" / "cache.py"
        
        caching_content = '''"""
Caching Utilities for Performance Optimization
Generated by Performance Optimizer Agent
"""

import time
import json
import hashlib
from functools import wraps
from typing import Any, Optional, Callable
from flask import current_app

class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key: str, default=None) -> Any:
        """Get value from cache"""
        if key in self.cache:
            # Check if expired
            if key in self.timestamps:
                if time.time() - self.timestamps[key]['created'] > self.timestamps[key]['ttl']:
                    del self.cache[key]
                    del self.timestamps[key]
                    return default
            return self.cache[key]
        return default
    
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL (time to live in seconds)"""
        self.cache[key] = value
        self.timestamps[key] = {
            'created': time.time(),
            'ttl': ttl
        }
    
    def delete(self, key: str) -> None:
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        self.timestamps.clear()
    
    def cleanup_expired(self) -> None:
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, timestamp_info in self.timestamps.items():
            if current_time - timestamp_info['created'] > timestamp_info['ttl']:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.delete(key)

# Global cache instance
cache = SimpleCache()

def cache_result(ttl: int = 300, key_func: Optional[Callable] = None):
    """Decorator to cache function results"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_data = {
                    'function': f.__name__,
                    'args': args,
                    'kwargs': kwargs
                }
                cache_key = hashlib.md5(
                    json.dumps(key_data, sort_keys=True, default=str).encode()
                ).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        
        return decorated_function
    return decorator

def cache_user_data(ttl: int = 300):
    """Cache decorator for user-specific data"""
    def key_func(*args, **kwargs):
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        return f"user_{user_id}_{args}_{kwargs}"
    
    return cache_result(ttl=ttl, key_func=key_func)

# Cache cleanup task (run periodically)
def cleanup_cache():
    """Cleanup expired cache entries"""
    cache.cleanup_expired()
'''
        
        with open(caching_file, 'w') as f:
            f.write(caching_content)
        
        # Create cached route examples
        cached_routes_file = self.backend_path / "cached_routes_examples.py"
        
        cached_examples = '''"""
Examples of cached routes for better performance
Generated by Performance Optimizer Agent
"""

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.utils.cache import cache_result, cache_user_data
from backend.models.task import Task

# Cache expensive statistics query
@tasks_bp.route('/stats', methods=['GET'])
@jwt_required()
@cache_user_data(ttl=300)  # Cache for 5 minutes per user
def get_cached_task_stats():
    """Get task statistics with caching"""
    user_id = get_jwt_identity()
    
    # This expensive query will be cached
    stats = db.session.query(
        func.count(Task.id).label('total'),
        func.sum(func.case([(Task.completed == True, 1)], else_=0)).label('completed')
    ).filter(Task.user_id == user_id).first()
    
    return jsonify({
        'total_tasks': stats.total or 0,
        'completed_tasks': stats.completed or 0
    })

# Cache user profile data
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
@cache_user_data(ttl=600)  # Cache for 10 minutes
def get_cached_user_profile():
    """Get user profile with caching"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

# Cache task categories and priorities (rarely change)
@cache_result(ttl=3600)  # Cache for 1 hour
def get_task_metadata():
    """Get task metadata with long-term caching"""
    categories = db.session.query(Task.category).distinct().all()
    priorities = db.session.query(Task.priority).distinct().all()
    
    return {
        'categories': [cat[0] for cat in categories if cat[0]],
        'priorities': [pri[0] for pri in priorities if pri[0]]
    }
'''
        
        with open(cached_routes_file, 'w') as f:
            f.write(cached_examples)
        
        self.optimizations['caching'].append({
            'type': 'Caching Implementation',
            'files': [str(caching_file), str(cached_routes_file)],
            'features': 'In-memory cache with TTL, user-specific caching, automatic cleanup',
            'recommendation': 'Implement caching for expensive queries and frequently accessed data'
        })
    
    def _optimize_serialization(self):
        """Optimize data serialization for better performance"""
        print("📦 Optimizing data serialization...")
        
        serialization_file = self.backend_path / "utils" / "serializers.py"
        
        serialization_content = '''"""
Optimized Serialization Utilities
Generated by Performance Optimizer Agent
"""

from typing import List, Dict, Any
import json
from datetime import datetime
from decimal import Decimal

class FastJSONEncoder(json.JSONEncoder):
    """Fast JSON encoder for common data types"""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)

def serialize_tasks_bulk(tasks: List) -> List[Dict[str, Any]]:
    """Optimized bulk serialization for tasks"""
    result = []
    
    for task in tasks:
        # Direct attribute access for better performance
        task_dict = {
            'id': task.id,
            'description': task.description,
            'priority': task.priority,
            'category': task.category,
            'completed': task.completed,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        }
        
        # Include email data if loaded
        if hasattr(task, 'email') and task.email:
            task_dict['email'] = {
                'id': task.email.id,
                'subject': task.email.subject,
                'sender': task.email.sender
            }
        
        result.append(task_dict)
    
    return result

def serialize_emails_bulk(emails: List) -> List[Dict[str, Any]]:
    """Optimized bulk serialization for emails"""
    result = []
    
    for email in emails:
        email_dict = {
            'id': email.id,
            'gmail_id': email.gmail_id,
            'subject': email.subject,
            'sender': email.sender,
            'sender_email': email.sender_email,
            'received_at': email.received_at.isoformat() if email.received_at else None,
            'processed': email.processed,
            'processed_at': email.processed_at.isoformat() if email.processed_at else None
        }
        
        result.append(email_dict)
    
    return result

def create_paginated_response(items: List, page: int, per_page: int, total: int) -> Dict[str, Any]:
    """Create optimized paginated response"""
    return {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,  # Ceiling division
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    }
'''
        
        with open(serialization_file, 'w') as f:
            f.write(serialization_content)
        
        self.optimizations['api'].append({
            'type': 'Serialization Optimization',
            'file': str(serialization_file),
            'improvements': 'Bulk serialization, fast JSON encoding, optimized pagination',
            'recommendation': 'Use optimized serializers for better API response times'
        })
    
    def _analyze_frontend_performance(self):
        """Analyze frontend performance bottlenecks"""
        print("🌐 Analyzing frontend performance...")
        
        frontend_issues = []
        
        # Check package.json for bundle size issues
        package_json = self.frontend_path / "package.json"
        if package_json.exists():
            with open(package_json) as f:
                package_data = json.load(f)
            
            dependencies = package_data.get('dependencies', {})
            
            # Check for heavy dependencies
            heavy_deps = ['lodash', 'moment', 'jquery']
            for dep in heavy_deps:
                if dep in dependencies:
                    frontend_issues.append({
                        'type': 'Heavy Dependency',
                        'dependency': dep,
                        'recommendation': f'Consider lighter alternative to {dep}'
                    })
        
        # Check TypeScript files for performance issues
        ts_files = list(self.frontend_path.glob("src/**/*.ts*"))
        
        for ts_file in ts_files:
            content = ts_file.read_text()
            
            # Check for inefficient patterns
            if 'map(' in content and 'filter(' in content:
                frontend_issues.append({
                    'type': 'Inefficient Array Operations',
                    'file': str(ts_file),
                    'recommendation': 'Combine map and filter operations'
                })
            
            if 'useState' in content and content.count('useState') > 5:
                frontend_issues.append({
                    'type': 'Excessive State',
                    'file': str(ts_file),
                    'recommendation': 'Consider useReducer or state management library'
                })
        
        self.optimizations['frontend'] = frontend_issues
    
    def _optimize_frontend_bundles(self):
        """Create frontend optimization suggestions"""
        print("📦 Optimizing frontend bundles...")
        
        # Create webpack optimization config
        webpack_config = self.frontend_path / "webpack.optimization.js"
        
        webpack_content = '''// Webpack optimization configuration
// Generated by Performance Optimizer Agent

const path = require('path');

module.exports = {
  // Bundle splitting for better caching
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\\\/]node_modules[\\\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        common: {
          name: 'common',
          minChunks: 2,
          chunks: 'all',
          enforce: true
        }
      }
    },
    // Minimize bundle size
    minimizer: [
      // Terser for JS minification
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: process.env.NODE_ENV === 'production'
          }
        }
      }),
      // CSS optimization
      new OptimizeCSSAssetsPlugin()
    ]
  },
  
  // Performance hints
  performance: {
    maxAssetSize: 250000,
    maxEntrypointSize: 250000,
    hints: process.env.NODE_ENV === 'production' ? 'warning' : false
  },
  
  // Tree shaking
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  
  // Resolve optimizations
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
};
'''
        
        with open(webpack_config, 'w') as f:
            f.write(webpack_content)
        
        self.optimizations['frontend'].append({
            'type': 'Bundle Optimization',
            'file': str(webpack_config),
            'features': 'Code splitting, tree shaking, minification',
            'recommendation': 'Configure webpack for production optimization'
        })
    
    def _implement_lazy_loading(self):
        """Create lazy loading examples for frontend"""
        print("⚡ Implementing lazy loading...")
        
        lazy_loading_file = self.frontend_path / "src" / "utils" / "lazyLoading.ts"
        lazy_loading_file.parent.mkdir(exist_ok=True)
        
        lazy_content = '''// Lazy loading utilities for performance optimization
// Generated by Performance Optimizer Agent

import { lazy, Suspense } from 'react';
import { ComponentType } from 'react';

// Higher-order component for lazy loading
export function withLazyLoading<T>(
  importFunc: () => Promise<{ default: ComponentType<T> }>,
  fallback: React.ComponentType = () => <div>Loading...</div>
) {
  const LazyComponent = lazy(importFunc);
  
  return function LazyWrapper(props: T) {
    return (
      <Suspense fallback={<fallback />}>
        <LazyComponent {...props} />
      </Suspense>
    );
  };
}

// Lazy load components
export const LazyDashboard = lazy(() => import('../pages/Dashboard'));
export const LazyTaskList = lazy(() => import('../components/TaskList'));
export const LazyEmailList = lazy(() => import('../components/EmailList'));

// Image lazy loading hook
export function useImageLazyLoading() {
  const imageRef = useRef<HTMLImageElement>(null);
  const [loaded, setLoaded] = useState(false);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !loaded) {
          setLoaded(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );
    
    if (imageRef.current) {
      observer.observe(imageRef.current);
    }
    
    return () => observer.disconnect();
  }, [loaded]);
  
  return { imageRef, loaded };
}

// Virtual scrolling for large lists
export function useVirtualScrolling<T>(
  items: T[],
  itemHeight: number,
  containerHeight: number
) {
  const [scrollTop, setScrollTop] = useState(0);
  
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight) + 1,
    items.length
  );
  
  const visibleItems = items.slice(startIndex, endIndex);
  
  return {
    visibleItems,
    startIndex,
    totalHeight: items.length * itemHeight,
    offsetY: startIndex * itemHeight,
    onScroll: (e: React.UIEvent<HTMLDivElement>) => {
      setScrollTop(e.currentTarget.scrollTop);
    }
  };
}
'''
        
        with open(lazy_loading_file, 'w') as f:
            f.write(lazy_content)
        
        self.optimizations['frontend'].append({
            'type': 'Lazy Loading Implementation',
            'file': str(lazy_loading_file),
            'features': 'Component lazy loading, image lazy loading, virtual scrolling',
            'recommendation': 'Implement lazy loading for better initial load performance'
        })
    
    def _analyze_memory_usage(self):
        """Analyze memory usage patterns"""
        print("💾 Analyzing memory usage...")
        
        # Create memory monitoring utility
        memory_monitor = self.backend_path / "utils" / "memory_monitor.py"
        
        memory_content = '''"""
Memory Usage Monitoring Utility
Generated by Performance Optimizer Agent
"""

import os
import psutil
import gc
import tracemalloc
from functools import wraps
from typing import Dict, Any

class MemoryMonitor:
    """Monitor and optimize memory usage"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_memory = self.get_memory_usage()
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage in MB"""
        memory_info = self.process.memory_info()
        
        return {
            'rss': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': self.process.memory_percent()
        }
    
    def memory_usage_decorator(self, threshold_mb: float = 100):
        """Decorator to monitor function memory usage"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Start memory tracking
                tracemalloc.start()
                start_memory = self.get_memory_usage()
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Check memory usage after function execution
                    end_memory = self.get_memory_usage()
                    memory_diff = end_memory['rss'] - start_memory['rss']
                    
                    if memory_diff > threshold_mb:
                        print(f"Warning: {func.__name__} used {memory_diff:.2f}MB of memory")
                        
                        # Get memory traceback
                        current, peak = tracemalloc.get_traced_memory()
                        print(f"Current memory: {current / 1024 / 1024:.2f}MB")
                        print(f"Peak memory: {peak / 1024 / 1024:.2f}MB")
                    
                    return result
                    
                finally:
                    tracemalloc.stop()
            
            return wrapper
        return decorator
    
    def cleanup_memory(self):
        """Force garbage collection and memory cleanup"""
        gc.collect()
        
        # Report memory usage after cleanup
        memory_usage = self.get_memory_usage()
        print(f"Memory usage after cleanup: {memory_usage['rss']:.2f}MB")
        
        return memory_usage

# Global memory monitor instance
memory_monitor = MemoryMonitor()

def monitor_memory_usage(threshold_mb: float = 50):
    """Decorator to monitor function memory usage"""
    return memory_monitor.memory_usage_decorator(threshold_mb)

def optimize_large_dataset_processing(data_batch_size: int = 1000):
    """Process large datasets in batches to optimize memory usage"""
    def decorator(func):
        @wraps(func)
        def wrapper(dataset, *args, **kwargs):
            if len(dataset) <= data_batch_size:
                return func(dataset, *args, **kwargs)
            
            results = []
            for i in range(0, len(dataset), data_batch_size):
                batch = dataset[i:i + data_batch_size]
                batch_result = func(batch, *args, **kwargs)
                results.extend(batch_result if isinstance(batch_result, list) else [batch_result])
                
                # Force garbage collection between batches
                gc.collect()
            
            return results
        
        return wrapper
    return decorator
'''
        
        with open(memory_monitor, 'w') as f:
            f.write(memory_content)
        
        self.optimizations['memory'].append({
            'type': 'Memory Monitoring',
            'file': str(memory_monitor),
            'features': 'Memory usage tracking, batch processing, garbage collection',
            'recommendation': 'Use memory monitoring decorators for memory-intensive operations'
        })
    
    def _optimize_resource_management(self):
        """Optimize resource management"""
        print("🔧 Optimizing resource management...")
        
        resource_manager = self.backend_path / "utils" / "resource_manager.py"
        
        resource_content = '''"""
Resource Management Optimization
Generated by Performance Optimizer Agent
"""

import threading
import time
from contextlib import contextmanager
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class ResourcePool:
    """Generic resource pool for connection management"""
    
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.pool = []
        self.in_use = set()
        self.lock = threading.Lock()
    
    def get_resource(self):
        """Get resource from pool"""
        with self.lock:
            if self.pool:
                resource = self.pool.pop()
                self.in_use.add(resource)
                return resource
            
            if len(self.in_use) < self.max_size:
                resource = self._create_resource()
                self.in_use.add(resource)
                return resource
            
            return None  # Pool exhausted
    
    def return_resource(self, resource):
        """Return resource to pool"""
        with self.lock:
            if resource in self.in_use:
                self.in_use.remove(resource)
                self.pool.append(resource)
    
    def _create_resource(self):
        """Override this method to create specific resources"""
        return object()

class OptimizedTaskProcessor:
    """Optimized task processing with resource management"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = []
        self.processing_stats = {
            'processed': 0,
            'failed': 0,
            'average_time': 0
        }
    
    def process_tasks_parallel(self, tasks, processor_func):
        """Process tasks in parallel with optimal resource usage"""
        futures = []
        
        for task in tasks:
            future = self.executor.submit(self._safe_process_task, task, processor_func)
            futures.append(future)
        
        results = []
        start_time = time.time()
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                self.processing_stats['processed'] += 1
            except Exception as e:
                print(f"Task processing error: {e}")
                self.processing_stats['failed'] += 1
        
        # Update average processing time
        total_time = time.time() - start_time
        self.processing_stats['average_time'] = total_time / len(tasks) if tasks else 0
        
        return results
    
    def _safe_process_task(self, task, processor_func):
        """Safely process individual task"""
        try:
            return processor_func(task)
        except Exception as e:
            print(f"Error processing task {task}: {e}")
            raise

@contextmanager
def database_transaction_manager(db_session):
    """Context manager for safe database transactions"""
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Database transaction error: {e}")
        raise
    finally:
        db_session.close()

class RequestLimiter:
    """Request rate limiter with token bucket algorithm"""
    
    def __init__(self, rate_limit: int, time_window: int = 60):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.tokens = rate_limit
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def allow_request(self) -> bool:
        """Check if request is allowed based on rate limit"""
        with self.lock:
            now = time.time()
            
            # Refill tokens
            time_passed = now - self.last_refill
            tokens_to_add = int(time_passed * (self.rate_limit / self.time_window))
            
            if tokens_to_add > 0:
                self.tokens = min(self.rate_limit, self.tokens + tokens_to_add)
                self.last_refill = now
            
            # Check if request is allowed
            if self.tokens > 0:
                self.tokens -= 1
                return True
            
            return False
'''
        
        with open(resource_manager, 'w') as f:
            f.write(resource_content)
        
        self.optimizations['memory'].append({
            'type': 'Resource Management',
            'file': str(resource_manager),
            'features': 'Connection pooling, parallel processing, transaction management, rate limiting',
            'recommendation': 'Use resource management utilities for better performance and stability'
        })
    
    def _implement_monitoring(self):
        """Implement performance monitoring"""
        print("📊 Implementing performance monitoring...")
        
        monitoring_file = self.backend_path / "monitoring" / "performance_dashboard.py"
        monitoring_file.parent.mkdir(exist_ok=True)
        
        monitoring_content = '''"""
Performance Monitoring Dashboard
Generated by Performance Optimizer Agent
"""

import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, deque
from flask import Flask, jsonify, render_template_string

class PerformanceMetrics:
    """Collect and store performance metrics"""
    
    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.metrics = defaultdict(deque)
        self.lock = threading.Lock()
        
        # Metric categories
        self.categories = {
            'api_response_times': deque(maxlen=max_samples),
            'database_query_times': deque(maxlen=max_samples),
            'memory_usage': deque(maxlen=max_samples),
            'active_users': deque(maxlen=max_samples),
            'error_rates': deque(maxlen=max_samples)
        }
    
    def record_api_response(self, endpoint: str, response_time: float, status_code: int):
        """Record API response metrics"""
        with self.lock:
            metric = {
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint,
                'response_time': response_time,
                'status_code': status_code
            }
            self.categories['api_response_times'].append(metric)
    
    def record_db_query(self, query_type: str, execution_time: float):
        """Record database query metrics"""
        with self.lock:
            metric = {
                'timestamp': datetime.now().isoformat(),
                'query_type': query_type,
                'execution_time': execution_time
            }
            self.categories['database_query_times'].append(metric)
    
    def record_memory_usage(self, usage_mb: float):
        """Record memory usage metrics"""
        with self.lock:
            metric = {
                'timestamp': datetime.now().isoformat(),
                'usage_mb': usage_mb
            }
            self.categories['memory_usage'].append(metric)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        with self.lock:
            summary = {}
            
            # API response time summary
            api_times = [m['response_time'] for m in self.categories['api_response_times']]
            if api_times:
                summary['api_response_times'] = {
                    'avg': sum(api_times) / len(api_times),
                    'min': min(api_times),
                    'max': max(api_times),
                    'count': len(api_times)
                }
            
            # Database query summary
            db_times = [m['execution_time'] for m in self.categories['database_query_times']]
            if db_times:
                summary['database_query_times'] = {
                    'avg': sum(db_times) / len(db_times),
                    'min': min(db_times),
                    'max': max(db_times),
                    'count': len(db_times)
                }
            
            # Memory usage summary
            memory_usage = [m['usage_mb'] for m in self.categories['memory_usage']]
            if memory_usage:
                summary['memory_usage'] = {
                    'avg': sum(memory_usage) / len(memory_usage),
                    'min': min(memory_usage),
                    'max': max(memory_usage),
                    'current': memory_usage[-1] if memory_usage else 0
                }
            
            return summary

# Global metrics collector
metrics_collector = PerformanceMetrics()

def create_monitoring_app():
    """Create Flask app for performance monitoring dashboard"""
    app = Flask(__name__)
    
    @app.route('/performance/metrics')
    def get_metrics():
        """Get current performance metrics"""
        return jsonify(metrics_collector.get_summary())
    
    @app.route('/performance/dashboard')
    def dashboard():
        """Performance monitoring dashboard"""
        dashboard_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Performance Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .metric-card { 
                    background: #f5f5f5; 
                    padding: 20px; 
                    margin: 10px; 
                    border-radius: 5px;
                    display: inline-block;
                    width: 300px;
                    vertical-align: top;
                }
                .metric-value { font-size: 24px; font-weight: bold; color: #2196F3; }
                .metric-label { color: #666; }
                canvas { margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1>Email Task Manager - Performance Dashboard</h1>
            
            <div id="metrics-cards"></div>
            
            <canvas id="responseTimeChart" width="800" height="400"></canvas>
            
            <script>
                // Fetch and display metrics
                function updateDashboard() {
                    fetch('/performance/metrics')
                        .then(response => response.json())
                        .then(data => {
                            updateMetricCards(data);
                            updateCharts(data);
                        });
                }
                
                function updateMetricCards(data) {
                    const container = document.getElementById('metrics-cards');
                    container.innerHTML = '';
                    
                    // API Response Times
                    if (data.api_response_times) {
                        const apiCard = createMetricCard(
                            'API Response Time',
                            data.api_response_times.avg.toFixed(2) + 'ms',
                            `Min: ${data.api_response_times.min.toFixed(2)}ms, Max: ${data.api_response_times.max.toFixed(2)}ms`
                        );
                        container.appendChild(apiCard);
                    }
                    
                    // Memory Usage
                    if (data.memory_usage) {
                        const memoryCard = createMetricCard(
                            'Memory Usage',
                            data.memory_usage.current.toFixed(2) + 'MB',
                            `Avg: ${data.memory_usage.avg.toFixed(2)}MB, Max: ${data.memory_usage.max.toFixed(2)}MB`
                        );
                        container.appendChild(memoryCard);
                    }
                    
                    // Database Queries
                    if (data.database_query_times) {
                        const dbCard = createMetricCard(
                            'Database Query Time',
                            data.database_query_times.avg.toFixed(2) + 'ms',
                            `Count: ${data.database_query_times.count}`
                        );
                        container.appendChild(dbCard);
                    }
                }
                
                function createMetricCard(title, value, subtitle) {
                    const card = document.createElement('div');
                    card.className = 'metric-card';
                    card.innerHTML = `
                        <div class="metric-label">${title}</div>
                        <div class="metric-value">${value}</div>
                        <div class="metric-label">${subtitle}</div>
                    `;
                    return card;
                }
                
                // Update dashboard every 30 seconds
                updateDashboard();
                setInterval(updateDashboard, 30000);
            </script>
        </body>
        </html>
        """
        
        return dashboard_html
    
    return app

# Performance monitoring middleware
def setup_performance_monitoring(main_app):
    """Set up performance monitoring middleware"""
    
    @main_app.before_request
    def before_request():
        from flask import g, request
        g.start_time = time.time()
    
    @main_app.after_request
    def after_request(response):
        from flask import g, request
        
        if hasattr(g, 'start_time'):
            response_time = (time.time() - g.start_time) * 1000  # Convert to ms
            
            # Record metrics
            metrics_collector.record_api_response(
                endpoint=request.endpoint or request.path,
                response_time=response_time,
                status_code=response.status_code
            )
        
        return response
'''
        
        with open(monitoring_file, 'w') as f:
            f.write(monitoring_content)
        
        self.optimizations['networking'].append({
            'type': 'Performance Monitoring',
            'file': str(monitoring_file),
            'features': 'Real-time metrics collection, performance dashboard, monitoring middleware',
            'recommendation': 'Implement performance monitoring for production visibility'
        })
    
    def _generate_optimization_report(self) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        
        total_optimizations = sum(len(opts) for opts in self.optimizations.values())
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': 'Email Task Manager',
            'total_optimizations': total_optimizations,
            'performance_metrics': self.performance_metrics,
            'bottlenecks': self.bottlenecks,
            'optimizations': self.optimizations,
            'recommendations': [
                "🗄️ Run database index optimization script for query performance",
                "🚀 Implement caching strategies for frequently accessed data",
                "📊 Add performance monitoring to track improvements",
                "⚡ Use optimized serializers for better API response times",
                "💾 Implement memory monitoring for resource-intensive operations",
                "🌐 Add bundle optimization for faster frontend loading",
                "🔄 Set up regular performance testing and benchmarking"
            ],
            'implementation_priority': [
                "1. Database Index Optimization (High Impact)",
                "2. API Endpoint Caching (Medium Impact)",
                "3. Query Optimization (High Impact)",
                "4. Performance Monitoring Setup (Low Impact, High Visibility)",
                "5. Frontend Bundle Optimization (Medium Impact)",
                "6. Memory Usage Optimization (Low Impact)"
            ]
        }
        
        # Save report
        report_file = self.project_root / "performance_optimization_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n⚡ Performance Optimization Complete!")
        print(f"Total Optimizations: {total_optimizations}")
        print(f"Categories: {list(self.optimizations.keys())}")
        print(f"Report saved to: {report_file}")
        
        return report


def main():
    """Main execution function"""
    import sys
    
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    optimizer = EmailTaskPerformanceOptimizer(project_root)
    report = optimizer.run_complete_optimization()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"PERFORMANCE OPTIMIZATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Optimizations: {report['total_optimizations']}")
    print(f"Database Optimizations: {len(report['optimizations']['database'])}")
    print(f"API Optimizations: {len(report['optimizations']['api'])}")
    print(f"Caching Optimizations: {len(report['optimizations']['caching'])}")
    print(f"Frontend Optimizations: {len(report['optimizations']['frontend'])}")
    print(f"Memory Optimizations: {len(report['optimizations']['memory'])}")
    print(f"Bottlenecks Found: {len(report['bottlenecks'])}")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)