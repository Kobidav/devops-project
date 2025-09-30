"""
Test configuration for pytest
"""
import pytest
import psycopg2
from unittest.mock import patch, MagicMock
import os


@pytest.fixture
def mock_db_config():
    """Mock database configuration for testing"""
    return {
        'host': 'localhost',
        'port': 5432,
        'database': 'testdb',
        'user': 'testuser',
        'password': 'testpass'
    }


@pytest.fixture
def mock_db_connection(mock_db_config):
    """Mock database connection"""
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_cursor.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_conn, mock_cursor


@pytest.fixture
def mock_requests():
    """Mock requests for API calls"""
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ.update({
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'testdb',
        'DB_USER': 'testuser',
        'DB_PASSWORD': 'testpass'
    })
    yield
    # Cleanup if needed