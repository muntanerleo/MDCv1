from psycopg2 import OperationalError
from dotenv import load_dotenv
from loguru import logger
import psycopg2
import os

load_dotenv()


def get_postgres_conn():
    """
    Establishes a connection to a PostgreSQL database using credentials from environment variables.
    
    Returns:
        connection (psycopg2.extensions.connection or None): A connection object to the PostgreSQL database 
        if the connection is successful, otherwise None.
    """
    connection = None
    
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME")
        )
        logger.info("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    
    return connection


def upload_to_postgres(conn, table_df_pairs):
    """
    Uploads a DataFrame to a PostgreSQL table using psycopg2.
    
    Args:
    - conn: database connection object
    - table_df_pairs: list of tuples where each tuple contains the table name and the DataFrame to upload
    
    Returns:
    None
    """
    
    try:
        for table_name, df in table_df_pairs:
            with conn.cursor() as cursor:
                # Convert each row of the DataFrame to a tuple and store in a list
                values = [tuple(row) for row in df.to_numpy()]
                
                # Join the DataFrame column names into a single string separated by commas
                columns = ','.join(list(df.columns))
                
                # Create a string of placeholders for SQL query, one for each column
                placeholders = ','.join(['%s'] * len(df.columns))
                
                # Formulate the SQL query for inserting data into the specified table
                sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Execute the SQL query with the list of values
                cursor.executemany(sql_query, values)
            
            conn.commit()
            logger.info(f"Data uploaded to {table_name} in PostgreSQL.")
    except OperationalError as e:
        logger.error(f"Error uploading data to PostgreSQL: {e}")
    finally:
        conn.close()