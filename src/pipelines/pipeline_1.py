


def pipeline_alpha(file_path, interm_folder, file_name):
    """
    Executes the data processing pipeline and returns the processed dataframes.
    
    Args:
        file_path (str): The path to the raw data file.
        interm_folder (str): The folder where intermediate files are stored.
        file_name (str): The name of the raw data file.
        list: List of tuples containing processed dataframes and their labels.
    
    Returns:
        list: List of processed dataframes.
    
    Raises:
        Exception: If there's an error during execution.
    """
    try:
        process_raw_data(file_path, interm_folder, file_name)
        
        # Call the function to get CSV files and store them in a dictionary
        dataframes_dict = get_interm_dataframes(interm_folder)
        
        # Extract DataFrames from the dictionary and set them as individual variables
        dfs = {}  # Dictionary to store the DataFrames
        for file_names, df in dataframes_dict.items():
            dfs[file_names] = df
        
        drugs = dfs['Med_data_1_drugs.csv']
        generic_names = dfs['Med_data_2_generic_names.csv']
        side_effects = dfs['Med_data_3_side_effects.csv']
        use_case = dfs['Med_data_4_use_case.csv']
        drug_class = dfs['Med_data_5_drug_class.csv']
        drug_state = dfs['Med_data_6_drug_state.csv']
        
        # Apply the normalization function to the dataframe columns
        df1_normalized = normalize_strings(drugs, transformations_1)
        df2_normalized = normalize_strings(generic_names, transformations_2)
        
        # Drop rows where Drug_ID has a value, but all other columns are NaN
        df2_normalized = df2_normalized.dropna(subset=[
            'generic_name_1', 
            'generic_name_2', 
            'generic_name_3', 
            'generic_name_4', 
            'generic_name_5'], how='all')
        df2_normalized = df2_normalized.reset_index(drop=True)
        
        df3_normalized = normalize_strings(use_case, transformations_3)
        df4_normalized = normalize_strings(drug_class, transformations_4)
        df5_normalized = normalize_strings(drug_state, transformations_5)
        
        # Create the new column 'generic_profile'
        df5_normalized['generic_profile'] = df5_normalized.apply(extract_generic_names, axis=1)
        
        # Apply the function to the generic_name_1 column
        df5_normalized['administration_method'] = df5_normalized['generic_name_1'].apply(extract_administration_method)
        
        # Drop the generic_name columns
        columns_to_drop = ['generic_name_1', 'generic_name_2', 
                        'generic_name_3', 'generic_name_4', 'generic_name_5']
        
        df5_normalized.drop(columns=columns_to_drop, inplace=True)
        df5_normalized.reset_index(drop=True, inplace=True)
        
        cols = {
            'use_case_1': 'case_definition',
            'therapeutic_class': 'therapeutic_type'
            }
        df5_normalized.rename(columns=cols, inplace=True)
        
        # Re-order the columns
        df5_normalized = df5_normalized[['drug_id', 'case_definition', 'therapeutic_type', 'administration_method', 'generic_profile']]
        
        df6_normalized = normalize_strings(side_effects, transformations_6)
        
        # Save list of tuples containing dataframe-label pairs
        dataframes_with_labels = [
            (df1_normalized, 'drugs'),
            (df2_normalized, 'generic_names'),
            (df3_normalized, 'use_case'),
            (df4_normalized, 'drug_class'),
            (df5_normalized, 'drug_state'),
            (df6_normalized, 'side_effects')
        ]
        
        return dataframes_with_labels
    except Exception as e:
        print(f"There was an error executing pipeline_alpha: {e}")
        raise e

def main():
    try:
        interm_folder = '../data/interm'
        processed_folder = '../data/processed'
        file_path = '../data/raw/medicine_dataset.csv'
        file_name = 'Med_data'
        
        dataframes_with_labels = pipeline_alpha(file_path, interm_folder, file_name)
        
        _save_processed_dataframes(dataframes_with_labels, file_name, processed_folder)
    except Exception as e:
        print(f"There was an error executing the main function: {e}")
        raise e

if __name__ == "__main__":
    main()