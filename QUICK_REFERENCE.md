# Quick Reference Guide

## 🚀 Quick Start Commands

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp env.example .env
python migrate_db.py
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🔧 Common Development Tasks

### Run Tests
```bash
cd backend
python run_tests.py          # Quick test run
pytest tests/ --cov=.        # With coverage
pytest tests/test_routes.py  # Specific test file
```

### Database Operations
```bash
cd backend
python migrate_db.py         # Initialize/update database
python -c "from run import db; db.create_all()"  # Create tables
```

### Environment Setup
```bash
# Backend .env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///email_task_manager.db
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OPENAI_API_KEY=your-openai-api-key
FRONTEND_URL=http://localhost:3000

# Frontend .env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

## 📁 Key Files & Directories

### Backend
- `run.py` - Application entry point
- `models/` - Database models (User, Task, Email)
- `routes/` - API endpoints (auth, tasks, emails)
- `services/` - Business logic (Gmail, AI)
- `utils/` - Utilities (encryption, validators)
- `tests/` - Test suite

### Frontend
- `src/App.tsx` - Main application component
- `src/pages/` - Page components (Login, Dashboard)
- `src/components/` - Reusable components
- `src/services/api.ts` - API service layer
- `src/types/index.ts` - TypeScript types

## 🔍 Common Issues & Solutions

### Backend Issues
1. **Import errors**: Ensure you're in the backend directory and virtual environment is activated
2. **Database errors**: Run `python migrate_db.py` to initialize database
3. **CORS errors**: Check `FRONTEND_URL` in backend .env matches frontend URL

### Frontend Issues
1. **API connection errors**: Verify `REACT_APP_API_URL` in frontend .env
2. **Build errors**: Clear node_modules and reinstall with `npm install`
3. **TypeScript errors**: Check types in `src/types/index.ts`

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/login` - Google OAuth login
- `POST /api/auth/logout` - Logout
- `GET /api/user/profile` - Get user profile

### Tasks
- `GET /api/tasks` - Get tasks (with pagination/filtering)
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PUT /api/tasks/:id/complete` - Mark task as complete

### Emails
- `POST /api/emails/process` - Process emails and extract tasks
- `GET /api/emails` - Get processed emails

### Health
- `GET /api/health` - Health check

## 🔐 Security Features

- JWT authentication with 24-hour expiry
- Rate limiting: 5 requests per 5 minutes per user
- Input validation and sanitization
- XSS protection
- Encrypted token storage
- CORS configuration

## 📊 Database Schema

### Users
- `id` (Primary Key)
- `email` (Unique)
- `name`
- `gmail_connected`
- `gmail_access_token` (Encrypted)
- `gmail_refresh_token` (Encrypted)
- `created_at`
- `updated_at`

### Tasks
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `email_id` (Foreign Key)
- `description`
- `priority` (High/Medium/Low)
- `category`
- `completed`
- `completed_at`
- `created_at`

### Emails
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `gmail_id` (Unique)
- `thread_id`
- `subject`
- `sender`
- `sender_email`
- `body`
- `snippet`
- `received_at`
- `processed`
- `processed_at`

## 🧪 Testing

### Test Structure
- `test_models.py` - Database model tests
- `test_routes.py` - API endpoint tests
- `test_services.py` - Business logic tests
- `test_integration.py` - Integration tests
- `test_utils.py` - Utility function tests

### Test Coverage
- Models: 95%+
- Routes: 90%+
- Services: 85%+
- Overall: 80%+

## 🚀 Deployment Checklist

### Backend
- [ ] Environment variables configured
- [ ] Database migrated
- [ ] Tests passing
- [ ] Security settings updated
- [ ] Logging configured
- [ ] Health checks working

### Frontend
- [ ] Environment variables configured
- [ ] Build successful
- [ ] API URLs updated
- [ ] Static assets optimized
- [ ] Error handling tested

## 📝 Update Instructions

**After making changes, update these files:**
1. `BRIEFING.md` - Main project documentation
2. `QUICK_REFERENCE.md` - This file
3. `README.md` - If public documentation changes
4. `CHANGELOG.md` - If you create one

### Update Format
```markdown
## Latest Updates
- [YYYY-MM-DD] - Description of changes
```

---

**Remember**: This is a living document. Update it as the project evolves!
