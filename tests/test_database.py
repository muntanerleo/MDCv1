import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import OperationalError

from your_module import DatabaseConnection  # Replace with the actual import path

class TestDatabaseConnection:
    @patch.dict(os.environ, {
        'DB_HOST': 'test-host',
        'DB_NAME': 'test-db',
        'DB_USER': 'test-user',
        'DB_PASSWORD': 'test-password',
        'DB_PORT': '5432'
    })
    def test_init_successful_connection(self):
        """
        Test successful initialization of DatabaseConnection
        """
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine
            
            db_conn = DatabaseConnection()
            
            assert hasattr(db_conn, 'engine')
            mock_create_engine.assert_called_once()
    
    @patch.dict(os.environ, {
        'DB_HOST': 'test-host',
        'DB_NAME': 'test-db',
        'DB_USER': 'test-user'
    })
    def test_missing_database_parameters(self):
        """
        Test that a ValueError is raised when required parameters are missing
        """
        with pytest.raises(ValueError, match="Missing required database parameter: password"):
            DatabaseConnection()
    
    @patch.dict(os.environ, {
        'DB_HOST': 'test-host',
        'DB_NAME': 'test-db',
        'DB_USER': 'test-user',
        'DB_PASSWORD': 'test-password',
        'DB_PORT': '5432'
    })
    def test_database_connection_error(self):
        """
        Test handling of database connection errors
        """
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            # Simulate connection error
            mock_create_engine.side_effect = OperationalError("Connection failed", None, None)
            
            with pytest.raises(RuntimeError, match="Database connection error"):
                DatabaseConnection()
    
    @patch.dict(os.environ, {
        'DB_HOST': 'test-host',
        'DB_NAME': 'test-db',
        'DB_USER': 'test-user',
        'DB_PASSWORD': 'test-password',
        'DB_PORT': '5432'
    })
    def test_load_medications_data_successful(self):
        """
        Test successful loading of medications data
        """
        # Create a mock DataFrame to simulate query result
        mock_df = pd.DataFrame({
            'drug_id': [1, 2],
            'drug_name': ['Aspirin', 'Ibuprofen'],
            'description': ['Pain reliever', 'Anti-inflammatory']
        })
        
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            with patch('pandas.read_sql') as mock_read_sql:
                # Setup mocks
                mock_engine = MagicMock()
                mock_create_engine.return_value = mock_engine
                mock_read_sql.return_value = mock_df
                
                # Create DatabaseConnection instance
                db_conn = DatabaseConnection()
                
                # Call load_medications_data
                result = db_conn.load_medications_data()
                
                # Assertions
                mock_read_sql.assert_called_once_with(
                    "SELECT * \nFROM public.drug_details_1", 
                    db_conn.engine
                )
                pd.testing.assert_frame_equal(result, mock_df)
    
    @patch.dict(os.environ, {
        'DB_HOST': 'test-host',
        'DB_NAME': 'test-db',
        'DB_USER': 'test-user',
        'DB_PASSWORD': 'test-password',
        'DB_PORT': '5432'
    })
    def test_load_medications_data_error(self):
        """
        Test error handling when loading medications data fails
        """
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            with patch('pandas.read_sql') as mock_read_sql:
                # Setup mocks
                mock_engine = MagicMock()
                mock_create_engine.return_value = mock_engine
                mock_read_sql.side_effect = Exception("Query execution failed")
                
                # Create DatabaseConnection instance
                db_conn = DatabaseConnection()
                
                # Expect RuntimeError when loading medications data
                with pytest.raises(RuntimeError, match="Error loading medication data"):
                    db_conn.load_medications_data()
    
    def test_engine_disposal(self):
        """
        Test that the database engine is properly disposed of
        """
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine
            
            # Create and immediately delete the DatabaseConnection instance
            db_conn = DatabaseConnection()
            del db_conn
            
            # Verify engine disposal
            mock_engine.dispose.assert_called_once()

# Pytest configuration to ensure proper environment setup
def pytest_configure(config):
    """
    Pytest configuration to load environment variables for tests
    """
    import dotenv
    dotenv.load_dotenv()
