# Testing Documentation

This document provides comprehensive information about the testing suite for the Email Task Manager application.

## Overview

The testing suite is designed to ensure code quality, reliability, and maintainability. It includes:

- **Unit Tests**: Testing individual components in isolation
- **Integration Tests**: Testing component interactions and workflows
- **API Tests**: Testing HTTP endpoints and responses
- **Security Tests**: Testing authentication, authorization, and input validation
- **Performance Tests**: Testing with large datasets and concurrent requests
- **Error Handling Tests**: Testing exception scenarios and edge cases

## Test Structure

```
backend/tests/
├── __init__.py              # Test package initialization
├── conftest.py             # Pytest configuration and fixtures
├── test_basic.py           # Basic setup verification tests
├── test_models.py          # Database model tests
├── test_routes.py          # API route tests
├── test_services.py        # Service layer tests
├── test_utils.py           # Utility function tests
└── test_integration.py     # Integration tests
```

## Test Categories

### 1. Unit Tests (`test_models.py`, `test_utils.py`)

**Purpose**: Test individual components in isolation

**Coverage**:
- Database models (User, Task, Email)
- Utility functions (encryption, validation, rate limiting)
- Model relationships and methods
- Data validation and sanitization

**Example**:
```python
def test_user_creation(self, db_session):
    """Test creating a new user"""
    user = User(email='test@example.com', name='Test User')
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.email == 'test@example.com'
```

### 2. API Tests (`test_routes.py`)

**Purpose**: Test HTTP endpoints and responses

**Coverage**:
- Authentication endpoints
- Task management endpoints
- Email processing endpoints
- Error handling and status codes
- Request/response validation

**Example**:
```python
def test_get_tasks_authenticated(self, client, auth_headers, sample_task):
    """Test getting tasks for authenticated user"""
    response = client.get('/api/tasks', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tasks' in data
    assert len(data['tasks']) == 1
```

### 3. Service Tests (`test_services.py`)

**Purpose**: Test business logic and external service integrations

**Coverage**:
- Gmail service integration
- AI service integration
- Error handling and retries
- Data processing and transformation

**Example**:
```python
def test_gmail_service_creation(self, sample_user):
    """Test GmailService creation"""
    with patch('services.gmail_service.build') as mock_build:
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        service = GmailService(sample_user)
        assert service.user == sample_user
        assert service.service == mock_service
```

### 4. Integration Tests (`test_integration.py`)

**Purpose**: Test complete workflows and system integration

**Coverage**:
- End-to-end user workflows
- Data flow between components
- Error scenarios and recovery
- Performance with large datasets
- Security and authorization

**Example**:
```python
def test_email_processing_workflow(self, client, auth_headers, sample_user, 
                                 mock_gmail_service, mock_ai_service):
    """Test complete email processing workflow"""
    # Mock services
    mock_gmail_service.return_value.get_unprocessed_emails.return_value = [...]
    mock_ai_service.return_value.extract_tasks.return_value = [...]
    
    # Process emails
    response = client.post('/api/emails/process', headers=auth_headers)
    assert response.status_code == 200
    
    # Verify results
    response = client.get('/api/tasks', headers=auth_headers)
    data = json.loads(response.data)
    assert len(data['tasks']) > 0
```

## Test Fixtures

### Core Fixtures (`conftest.py`)

- **`app`**: Flask application instance for testing
- **`client`**: Test client for making HTTP requests
- **`db_session`**: Database session for each test
- **`sample_user`**: Sample user for testing
- **`sample_email`**: Sample email for testing
- **`sample_task`**: Sample task for testing
- **`auth_headers`**: Authentication headers for protected endpoints

### Mock Fixtures

- **`mock_gmail_service`**: Mock Gmail service
- **`mock_ai_service`**: Mock AI service
- **`mock_google_oauth`**: Mock Google OAuth
- **`mock_openai`**: Mock OpenAI service
- **`mock_rate_limiter`**: Mock rate limiter
- **`mock_encryption`**: Mock encryption utilities

## Running Tests

### Quick Start

```bash
cd backend
python run_tests.py
```

### Specific Test Types

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

### Specific Test Files

```bash
# Run specific test file
python run_tests.py --file test_models.py

# Run with verbose output
python run_tests.py --verbose
```

### Coverage Reports

```bash
# Generate coverage report
python run_tests.py --coverage-report

# Run tests without coverage
python run_tests.py --no-coverage
```

### Manual pytest Commands

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

## Test Coverage

### Current Coverage

The testing suite aims for **80%+ code coverage** across all components:

- **Models**: 95%+ coverage
- **Routes**: 90%+ coverage
- **Services**: 85%+ coverage
- **Utils**: 95%+ coverage
- **Integration**: 80%+ coverage

### Coverage Reports

Coverage reports are generated in multiple formats:

- **Terminal**: `--cov-report=term-missing`
- **HTML**: `--cov-report=html:htmlcov`
- **XML**: `--cov-report=xml`

### Coverage Targets

- **Minimum**: 80% overall coverage
- **Target**: 90% overall coverage
- **Critical Paths**: 100% coverage

## Test Data Management

### Test Database

- Uses SQLite in-memory database for testing
- Each test gets a fresh database session
- Data is automatically cleaned up after each test

### Sample Data

- **`sample_user`**: Test user with Gmail connected
- **`sample_email`**: Test email with subject and body
- **`sample_task`**: Test task with description and priority

### Data Factories

For complex test scenarios, use data factories:

```python
# Create multiple users
users = []
for i in range(10):
    user = User(email=f'user{i}@example.com', name=f'User {i}')
    users.append(user)
db_session.add_all(users)
db_session.commit()
```

## Error Handling Tests

### Common Error Scenarios

1. **Authentication Errors**
   - Invalid tokens
   - Expired tokens
   - Missing authentication

2. **Database Errors**
   - Connection failures
   - Constraint violations
   - Data integrity issues

3. **External Service Errors**
   - Gmail API failures
   - OpenAI API failures
   - Network timeouts

4. **Validation Errors**
   - Invalid input data
   - Missing required fields
   - Data type mismatches

### Error Test Examples

```python
def test_invalid_authentication(self, client):
    """Test handling of invalid authentication"""
    response = client.get('/api/tasks')
    assert response.status_code == 401

def test_database_errors(self, client, auth_headers):
    """Test handling of database errors"""
    response = client.get('/api/tasks/999', headers=auth_headers)
    assert response.status_code == 404
```

## Performance Testing

### Large Dataset Testing

```python
def test_large_dataset_handling(self, client, auth_headers, db_session, sample_user):
    """Test handling of large datasets"""
    # Create many tasks
    tasks = []
    for i in range(100):
        task = Task(user_id=sample_user.id, description=f'Task {i}')
        tasks.append(task)
    db_session.add_all(tasks)
    db_session.commit()
    
    # Test pagination
    response = client.get('/api/tasks?page=1&per_page=50', headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['tasks']) == 50
```

### Concurrent Request Testing

```python
def test_concurrent_requests(self, client, auth_headers):
    """Test handling of concurrent requests"""
    import threading
    
    results = []
    def make_request():
        response = client.get('/api/tasks', headers=auth_headers)
        results.append(response.status_code)
    
    # Create multiple threads
    threads = [threading.Thread(target=make_request) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    # All requests should succeed
    assert all(status == 200 for status in results)
```

## Security Testing

### Authentication Testing

- Token validation
- Session management
- Authorization controls
- Rate limiting

### Input Validation Testing

- XSS prevention
- SQL injection prevention
- Data sanitization
- Length limits

### Example Security Tests

```python
def test_token_encryption(self, db_session, sample_user):
    """Test token encryption security"""
    test_token = "sensitive-access-token-123"
    sample_user.gmail_access_token = test_token
    db_session.commit()
    
    # Verify token is encrypted in database
    db_session.refresh(sample_user)
    assert sample_user._gmail_access_token != test_token
    assert sample_user.gmail_access_token == test_token

def test_input_sanitization(self, client, auth_headers, sample_user, db_session):
    """Test input sanitization"""
    malicious_subject = "<script>alert('xss')</script>Test Subject"
    
    # Create email with malicious content
    email = Email(user_id=sample_user.id, subject=malicious_subject)
    db_session.add(email)
    db_session.commit()
    
    # Verify content is sanitized
    response = client.get('/api/emails', headers=auth_headers)
    data = json.loads(response.data)
    assert '<script>' not in data['emails'][0]['subject']
```

## Continuous Integration

### CI/CD Integration

The testing suite is designed to integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd backend
    python run_tests.py --coverage-report
    coverage report --show-missing
```

### Pre-commit Hooks

Recommended pre-commit hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: python run_tests.py
        language: system
        pass_filenames: false
```

## Best Practices

### Test Writing Guidelines

1. **Test Naming**: Use descriptive test names that explain the scenario
2. **Arrange-Act-Assert**: Structure tests with clear sections
3. **Isolation**: Each test should be independent and not rely on others
4. **Mocking**: Mock external dependencies to avoid side effects
5. **Coverage**: Aim for high coverage but focus on critical paths

### Test Maintenance

1. **Regular Updates**: Update tests when code changes
2. **Refactoring**: Refactor tests to maintain readability
3. **Documentation**: Keep test documentation up to date
4. **Performance**: Monitor test execution time

### Debugging Tests

1. **Verbose Output**: Use `-v` flag for detailed output
2. **Debugging**: Use `pdb` or `ipdb` for debugging
3. **Logging**: Add logging to understand test failures
4. **Isolation**: Run individual tests to isolate issues

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Issues**: Check database configuration
3. **Mock Issues**: Verify mock setup and expectations
4. **Environment Issues**: Check environment variables

### Debugging Commands

```bash
# Run with debug output
pytest -v -s tests/test_models.py

# Run specific test with debugger
pytest -v -s tests/test_models.py::TestUser::test_user_creation

# Check test discovery
pytest --collect-only
```

## Conclusion

This comprehensive testing suite ensures the Email Task Manager application is reliable, secure, and maintainable. Regular testing helps catch issues early and provides confidence in code changes.

For questions or issues with the testing suite, please refer to the project documentation or create an issue in the repository.
