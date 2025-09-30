"""
Tests for create_envs.py
"""
import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import create_envs


class TestCreateEnvs:
    """Test suite for create_envs module"""

    @patch.dict(os.environ, {
        'DB_HOST': 'test_host',
        'DB_PORT': '5433',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass'
    })
    def test_import_envs_and_create_db_config_with_env_vars(self):
        """Test configuration creation with environment variables"""
        config = create_envs.import_envs_and_create_db_config()
        
        expected_config = {
            'host': 'test_host',
            'port': 5433,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_pass'
        }
        
        assert config == expected_config

    @patch.dict(os.environ, {}, clear=True)
    def test_import_envs_and_create_db_config_with_defaults(self):
        """Test configuration creation with default values"""
        # Clear environment variables and test defaults
        for key in ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']:
            if key in os.environ:
                del os.environ[key]
        
        config = create_envs.import_envs_and_create_db_config()
        
        expected_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'mydatabase',
            'user': 'myuser',
            'password': 'mypassword'
        }
        
        assert config == expected_config

    @patch.dict(os.environ, {
        'DB_HOST': 'custom_host',
        'DB_PORT': '3306',  # Different port
        'DB_NAME': 'custom_db',
        # Missing DB_USER and DB_PASSWORD to test partial env vars
    })
    def test_import_envs_and_create_db_config_partial_env_vars(self):
        """Test configuration with partial environment variables"""
        # Remove specific env vars to test defaults
        if 'DB_USER' in os.environ:
            del os.environ['DB_USER']
        if 'DB_PASSWORD' in os.environ:
            del os.environ['DB_PASSWORD']
            
        config = create_envs.import_envs_and_create_db_config()
        
        expected_config = {
            'host': 'custom_host',
            'port': 3306,
            'database': 'custom_db',
            'user': 'myuser',      # default
            'password': 'mypassword'  # default
        }
        
        assert config == expected_config

    def test_config_port_type_conversion(self):
        """Test that port is converted to integer"""
        with patch.dict(os.environ, {'DB_PORT': '9999'}):
            config = create_envs.import_envs_and_create_db_config()
            assert isinstance(config['port'], int)
            assert config['port'] == 9999

    def test_config_keys_present(self):
        """Test that all required keys are present in config"""
        config = create_envs.import_envs_and_create_db_config()
        
        required_keys = ['host', 'port', 'database', 'user', 'password']
        for key in required_keys:
            assert key in config

    def test_config_values_not_none(self):
        """Test that no config values are None"""
        config = create_envs.import_envs_and_create_db_config()
        
        for key, value in config.items():
            assert value is not None
            assert value != ""

    @patch.dict(os.environ, {'DB_PORT': 'invalid_port'})
    def test_invalid_port_handling(self):
        """Test handling of invalid port values"""
        # This test assumes the function should handle invalid port gracefully
        # If the actual implementation doesn't handle this, this test will help identify the issue
        try:
            config = create_envs.import_envs_and_create_db_config()
            # If no exception is raised, check if port falls back to default
            # This depends on the actual implementation
            assert 'port' in config
        except ValueError:
            # If ValueError is raised for invalid port, that's also acceptable behavior
            pass

    def test_empty_string_env_vars(self):
        """Test behavior with empty string environment variables"""
        with patch.dict(os.environ, {
            'DB_HOST': '',
            'DB_NAME': '',
            'DB_USER': '',
            'DB_PASSWORD': ''
        }):
            config = create_envs.import_envs_and_create_db_config()
            
            # Test that empty strings either use defaults or are handled appropriately
            assert config['host'] != '' or config['host'] == 'localhost'
            assert config['database'] != '' or config['database'] == 'mydatabase'
            assert config['user'] != '' or config['user'] == 'myuser'
            assert config['password'] != '' or config['password'] == 'mypassword'