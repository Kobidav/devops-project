"""
Tests for backend_app.py
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import backend_app


class TestBackendApp:
    """Test suite for backend application"""

    def test_ensure_table_exists_success(self, mock_db_connection):
        """Test successful table creation"""
        mock_conn, mock_cursor = mock_db_connection
        
        # Call the function
        backend_app.ensure_table_exists()
        
        # Verify database connection was attempted
        assert mock_conn.cursor.called
        assert mock_cursor.execute.called
        
        # Check that the CREATE TABLE query was executed
        call_args = mock_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS data" in call_args

    def test_ensure_table_exists_connection_error(self):
        """Test table creation with connection error"""
        with patch('psycopg2.connect', side_effect=Exception("Connection failed")):
            with patch('builtins.print') as mock_print:
                backend_app.ensure_table_exists()
                mock_print.assert_called_with("Error connecting to database: Connection failed")

    def test_create_row_success(self, mock_db_connection):
        """Test successful row creation"""
        mock_conn, mock_cursor = mock_db_connection
        test_name = "Test joke"
        test_date = date(2024, 1, 1)
        
        # Call the function
        backend_app.create_row(test_name, test_date)
        
        # Verify the INSERT query was called with correct parameters
        mock_cursor.execute.assert_called_with(
            "INSERT INTO data (name, date) VALUES (%s, %s)",
            (test_name, test_date)
        )

    def test_create_row_connection_error(self):
        """Test row creation with connection error"""
        with patch('psycopg2.connect', side_effect=Exception("Connection failed")):
            with patch('builtins.print') as mock_print:
                backend_app.create_row("test", date.today())
                mock_print.assert_called_with("Error connecting to database: Connection failed")

    def test_fetch_joke_success(self, mock_requests):
        """Test successful joke fetching"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"joke": "Test joke"}
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Call the function
        result = backend_app.fetch_joke()
        
        # Verify the result
        assert result == "Test joke"
        mock_requests.assert_called_once_with(
            "https://geek-jokes.sameerkumar.website/api?format=json",
            timeout=10,
            verify=False
        )

    def test_fetch_joke_api_error(self, mock_requests):
        """Test joke fetching with API error"""
        # Mock API error
        mock_requests.side_effect = Exception("API Error")
        
        # Call the function
        result = backend_app.fetch_joke()
        
        # Verify error handling
        assert "Error fetching joke: API Error" in result

    def test_fetch_joke_empty_response(self, mock_requests):
        """Test joke fetching with empty response"""
        # Mock empty response
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Call the function
        result = backend_app.fetch_joke()
        
        # Verify empty string is returned
        assert result == ""

    @patch('backend_app.time.sleep')
    @patch('backend_app.fetch_joke')
    @patch('backend_app.create_row')
    @patch('backend_app.date')
    def test_main_loop_integration(self, mock_date, mock_create_row, mock_fetch_joke, mock_sleep):
        """Test the main loop integration (run once)"""
        # Setup mocks
        mock_date.today.return_value = date(2024, 1, 1)
        mock_fetch_joke.return_value = "Test joke"
        
        # Mock the while loop to run only once
        with patch('builtins.__import__') as mock_import:
            original_import = __import__
            
            def side_effect(name, *args, **kwargs):
                if name == 'backend_app' and hasattr(backend_app, '_test_run_once'):
                    # Exit after one iteration for testing
                    raise KeyboardInterrupt()
                return original_import(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            # Set test flag and run
            backend_app._test_run_once = True
            try:
                # This would normally run forever, but we'll catch the KeyboardInterrupt
                exec(compile(open('backend_app.py').read(), 'backend_app.py', 'exec'))
            except (KeyboardInterrupt, SystemExit):
                pass
            
            # Clean up test flag
            delattr(backend_app, '_test_run_once')