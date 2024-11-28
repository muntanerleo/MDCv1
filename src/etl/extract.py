from loguru import logger
import pandas as pd
import httpx
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.model import JobParams
from datetime import datetime


def get_api_data(params):
    try:
        response_1 = httpx.get(params.endpoint_1)
        response_2 = httpx.get(params.endpoint_2)
        
        # Print the status code of the response
        logger.info(f"Status code for first response: {response_1.status_code}")
        logger.info(f"Status code for second ressponse: {response_2.status_code}")
        
        # Save the response body to a variable
        data_eff_time = response_1.json()
        data_finished = response_2.json()
        
        # Converting the first result to a dataframe
        df_1 = pd.DataFrame(data_eff_time['results'])
        df_2 = pd.DataFrame(data_finished['results'])
        
        # Doing some simple data cleaning
        df_1.drop(columns='references', inplace=True)
        df_2['finished'] = df_2['finished'].astype(str)
        
        # Save the dataframe to a CSV file with a timestamp
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        raw_data_dir = os.path.abspath(params.raw_dir)
        
        file_name_1 = f"{params.file_name_1.split('.')[0]}_{timestamp}.csv"
        file_name_2 = f"{params.file_name_2.split('.')[0]}_{timestamp}.csv"
        
        df_1.to_csv(os.path.join(raw_data_dir, file_name_1), index=False)
        df_2.to_csv(os.path.join(raw_data_dir, file_name_2), index=False)
        
        logger.info("Data successfully saved in the raw folder")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e


def main(params: JobParams):
    get_api_data(params)


if __name__ == '__main__':
    main(JobParams())