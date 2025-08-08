// Application configuration
export const config = {
  api: {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
    timeout: 30000, // 30 seconds
  },
  app: {
    name: process.env.REACT_APP_APP_NAME || 'Email Task Manager',
    version: process.env.REACT_APP_VERSION || '1.0.0',
  },
  features: {
    debug: process.env.REACT_APP_ENABLE_DEBUG === 'true',
    analytics: process.env.REACT_APP_ENABLE_ANALYTICS === 'true',
  },
  auth: {
    tokenKey: 'email_task_manager_token',
    sessionTimeout: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
  },
  validation: {
    maxEmailBodyLength: 50000,
    maxTaskDescriptionLength: 1000,
    maxSubjectLength: 500,
  },
};

// Validate required environment variables
const requiredEnvVars = ['REACT_APP_API_URL'];
const missingEnvVars = requiredEnvVars.filter(
  (envVar) => !process.env[envVar]
);

if (missingEnvVars.length > 0 && process.env.NODE_ENV === 'production') {
  console.error('Missing required environment variables:', missingEnvVars);
}