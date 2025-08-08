import axios, { AxiosInstance } from 'axios';
import { User, Task, Email, TaskStats, EmailStats } from '../types';
import { config } from '../config';

const API_BASE_URL = config.api.baseURL;

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: config.api.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      (axiosConfig) => {
        const token = localStorage.getItem(config.auth.tokenKey);
        if (token) {
          axiosConfig.headers.Authorization = `Bearer ${token}`;
        }
        return axiosConfig;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle auth errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem(config.auth.tokenKey);
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async googleAuthorize(): Promise<{ authorization_url: string }> {
    const response = await this.api.get('/auth/google/authorize');
    return response.data;
  }

  async logout(): Promise<void> {
    await this.api.post('/auth/logout');
    localStorage.removeItem(config.auth.tokenKey);
  }

  async refreshToken(): Promise<{ access_token: string }> {
    const response = await this.api.post('/auth/refresh');
    return response.data;
  }

  // User endpoints
  async getUserProfile(): Promise<User> {
    const response = await this.api.get('/user/profile');
    return response.data;
  }

  // Task endpoints
  async getTasks(params?: {
    completed?: boolean;
    priority?: string;
    category?: string;
    sort_by?: string;
    sort_order?: string;
  }): Promise<{ tasks: Task[]; total: number }> {
    const response = await this.api.get('/tasks', { params });
    return response.data;
  }

  async completeTask(taskId: number): Promise<Task> {
    const response = await this.api.put(`/tasks/${taskId}/complete`);
    return response.data;
  }

  async incompleteTask(taskId: number): Promise<Task> {
    const response = await this.api.put(`/tasks/${taskId}/incomplete`);
    return response.data;
  }

  async getTaskStats(): Promise<TaskStats> {
    const response = await this.api.get('/tasks/stats');
    return response.data;
  }

  async getCategories(): Promise<{ categories: string[] }> {
    const response = await this.api.get('/tasks/categories');
    return response.data;
  }

  async getPriorities(): Promise<{ priorities: string[] }> {
    const response = await this.api.get('/tasks/priorities');
    return response.data;
  }

  // Email endpoints
  async processEmails(): Promise<{
    message: string;
    emails_processed: number;
    tasks_created: number;
  }> {
    const response = await this.api.post('/emails/process');
    return response.data;
  }

  async getEmails(params?: {
    processed?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<{ emails: Email[]; total: number }> {
    const response = await this.api.get('/emails', { params });
    return response.data;
  }

  async getEmail(emailId: number): Promise<Email> {
    const response = await this.api.get(`/emails/${emailId}`);
    return response.data;
  }

  async getEmailTasks(emailId: number): Promise<{
    email: Email;
    tasks: Task[];
  }> {
    const response = await this.api.get(`/emails/${emailId}/tasks`);
    return response.data;
  }

  async getEmailStats(): Promise<EmailStats> {
    const response = await this.api.get('/emails/stats');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await this.api.get('/health');
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService;
