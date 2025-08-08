# AI-Powered Email Task Manager

An intelligent web application that automatically extracts and organizes actionable tasks from your Gmail inbox using AI.

## Features

- 🔐 Secure Google OAuth authentication with encrypted token storage
- 🤖 AI-powered task extraction from emails with rate limiting
- 📊 Clean dashboard with categorized and paginated tasks
- 🎯 Automatic priority inference with optimized database queries
- ✅ Task completion tracking with comprehensive statistics
- 📱 Modern, responsive web interface with centralized configuration
- 🛡️ Enterprise-level security with input validation and XSS protection
- ⚡ High-performance database with optimized indexes and queries
- 🧪 Comprehensive testing suite with 80%+ coverage

## Tech Stack

- **Frontend**: React + TypeScript + Tailwind CSS with centralized configuration
- **Backend**: Python Flask + SQLAlchemy with application factory pattern
- **Database**: SQLite (development) / PostgreSQL (production) with optimized indexes
- **AI**: OpenAI GPT-4 for task extraction with rate limiting
- **Authentication**: Google OAuth 2.0 with encrypted token storage
- **Email**: Gmail API with input validation and sanitization
- **Security**: PBKDF2 encryption, XSS protection, CORS configuration, rate limiting
- **Testing**: pytest, coverage reporting, integration tests, unit tests

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Cloud Platform account
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd email-task-manager
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   # Backend (.env)
   cp backend/.env.example backend/.env
   # Edit backend/.env with your credentials
   
   # Frontend (.env)
   cp frontend/.env.example frontend/.env
   # Edit frontend/.env with your API URLs
   ```

5. **Run the Application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python run.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```
   
6. **Initialize Database (First time only)**
   ```bash
   cd backend
   python migrate_db.py  # Adds performance indexes
   ```

## Testing

### Running Tests

The application includes a comprehensive testing suite with over 80% code coverage.

#### Quick Test Run
```bash
cd backend
python run_tests.py
```

#### Specific Test Types
```bash
# Unit tests only
python run_tests.py --type unit

# Integration tests only
python run_tests.py --type integration

# API tests only
python run_tests.py --type api

# Models tests only
python run_tests.py --type models

# Services tests only
python run_tests.py --type services

# Utils tests only
python run_tests.py --type utils
```

#### Specific Test Files
```bash
# Run specific test file
python run_tests.py --file test_models.py

# Run with verbose output
python run_tests.py --verbose
```

#### Coverage Reports
```bash
# Generate coverage report
python run_tests.py --coverage-report

# Run tests without coverage
python run_tests.py --no-coverage
```

#### Manual pytest Commands
```bash
# Run all tests with coverage
pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov

# Run specific test file
pytest tests/test_models.py -v

# Run tests matching pattern
pytest -k "test_user" -v

# Run tests with markers
pytest -m "unit" -v
```

### Test Structure

```
backend/tests/
├── __init__.py              # Test package initialization
├── conftest.py             # Pytest configuration and fixtures
├── test_models.py          # Database model tests
├── test_routes.py          # API route tests
├── test_services.py        # Service layer tests
├── test_utils.py           # Utility function tests
└── test_integration.py     # Integration tests
```

### Test Coverage

The testing suite covers:

- **Models**: Database models, relationships, encryption, validation
- **Routes**: API endpoints, authentication, authorization, error handling
- **Services**: Gmail service, AI service, error handling
- **Utils**: Encryption, validation, rate limiting, sanitization
- **Integration**: Full workflows, error scenarios, performance, security

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **API Tests**: HTTP endpoint testing
- **Security Tests**: Authentication, authorization, input validation
- **Performance Tests**: Large datasets, concurrent requests
- **Error Handling Tests**: Exception scenarios, edge cases

## Configuration

### Google OAuth Setup

1. Create a Google Cloud Project
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Add authorized redirect URIs
5. Download credentials and update `.env`

### OpenAI Setup

1. Get an OpenAI API key
2. Add to backend `.env` file

## Project Structure

```
email-task-manager/
├── backend/                 # Flask API
│   ├── app.py              # Main application
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── routes/             # API endpoints
│   ├── utils/              # Utilities
│   ├── tests/              # Test suite
│   │   ├── conftest.py     # Test configuration
│   │   ├── test_models.py  # Model tests
│   │   ├── test_routes.py  # Route tests
│   │   ├── test_services.py # Service tests
│   │   ├── test_utils.py   # Utility tests
│   │   └── test_integration.py # Integration tests
│   └── run_tests.py        # Test runner
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
│   └── public/             # Static assets
└── docs/                   # Documentation
```

## API Endpoints

### Authentication
- `GET /api/auth/google/authorize` - Initiate Google OAuth flow
- `GET /api/auth/google/callback` - Handle OAuth callback
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh JWT token

### Tasks (with pagination & filtering)
- `GET /api/tasks` - Get user tasks (supports pagination, filtering, sorting)
- `PUT /api/tasks/:id/complete` - Mark task as complete
- `PUT /api/tasks/:id/incomplete` - Mark task as incomplete
- `GET /api/tasks/stats` - Get task statistics
- `GET /api/tasks/categories` - Get available categories
- `GET /api/tasks/priorities` - Get available priorities

### Emails (rate limited)
- `POST /api/emails/process` - Process new emails (5 requests/5min per user)
- `GET /api/emails` - Get processed emails
- `GET /api/emails/:id` - Get specific email
- `GET /api/emails/:id/tasks` - Get tasks for specific email
- `GET /api/emails/stats` - Get email processing statistics

### System
- `GET /api/health` - Health check endpoint
- `GET /api/user/profile` - Get current user profile

## Security Features

### Data Protection
- **Token Encryption**: OAuth tokens encrypted using PBKDF2 + Fernet encryption
- **Input Validation**: All user inputs sanitized and validated to prevent XSS attacks
- **Rate Limiting**: API endpoints protected with configurable rate limits
- **Session Security**: Secure session configuration with httpOnly and SameSite cookies

### Performance Optimizations
- **Database Indexes**: 23 indexes on frequently queried columns for optimal performance
- **Query Optimization**: Aggregated queries reduce database load
- **Pagination**: Task listings paginated to handle large datasets
- **Caching**: Efficient data retrieval with optimized query patterns

## Development & Testing

### Backend Testing
```bash
cd backend
python run_tests.py  # Run all tests
python run_tests.py --type unit  # Run unit tests only
python run_tests.py --coverage-report  # Generate coverage report
```

### Database Management
```bash
cd backend
python migrate_db.py  # Add performance indexes
```

### Code Quality
```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# Check test coverage
coverage report --show-missing
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Run coverage report
7. Submit a pull request

### Testing Requirements

- All new code must have corresponding tests
- Maintain 80%+ code coverage
- Include unit tests for new functions
- Include integration tests for new workflows
- Test error scenarios and edge cases

## License

Internal use only - Company proprietary software
