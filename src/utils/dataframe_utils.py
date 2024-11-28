import os
import pandas as pd
from datetime import datetime


def _create_dataframe_subset(dataframe, columns):
    subset = dataframe[columns]
    return subset


def _save_dataframe(dataframe, file_name, idx, subset_name, interm_folder):
    csv_file_name = f'{file_name}_{idx}_{subset_name}.csv'
    csv_file_path = os.path.join(interm_folder, csv_file_name)
    
    dataframe.to_csv(csv_file_path, index=False)


def _subset_and_save_dataframes(dataframe, file_name, interm_folder):
    try:
        # Now that the dataframe is mostly cleaned, I will make the table dataframes-
        # by subsetting med_df
        
        # Define the subsets and their columns
        subsets = {
            'drugs': ['drug_id', 'drug_name', 'habit_forming'],
            'generic_names': ['drug_id', 'generic_name_1', 'generic_name_2', 'generic_name_3', 'generic_name_4', 'generic_name_5'],
            'side_effects': ['drug_id', 'side_effect_1', 'side_effect_2', 'side_effect_3', 'side_effect_4', 'side_effect_5'],
            'use_case': ['drug_id', 'use_case_1', 'use_case_2'],
            'drug_class': ['drug_id', 'chemical_class', 'therapeutic_class', 'action_class'],
            'drug_state': ['drug_id', 'use_case_1', 'generic_name_1', 'generic_name_2', 'generic_name_3', 'generic_name_4', 
                            'generic_name_5', 'therapeutic_class']
        }
        
        # Loop through the dataframes list and save them 
        for idx, (subset_name, columns) in enumerate(subsets.items(), start=1):
            subset = _create_dataframe_subset(dataframe, columns)
            _save_dataframe(subset, file_name, idx, subset_name, interm_folder)
        
        print("Raw data processed and dataframes saved into interm folder.")
    except Exception as e:
        print(f"Error subsetting and saving dataframes: {e}")
        raise e


def _save_processed_dataframes(dataframes_with_labels, file_name, processed_folder):
    """
    Saves processed dataframes to CSV files in the 'processed' folder.
    
    Args:
        dataframes_with_labels (list of tuples): List of tuples containing dataframe-label pairs to be saved.
        file_name (str): Base name for the CSV files.
        processed_folder (str): processed folder to store the csv files
        
    Raises:
        Exception: If there's an error during saving.
    """
    try: 
        timestamp = datetime.now().strftime("%Y%m%d")
        
        # Loop through the dataframes list and save them 
        for idx, (df, label) in enumerate(dataframes_with_labels, start=1):
            csv_file_name = f'{file_name}_{idx}_{timestamp}'
            
            # Add the label to the CSV file name
            if label:
                csv_file_name += f'_{label}'
            
            csv_file_name += '.csv'
            
            csv_file_path = os.path.join(processed_folder, csv_file_name)
            df.to_csv(csv_file_path, index=False)
        
        print("Dataframes saved into processed folder successfully.")
    except Exception as e:
        print(f"Error saving dataframes: {e}")
        raise e


def get_interm_dataframes(interm_folder, recursive=False, file_filter=None):
    """
    Iterates through a directory, reads CSV files, and stores them in a dictionary of DataFrames.
    
    Args:
    - interm_folder: The path to the directory containing CSV files.
    - recursive: Boolean indicating whether to search recursively in subdirectories.
    - file_filter: A function to filter files based on custom criteria.
    
    Returns:
    - A dictionary where keys are file names and values are corresponding DataFrames.
    """
    try:
        # Initialize an empty dictionary to store DataFrames
        dataframes_dict = {}
        
        # Walk through the directory tree if recursive is set to True
        for root, dirs, files in os.walk(interm_folder):
            for filename in files:
                # Check if the file is a CSV file
                if filename.endswith('.csv'):
                    # Construct the full path to the CSV file
                    file_path = os.path.join(root, filename)
                    try:
                        # Read the CSV file into a DataFrame
                        if file_filter is None or file_filter(file_path):
                            df = pd.read_csv(file_path)
                            
                            # Store the DataFrame in the dictionary with the file name as the key
                            dataframes_dict[filename] = df
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
        
        return dataframes_dict
    except Exception as e:
        print(f"Error storing csv files into dataframes: {e}")
        raise e