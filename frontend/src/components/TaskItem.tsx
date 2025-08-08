import React from 'react';
import { Task } from '../types';

interface TaskItemProps {
  task: Task;
  onComplete: (completed: boolean) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onComplete }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'badge-high';
      case 'Medium':
        return 'badge-medium';
      case 'Low':
        return 'badge-low';
      default:
        return 'badge-medium';
    }
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      'Follow-up': 'bg-blue-100 text-blue-800',
      'Meeting Prep': 'bg-purple-100 text-purple-800',
      'Purchase': 'bg-green-100 text-green-800',
      'General': 'bg-gray-100 text-gray-800',
      'Review': 'bg-yellow-100 text-yellow-800',
      'Approval': 'bg-red-100 text-red-800',
      'Schedule': 'bg-indigo-100 text-indigo-800',
      'Research': 'bg-pink-100 text-pink-800',
    };
    return colors[category as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className={`card transition-all duration-200 ${task.completed ? 'opacity-75' : ''}`}>
      <div className="flex items-start space-x-4">
        {/* Checkbox */}
        <div className="flex-shrink-0 pt-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={(e) => onComplete(e.target.checked)}
            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
        </div>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.description}
              </h3>
              
              <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                <span className="flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {task.sender}
                </span>
                
                {task.email && (
                  <span className="flex items-center">
                    <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {task.email.subject}
                  </span>
                )}
                
                <span className="flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {formatDate(task.created_at)}
                </span>
              </div>
            </div>

            {/* Priority and Category Badges */}
            <div className="flex flex-col items-end space-y-2">
              <span className={`badge ${getPriorityColor(task.priority)}`}>
                {task.priority}
              </span>
              <span className={`badge ${getCategoryColor(task.category)}`}>
                {task.category}
              </span>
            </div>
          </div>

          {/* Completion Info */}
          {task.completed && task.completed_at && (
            <div className="mt-2 flex items-center text-xs text-green-600">
              <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Completed {formatDate(task.completed_at)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskItem;
