import React, { useState, useEffect } from 'react';
import apiService from '../services/api';

interface TaskFiltersProps {
  filters: {
    completed?: boolean;
    priority: string;
    category: string;
    sort_by: string;
    sort_order: string;
  };
  onFilterChange: (filters: Partial<TaskFiltersProps['filters']>) => void;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({ filters, onFilterChange }) => {
  const [categories, setCategories] = useState<string[]>([]);
  const [priorities, setPriorities] = useState<string[]>([]);

  useEffect(() => {
    const loadFilterOptions = async () => {
      try {
        const [categoriesData, prioritiesData] = await Promise.all([
          apiService.getCategories(),
          apiService.getPriorities()
        ]);
        setCategories(categoriesData.categories);
        setPriorities(prioritiesData.priorities);
      } catch (error) {
        console.error('Failed to load filter options:', error);
      }
    };

    loadFilterOptions();
  }, []);

  return (
    <div className="card">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            value={filters.completed === undefined ? '' : filters.completed.toString()}
            onChange={(e) => {
              const value = e.target.value;
              onFilterChange({
                completed: value === '' ? undefined : value === 'true'
              });
            }}
            className="input text-sm"
          >
            <option value="">All</option>
            <option value="false">Pending</option>
            <option value="true">Completed</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            value={filters.priority}
            onChange={(e) => onFilterChange({ priority: e.target.value })}
            className="input text-sm"
          >
            <option value="">All Priorities</option>
            {priorities.map((priority) => (
              <option key={priority} value={priority}>
                {priority}
              </option>
            ))}
          </select>
        </div>

        {/* Category Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            value={filters.category}
            onChange={(e) => onFilterChange({ category: e.target.value })}
            className="input text-sm"
          >
            <option value="">All Categories</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        {/* Sort By */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Sort By
          </label>
          <select
            value={filters.sort_by}
            onChange={(e) => onFilterChange({ sort_by: e.target.value })}
            className="input text-sm"
          >
            <option value="created_at">Date Created</option>
            <option value="priority">Priority</option>
            <option value="sender">Sender</option>
          </select>
        </div>

        {/* Sort Order */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Sort Order
          </label>
          <select
            value={filters.sort_order}
            onChange={(e) => onFilterChange({ sort_order: e.target.value })}
            className="input text-sm"
          >
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>
        </div>
      </div>

      {/* Clear Filters */}
      {(filters.completed !== undefined || filters.priority || filters.category) && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <button
            onClick={() => onFilterChange({ completed: undefined, priority: '', category: '' })}
            className="text-sm text-primary-600 hover:text-primary-500 font-medium"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
};

export default TaskFilters;
