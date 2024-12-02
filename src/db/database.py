from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import pandas as pd
from dotenv import load_dotenv
import os

class DatabaseConnection:
    """
    Manages database connection and data retrieval
    """
    def __init__(self):
        """
        Initialize database connection
        """
        # Load environment variables
        load_dotenv()
        
        # Create database connection
        self.engine = self._create_db_connection()
    
    def _create_db_connection(self) -> Engine:
        """
        Create a database connection using environment variables
        
        Returns:
            sqlalchemy.engine.base.Engine: Database connection engine
        """
        # Construct connection string from environment variables
        db_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        # Validate required connection parameters
        required_params = ['database', 'user', 'password']
        for param in required_params:
            if not db_params[param]:
                raise ValueError(f"Missing required database parameter: {param}")
        
        # Construct SQLAlchemy connection string
        connection_string = (
            f"postgresql://{db_params['user']}:{db_params['password']}@"
            f"{db_params['host']}:{db_params['port']}/{db_params['database']}"
        )
        
        try:
            # Create SQLAlchemy engine
            return create_engine(connection_string)
        except Exception as e:
            raise RuntimeError(f"Database connection error: {e}")
    
    def load_drug_details(self, table_name: str) -> pd.DataFrame:
        """
        Load medication data from PostgreSQL database
        
        Returns:
            pd.DataFrame: Medication data
        """
        query = f"SELECT * FROM public.{table_name}"
        
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            raise RuntimeError(f"Error loading medication data from {table_name}: {e}")
    
    def __del__(self):
        """
        Dispose of database engine
        """
        if hasattr(self, 'engine'):
            self.engine.dispose()