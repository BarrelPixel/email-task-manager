"""
Pytest configuration and fixtures for Email Task Manager tests
"""
import pytest
import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from run import create_app, db
from models.user import User
from models.task import Task
from models.email import Email
from utils.encryption import token_encryption


@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    # Create a temporary file to isolate the database for each test session
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'ENCRYPTION_SALT': 'test-salt'
    })
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        yield app
    
    # Clean up the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Create a fresh database session for each test."""
    with app.app_context():
        # Clear all data
        db.session.remove()
        db.drop_all()
        db.create_all()
        
        yield db.session
        
        # Clean up
        db.session.remove()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        email='test@example.com',
        name='Test User',
        gmail_connected=True,
        gmail_access_token='test-access-token',
        gmail_refresh_token='test-refresh-token',
        gmail_token_expiry=datetime.utcnow() + timedelta(hours=1)
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_email(db_session, sample_user):
    """Create a sample email for testing."""
    email = Email(
        user_id=sample_user.id,
        gmail_id='test-gmail-id-123',
        thread_id='test-thread-id-123',
        subject='Test Email Subject',
        sender='Test Sender',
        sender_email='sender@example.com',
        body='This is a test email body.',
        snippet='Test email snippet',
        received_at=datetime.utcnow(),
        processed=True,
        processed_at=datetime.utcnow()
    )
    db_session.add(email)
    db_session.commit()
    return email


@pytest.fixture
def sample_task(db_session, sample_user, sample_email):
    """Create a sample task for testing."""
    task = Task(
        user_id=sample_user.id,
        email_id=sample_email.id,
        description='Test task description',
        sender='Test Sender',
        priority='Medium',
        category='General',
        completed=False
    )
    db_session.add(task)
    db_session.commit()
    return task


@pytest.fixture
def auth_headers(sample_user):
    """Create authentication headers for testing."""
    from flask_jwt_extended import create_access_token
    
    token = create_access_token(identity=sample_user.id)
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def mock_gmail_service():
    """Mock Gmail service for testing."""
    with patch('services.gmail_service.GmailService') as mock:
        mock_instance = Mock()
        mock_instance.get_unprocessed_emails.return_value = []
        mock.return_value = mock_instance
        yield mock


@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing."""
    with patch('services.ai_service.AIService') as mock:
        mock_instance = Mock()
        mock_instance.extract_tasks.return_value = []
        mock.return_value = mock_instance
        yield mock


@pytest.fixture
def mock_google_oauth():
    """Mock Google OAuth for testing."""
    with patch('google_auth_oauthlib.flow.Flow') as mock_flow:
        with patch('google.oauth2.credentials.Credentials') as mock_creds:
            with patch('googleapiclient.discovery.build') as mock_build:
                # Mock flow
                mock_flow_instance = Mock()
                mock_flow_instance.authorization_url.return_value = ('http://test.com', 'state')
                mock_flow_instance.fetch_token.return_value = None
                mock_flow_instance.credentials = Mock()
                mock_flow_instance.credentials.token = 'test-token'
                mock_flow_instance.credentials.refresh_token = 'test-refresh-token'
                mock_flow_instance.credentials.expiry = datetime.utcnow() + timedelta(hours=1)
                mock_flow.from_client_config.return_value = mock_flow_instance
                
                # Mock credentials
                mock_creds_instance = Mock()
                mock_creds_instance.expired = False
                mock_creds_instance.refresh_token = 'test-refresh-token'
                mock_creds.return_value = mock_creds_instance
                
                # Mock build
                mock_service = Mock()
                mock_userinfo = Mock()
                mock_userinfo.get.return_value.execute.return_value = {
                    'email': 'test@example.com',
                    'name': 'Test User'
                }
                mock_service.userinfo.return_value = mock_userinfo
                mock_build.return_value = mock_service
                
                yield {
                    'flow': mock_flow,
                    'credentials': mock_creds,
                    'build': mock_build
                }


@pytest.fixture
def mock_openai():
    """Mock OpenAI service for testing."""
    with patch('openai.OpenAI') as mock:
        mock_instance = Mock()
        mock_instance.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content='{"tasks": []}'))]
        )
        mock.return_value = mock_instance
        yield mock


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        'gmail_id': 'test-gmail-id-123',
        'thread_id': 'test-thread-id-123',
        'subject': 'Test Email Subject',
        'sender': 'Test Sender',
        'sender_email': 'sender@example.com',
        'body': 'This is a test email body with some actionable items.',
        'snippet': 'Test email snippet',
        'received_at': datetime.utcnow()
    }


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        'description': 'Test task description',
        'priority': 'Medium',
        'category': 'General'
    }


@pytest.fixture
def mock_rate_limiter():
    """Mock rate limiter for testing."""
    with patch('utils.rate_limiter.rate_limiter') as mock:
        mock.is_allowed.return_value = True
        yield mock


@pytest.fixture
def mock_encryption():
    """Mock encryption for testing."""
    with patch('utils.encryption.token_encryption') as mock:
        mock.encrypt_token.return_value = 'encrypted-token'
        mock.decrypt_token.return_value = 'decrypted-token'
        yield mock
