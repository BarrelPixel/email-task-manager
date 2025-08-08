# Quick Start Guide

This guide will help you get the Email Task Manager up and running in under 10 minutes.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Google Cloud Platform account (for OAuth)
- OpenAI API key

## Step 1: Clone and Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd email-task-manager
```

2. **Run the setup script**:
```bash
python setup.py
```

This will:
- Create virtual environments
- Install dependencies
- Create configuration files

## Step 2: Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:5000/api/auth/google/callback`
5. Download the credentials

## Step 3: Configure Environment

1. **Edit `backend/.env`**:
```bash
# Replace these values with your actual credentials
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-strong-secret-key-here
FRONTEND_URL=http://localhost:3000
ENCRYPTION_SALT=your-unique-salt-change-in-production
```

## Step 4: Initialize Database

1. **Set up database indexes** (First time only):
```bash
cd backend
python migrate_db.py
```

## Step 5: Start the Application

1. **Start the backend** (Terminal 1):
```bash
cd backend
python run.py
```

2. **Start the frontend** (Terminal 2):
```bash
cd frontend
npm start
```

## Step 6: Access the Application

1. Open your browser to `http://localhost:3000`
2. Click "Connect with Google"
3. Authorize the application
4. Start using the Email Task Manager!

## What You Can Do

- **Connect Gmail**: Securely link your Gmail account with encrypted token storage
- **Process Emails**: Extract tasks from your inbox with AI (rate limited for security)
- **View Tasks**: See paginated tasks with optimized loading and filtering
- **Complete Tasks**: Mark tasks as done with real-time statistics updates
- **Filter & Sort**: Server-side filtering by priority, category, completion status
- **View Stats**: Comprehensive analytics with optimized database queries
- **Secure Access**: All data protected with enterprise-level security measures

## Troubleshooting

### Common Issues

1. **"Gmail not connected" error**:
   - Make sure you've completed the Google OAuth flow
   - Check that your Google OAuth credentials are correct

2. **"Failed to process emails" error**:
   - Verify your OpenAI API key is valid
   - Check that you have sufficient API credits

3. **CORS errors**:
   - Ensure both frontend (port 3000) and backend (port 5000) are running
   - Check that the API URL in frontend matches the backend

4. **Database errors**:
   - Make sure the backend can write to the current directory
   - Check that SQLite is working properly

### Getting Help

- Check the logs in the terminal where you started the backend
- Verify all environment variables are set correctly
- Ensure all dependencies are installed
- Run `python test_app.py` in the backend directory to test functionality
- Check that database indexes were created with `python migrate_db.py`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Review the code structure in the `backend/` and `frontend/` directories

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Ensure all prerequisites are met
4. Create an issue in the project repository

Happy task managing! 🎯
