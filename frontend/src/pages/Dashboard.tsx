import React, { useState, useEffect, useCallback } from 'react';
import { User, Task, TaskStats as TaskStatsType } from '../types';
import apiService from '../services/api';
import TaskList from '../components/TaskList';
import TaskStatsComponent from '../components/TaskStats';
import Header from '../components/Header';
import LoadingSpinner from '../components/LoadingSpinner';

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ user, onLogout }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<TaskStatsType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessingEmails, setIsProcessingEmails] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    completed: undefined as boolean | undefined,
    priority: '',
    category: '',
    sort_by: 'created_at',
    sort_order: 'desc'
  });

  const loadTasks = useCallback(async () => {
    try {
      const response = await apiService.getTasks(filters);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
      setError('Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  }, [filters]);

  const loadStats = useCallback(async () => {
    try {
      const statsData = await apiService.getTaskStats();
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  }, []);

  useEffect(() => {
    loadTasks();
    loadStats();
  }, [loadTasks, loadStats]);

  const handleProcessEmails = async () => {
    setIsProcessingEmails(true);
    setError(null);

    try {
      const result = await apiService.processEmails();
      await loadTasks();
      await loadStats();
      
      // Show success message
      alert(`Processed ${result.emails_processed} emails and created ${result.tasks_created} tasks`);
    } catch (error) {
      console.error('Failed to process emails:', error);
      setError('Failed to process emails. Please try again.');
    } finally {
      setIsProcessingEmails(false);
    }
  };

  const handleTaskComplete = async (taskId: number, completed: boolean) => {
    try {
      if (completed) {
        await apiService.completeTask(taskId);
      } else {
        await apiService.incompleteTask(taskId);
      }
      
      // Update local state
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId
            ? { ...task, completed, completed_at: completed ? new Date().toISOString() : null }
            : task
        )
      );
      
      // Reload stats
      await loadStats();
    } catch (error) {
      console.error('Failed to update task:', error);
      setError('Failed to update task status');
    }
  };

  const handleFilterChange = (newFilters: Partial<typeof filters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onLogout={onLogout} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Section */}
        {stats && (
          <div className="mb-8">
            <TaskStatsComponent stats={stats} />
          </div>
        )}

        {/* Actions Section */}
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
            <p className="text-gray-600">Manage your extracted tasks from emails</p>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={handleProcessEmails}
              disabled={isProcessingEmails || !user.gmail_connected}
              className="btn btn-primary flex items-center"
            >
              {isProcessingEmails ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Processing...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Process Emails
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{error}</h3>
              </div>
            </div>
          </div>
        )}

        {/* Task List */}
        <TaskList
          tasks={tasks}
          filters={filters}
          onFilterChange={handleFilterChange}
          onTaskComplete={handleTaskComplete}
        />
      </div>
    </div>
  );
};

export default Dashboard;
