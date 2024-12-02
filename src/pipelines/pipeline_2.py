from utils.db_utils import get_postgres_conn, upload_to_postgres
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.model import JobParams


def main(params: JobParams):
    conn = get_postgres_conn()
    
    # Using the params, create a dataframe from the CSV files
    raw_data_dir = os.path.abspath(params.raw_dir)
    
    df_1 = pd.read_csv(os.path.join(raw_data_dir, params.file_name_1))
    df_2 = pd.read_csv(os.path.join(raw_data_dir, params.file_name_2))
    
    # Create a list of tuples with the table name and the dataframe
    table_df_pairs = [
        (params.staging_table_1, df_1),
        (params.staging_table_2, df_2)
    ]
    
    upload_to_postgres(conn, table_df_pairs)


if __name__ == '__main__':
    main(JobParams())