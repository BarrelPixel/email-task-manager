# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Email Task Manager is a full-stack AI-powered web application that extracts actionable tasks from Gmail emails using OpenAI's GPT-4. It features a React TypeScript frontend and a Python Flask backend with SQLite/PostgreSQL database support.

## Development Commands

### Frontend (React TypeScript)
```bash
cd frontend
npm install        # Install dependencies
npm start         # Start development server (port 3000)
npm run build     # Build for production
npm test          # Run tests with Jest
```

### Backend (Flask Python)
```bash
cd backend
pip install -r requirements.txt       # Install dependencies
python run.py                          # Start development server (port 5000)
python migrate_db.py                   # Add database indexes (one-time setup)
python test_app.py                     # Test backend functionality
```

### Full Setup
```bash
python setup.py   # Automated setup script for both frontend and backend
```

## Architecture Overview

### Backend Structure
- **Flask Application** (`app.py`): Main application with JWT authentication, CORS, and SQLAlchemy
- **Models** (`models/`): SQLAlchemy models for User, Task, and Email entities
- **Services** (`services/`):
  - `ai_service.py`: OpenAI GPT-4 integration for task extraction from email content
  - `gmail_service.py`: Google Gmail API integration with OAuth 2.0 authentication
- **Routes** (`routes/`): API endpoints organized by domain (auth, tasks, emails)

### Frontend Structure
- **React TypeScript** with Tailwind CSS for styling
- **Components** (`src/components/`): Reusable UI components (TaskList, TaskItem, TaskStats, etc.)
- **Pages** (`src/pages/`): Route-level components (Dashboard, Login)
- **Services** (`src/services/`): API client (`api.ts`) for backend communication
- **Types** (`src/types/`): TypeScript interfaces for data models

### Key Integrations
- **Google OAuth 2.0**: User authentication and Gmail API access
- **OpenAI GPT-4**: Intelligent task extraction with structured prompting
- **Gmail API**: Email fetching with filtering (inbox, last 7 days)
- **SQLite/PostgreSQL**: Database with SQLAlchemy ORM

## Data Flow
1. Users authenticate via Google OAuth to connect Gmail
2. Backend periodically fetches emails from Gmail API (configurable interval)
3. AI service processes email content and extracts actionable tasks
4. Tasks are categorized (Follow-up, Meeting Prep, etc.) and prioritized (High/Medium/Low)
5. Frontend displays tasks with filtering, completion tracking, and statistics

## Environment Configuration

### Backend (.env)
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///email_task_manager.db
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OPENAI_API_KEY=your-openai-api-key
```

### Security Considerations
- OAuth tokens are stored encrypted in database
- JWT tokens for session management
- CORS configured for development (localhost:3000)
- No sensitive data logged or committed

## Testing and Quality
- Frontend uses Jest and React Testing Library
- No specific backend test framework configured
- ESLint configured for frontend code quality

## Security & Performance Improvements

### Security Features
- **Token Encryption**: OAuth tokens encrypted in database using PBKDF2 + Fernet
- **Input Validation**: All user inputs sanitized and validated to prevent XSS
- **CORS Security**: Proper CORS configuration with specific origins
- **Rate Limiting**: API endpoints protected against abuse (5 requests/5min for email processing)
- **Session Security**: Secure session configuration with httpOnly and SameSite cookies

### Performance Optimizations
- **Database Indexes**: Comprehensive indexing on frequently queried columns
- **Optimized Queries**: Single aggregated queries for statistics instead of multiple calls
- **Pagination**: Task listing with pagination (max 100 items per page)
- **Rate Limiting**: Prevents API abuse and OpenAI cost overruns
- **Efficient Filtering**: Server-side filtering and sorting instead of client-side

## Development Notes
- Uses Flask application factory pattern to avoid circular imports
- Gmail API limited to inbox emails from last 7 days to avoid processing history
- AI service includes robust error handling and JSON parsing for GPT-4 responses
- Frontend uses centralized configuration management
- Email processing is configurable (intervals, batch sizes) via environment variables
- Database migration script available for adding indexes to existing databases