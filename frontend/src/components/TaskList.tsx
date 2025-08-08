import React, { useState, useEffect } from 'react';
import { Task } from '../types';
import TaskItem from './TaskItem';
import TaskFilters from './TaskFilters';

interface TaskListProps {
  tasks: Task[];
  filters: {
    completed?: boolean;
    priority: string;
    category: string;
    sort_by: string;
    sort_order: string;
  };
  onFilterChange: (filters: Partial<TaskListProps['filters']>) => void;
  onTaskComplete: (taskId: number, completed: boolean) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, filters, onFilterChange, onTaskComplete }) => {
  // Remove client-side filtering - now handled by backend

  if (tasks.length === 0) {
    return (
      <div className="card text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks found</h3>
        <p className="mt-1 text-sm text-gray-500">
          {filters.completed !== undefined || filters.priority || filters.category
            ? 'Try adjusting your filters to see more tasks.'
            : 'Get started by processing your emails to extract tasks.'}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters */}
      <TaskFilters filters={filters} onFilterChange={onFilterChange} />

      {/* Task Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-700">
          Showing {tasks.length} tasks
        </p>
      </div>

      {/* Task List */}
      <div className="space-y-4">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onComplete={(completed) => onTaskComplete(task.id, completed)}
          />
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="card text-center py-8">
          <p className="text-gray-500">No tasks match your current filters.</p>
          <button
            onClick={() => onFilterChange({ completed: undefined, priority: '', category: '' })}
            className="mt-2 text-primary-600 hover:text-primary-500 text-sm font-medium"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
};

export default TaskList;
