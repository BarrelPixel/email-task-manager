export interface User {
  id: number;
  email: string;
  name: string;
  gmail_connected: boolean;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  user_id: number;
  email_id: number;
  description: string;
  sender: string;
  priority: 'High' | 'Medium' | 'Low';
  category: string;
  completed: boolean;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
  email?: {
    subject: string;
    received_at: string;
  };
}

export interface Email {
  id: number;
  user_id: number;
  gmail_id: string;
  thread_id?: string;
  subject: string;
  sender: string;
  sender_email: string;
  body?: string;
  snippet?: string;
  processed: boolean;
  processed_at?: string;
  received_at: string;
  created_at: string;
  updated_at: string;
}

export interface TaskStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  completion_rate: number;
  priority_breakdown: {
    high: number;
    medium: number;
    low: number;
  };
  category_breakdown: Record<string, number>;
  recent_completed: number;
}

export interface EmailStats {
  total_emails: number;
  processed_emails: number;
  emails_with_tasks: number;
  recent_emails: number;
  processing_rate: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
