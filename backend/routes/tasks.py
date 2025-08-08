from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from run import db
from models.task import Task
from models.user import User

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks for the current user with pagination"""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    completed = request.args.get('completed', type=str)
    priority = request.args.get('priority', type=str)
    category = request.args.get('category', type=str)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)  # Max 100 items per page
    
    # Build query
    query = Task.query.filter_by(user_id=current_user_id)
    
    # Apply filters
    if completed is not None:
        if completed.lower() == 'true':
            query = query.filter_by(completed=True)
        elif completed.lower() == 'false':
            query = query.filter_by(completed=False)
    
    if priority:
        query = query.filter_by(priority=priority)
    
    if category:
        query = query.filter_by(category=category)
    
    # Apply sorting
    if sort_by == 'priority':
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        if sort_order == 'asc':
            query = query.order_by(db.case(priority_order, value=Task.priority))
        else:
            query = query.order_by(db.case(priority_order, value=Task.priority).desc())
    elif sort_by == 'created_at':
        if sort_order == 'asc':
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())
    elif sort_by == 'sender':
        if sort_order == 'asc':
            query = query.order_by(Task.sender.asc())
        else:
            query = query.order_by(Task.sender.desc())
    
    # Get paginated results
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'tasks': [task.to_dict() for task in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@tasks_bp.route('/<int:task_id>/complete', methods=['PUT'])
@jwt_required()
def complete_task(task_id):
    """Mark a task as complete"""
    current_user_id = get_jwt_identity()
    
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    task.mark_completed()
    db.session.commit()
    
    return jsonify(task.to_dict())

@tasks_bp.route('/<int:task_id>/incomplete', methods=['PUT'])
@jwt_required()
def incomplete_task(task_id):
    """Mark a task as incomplete"""
    current_user_id = get_jwt_identity()
    
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    task.completed = False
    task.completed_at = None
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(task.to_dict())

@tasks_bp.route('/stats')
@jwt_required()
def get_task_stats():
    """Get task statistics for the current user"""
    current_user_id = get_jwt_identity()
    
    # Use a single query with aggregation for better performance
    from sqlalchemy import func, case
    
    # Get all stats in one query
    stats_query = db.session.query(
        func.count(Task.id).label('total_tasks'),
        func.sum(case((Task.completed == True, 1), else_=0)).label('completed_tasks'),
        func.sum(case((Task.priority == 'High', case((Task.completed == False, 1), else_=0)), else_=0)).label('high_priority'),
        func.sum(case((Task.priority == 'Medium', case((Task.completed == False, 1), else_=0)), else_=0)).label('medium_priority'),
        func.sum(case((Task.priority == 'Low', case((Task.completed == False, 1), else_=0)), else_=0)).label('low_priority')
    ).filter_by(user_id=current_user_id).first()
    
    # Tasks by category (separate query as it needs GROUP BY)
    categories = db.session.query(Task.category, func.count(Task.id)).filter_by(
        user_id=current_user_id, completed=False
    ).group_by(Task.category).all()
    
    # Recent completed tasks (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_completed = Task.query.filter_by(
        user_id=current_user_id, completed=True
    ).filter(Task.completed_at >= week_ago).count()
    
    total_tasks = stats_query.total_tasks or 0
    completed_tasks = stats_query.completed_tasks or 0
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': total_tasks - completed_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'priority_breakdown': {
            'high': stats_query.high_priority or 0,
            'medium': stats_query.medium_priority or 0,
            'low': stats_query.low_priority or 0
        },
        'category_breakdown': dict(categories),
        'recent_completed': recent_completed
    })

@tasks_bp.route('/categories')
@jwt_required()
def get_categories():
    """Get all available task categories"""
    categories = [
        'Follow-up',
        'Meeting Prep',
        'Purchase',
        'General',
        'Review',
        'Approval',
        'Schedule',
        'Research'
    ]
    
    return jsonify({'categories': categories})

@tasks_bp.route('/priorities')
@jwt_required()
def get_priorities():
    """Get all available task priorities"""
    priorities = ['High', 'Medium', 'Low']
    
    return jsonify({'priorities': priorities})
