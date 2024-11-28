import re
import pandas as pd
from utils.dataframe_utils import _subset_and_save_dataframes


def _preprocess_data(dataframe, file_name, interm_folder):
    try:
        # Changing the column names to what the other source files have them as.
        dataframe.rename(columns={
            'id': 'drug_id', 
            'name': 'drug_name',
            'substitute0': 'generic_name_1', 
            'substitute1': 'generic_name_2', 
            'substitute2': 'generic_name_3', 
            'substitute3': 'generic_name_4', 
            'substitute4': 'generic_name_5',
            'sideEffect0': 'side_effect_1',
            'sideEffect1': 'side_effect_2',
            'sideEffect2': 'side_effect_3',
            'sideEffect3': 'side_effect_4',
            'sideEffect4': 'side_effect_5',
            'use0': 'use_case_1', 
            'use1': 'use_case_2',
            'Chemical Class': 'chemical_class', 
            'Habit Forming': 'habit_forming', 
            'Therapeutic Class': 'therapeutic_class',
            'Action Class': 'action_class'}, inplace=True)
        
        _subset_and_save_dataframes(dataframe, file_name, interm_folder)
    except Exception as e:
        print(f"Error subsetting and saving dataframes: {e}")
        raise e


def extract_generic_names(row):
    """
    Extracts generic names from generic_name columns in a DataFrame row.
    
    Args:
        row (pd.Series): A pandas Series representing a row of a DataFrame.
    
    Returns:
        str: Comma-separated string of generic names extracted from the row.
    
    Example:
        If the row has values 
        'generic_name_1': 'penciclav 500mg/125mg tablet',
        'generic_name_2': 'moxikind-cv 625 tablet', 
        the function will return 'penciclav,moxikind-cv'.
    """
    # Check if all generic_name columns are NaN
    if row.filter(like='generic_name_').isnull().all():
        return None
    
    generic_names = []
    # Iterate through the generic_name columns
    for i in range(1, 6):
        generic_name = row[f'generic_name_{i}']
        # Check if the value is a string
        if isinstance(generic_name, str):
            # Split the string and extract the first word
            generic_names.append(generic_name.split()[0])
    
    # Join the extracted generic names into a comma-separated string
    return ','.join(generic_names)


def extract_administration_method(generic_name):
    """
    This function extracts the administration method from a given generic name.
    
    Parameters:
    generic_name (str): The generic name of a medication.
    
    Returns:
    str: The extracted administration method. If no match is found, returns None.
    
    The function uses a list of common administration methods and a regular expression 
    to match the method in the generic name. The method is considered to be the first 
    word that matches the list.
    """
    
    # Check if the generic_name is a string
    if isinstance(generic_name, str):
        administration_methods = [
            'tablet', 'syrup', 'capsule', 'injection', 
            'suspension', 'iv', 'ointment', 'drop', 'cream', 
            'inhaler', 'kit', 'oral drops', 'nasal spray', 'lotion', 
            'spray', 'eye gel', 'oral gel', 'eye drop', 
            'eye/ear drops', 'dispopen', 'flextouch', 'soap',
            'oral solution', 'shampoo', 'expectorant']
        
        # Create a regex pattern to match any of the administration methods
        pattern = re.compile(r'\b(?:' + '|'.join(administration_methods) + r')\b', flags=re.IGNORECASE)
        
        # Search for the pattern in the generic_name string
        match = re.search(pattern, generic_name)
        
        if match:
            return match.group(0)
        else:
            return generic_name
    else:
        return generic_name


def process_raw_data(file_path, interm_folder, file_name):
    """
    Reads raw data from a CSV file, preprocesses it, and prints a success message upon completion.
    Args:
        file_path (str): file path to the csv file
        file_name (str): the name that the files will have
        interm_folder (str): path to the interm folder
    
    Raises:
        Exception: If there's an error during processing.
    """
    try:
        raw_df = pd.read_csv(file_path)
        
        _preprocess_data(raw_df, file_name, interm_folder)
    except Exception as e:
        print(f"There was an error processing raw data: {e}")
        raise e