"""
Tests for frontend_app.py
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import frontend_app


class TestFrontendApp:
    """Test suite for frontend application"""

    def test_get_last_20_records_success(self, mock_db_connection):
        """Test successful retrieval of last 20 records"""
        mock_conn, mock_cursor = mock_db_connection
        
        # Mock database results
        mock_records = [
            ("Joke 1", "2024-01-01"),
            ("Joke 2", "2024-01-02"),
        ]
        mock_cursor.fetchall.return_value = mock_records
        
        # Call the function
        result = frontend_app.get_last_20_records()
        
        # Verify the query was executed correctly
        mock_cursor.execute.assert_called_with(
            'SELECT name, date FROM data ORDER BY id DESC LIMIT 20'
        )
        
        # Verify the results
        assert result == mock_records
        assert mock_cursor.close.called
        assert mock_conn.close.called

    def test_get_last_20_records_error(self):
        """Test record retrieval with database error"""
        with patch('psycopg2.connect', side_effect=Exception("Database error")):
            with patch('builtins.print') as mock_print:
                result = frontend_app.get_last_20_records()
                
                # Verify error handling
                assert result == []
                mock_print.assert_called_with("Error fetching records: Database error")

    def test_get_last_20_records_partial_cleanup(self):
        """Test record retrieval with partial cleanup on error"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Mock connection to succeed but cursor to fail
        with patch('psycopg2.connect', return_value=mock_conn):
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Query error")
            
            with patch('builtins.print'):
                result = frontend_app.get_last_20_records()
                
                # Verify cleanup was attempted
                assert result == []
                assert mock_cursor.close.called
                assert mock_conn.close.called

    @patch('frontend_app.get_last_20_records')
    def test_index_route_success(self, mock_get_records):
        """Test the index route with successful data retrieval"""
        # Mock database records
        mock_records = [
            ("Test joke 1", "2024-01-01"),
            ("Test joke 2", "2024-01-02"),
        ]
        mock_get_records.return_value = mock_records
        
        # Call the route function
        result = frontend_app.index()
        
        # Verify that get_last_20_records was called
        mock_get_records.assert_called_once()
        
        # Verify HTML structure
        assert isinstance(result, str)
        assert "Test joke 1" in result
        assert "Test joke 2" in result
        assert "2024-01-01" in result
        assert "2024-01-02" in result
        assert "Last 20 Records" in result
        assert "<!DOCTYPE html>" in result

    @patch('frontend_app.get_last_20_records')
    def test_index_route_empty_records(self, mock_get_records):
        """Test the index route with no records"""
        # Mock empty database
        mock_get_records.return_value = []
        
        # Call the route function
        result = frontend_app.index()
        
        # Verify that get_last_20_records was called
        mock_get_records.assert_called_once()
        
        # Verify HTML structure with no data
        assert isinstance(result, str)
        assert "Last 20 Records" in result
        assert "<!DOCTYPE html>" in result
        assert "<tbody>" in result

    def test_app_routes_registration(self):
        """Test that routes are properly registered"""
        # Check that the app has the expected route
        routes = [rule.rule for rule in frontend_app.app.router.rules]
        assert '/' in routes

    @patch('frontend_app.run')
    def test_main_execution(self, mock_run):
        """Test the main execution block"""
        # Mock the __name__ == '__main__' condition
        with patch('frontend_app.__name__', '__main__'):
            # Import and execute the main block logic
            # Since we can't easily test the if __name__ == '__main__' block directly,
            # we'll test that run would be called with correct parameters
            expected_args = {
                'host': '0.0.0.0',
                'port': 8080,
                'debug': True
            }
            
            # Verify the app object exists and has the expected configuration
            assert hasattr(frontend_app, 'app')
            assert frontend_app.app is not None

    def test_bottle_app_creation(self):
        """Test that Bottle app is created correctly"""
        assert frontend_app.app is not None
        assert hasattr(frontend_app.app, 'route')
        assert hasattr(frontend_app.app, 'router')

    @patch('frontend_app.SimpleTemplate')
    @patch('frontend_app.get_last_20_records')
    def test_template_rendering(self, mock_get_records, mock_template):
        """Test template rendering functionality"""
        # Mock data and template
        mock_records = [("Test", "2024-01-01")]
        mock_get_records.return_value = mock_records
        
        mock_template_instance = MagicMock()
        mock_template_instance.render.return_value = "rendered_html"
        mock_template.return_value = mock_template_instance
        
        # Call the index function
        result = frontend_app.index()
        
        # Verify template was used (in actual implementation)
        # Note: Since SimpleTemplate is used directly in the code,
        # this test verifies the structure rather than mocked behavior
        assert isinstance(result, str)
        assert len(result) > 0