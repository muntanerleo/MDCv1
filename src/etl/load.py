import os
import sys
import pandas as pd
from utils.db_utils import get_postgres_conn, upload_to_postgres

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.model import JobParams


def load_meds_data(params: JobParams):
    conn = get_postgres_conn()
    
    # Read in the data
    Drugs = pd.read_csv(
        '../data/processed/Med_data_1_20240530_drugs.csv', 
        index_col=False)
    
    Generic_Drug_Names = pd.read_csv(
        '../data/processed/Med_data_2_20240530_generic_names.csv', 
        index_col=False)
    
    Use_Case = pd.read_csv(
        '../data/processed/Med_data_3_20240530_use_case.csv', 
        index_col=False)
    
    Drug_Class = pd.read_csv(
        '../data/processed/Med_data_4_20240530_drug_class.csv', 
        index_col=False)
    
    Drug_State = pd.read_csv(
        '../data/processed/Med_data_5_20240530_drug_state.csv', 
        index_col=False)
    
    Side_Effects = pd.read_csv(
        '../data/processed/Med_data_6_20240530_side_effects.csv', 
        index_col=False)
    
    # List of tuples with the dataframes to upload
    table_dataframe_pairs = [
        ('public.drugs', Drugs),
        ('public.generic_drug_names', Generic_Drug_Names),
        ('public.use_case', Use_Case),
        ('public.drug_class', Drug_Class),
        ('public.drug_state', Drug_State),
        ('public.side_effects', Side_Effects)
    ]
    
    # Iterate through the list of tuples and convert- 
    # the 'drug_id' column to string datatype
    for table_name, df in table_dataframe_pairs:
        df['drug_id'] = df['drug_id'].astype(str)
        print(f"Datatype of 'drug_id' column in dataframe '{table_name}': {df['drug_id'].dtype}")
    
    upload_to_postgres(conn, table_dataframe_pairs)


def load_fda_meds(params: JobParams):
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

