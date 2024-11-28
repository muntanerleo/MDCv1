'''
Transforming column string values

The following dataframe columns will be transformed using regular expressions:
    Strip leading and trailing whitespace: (r'^\s+|\s+$', '')
    Replace any sequence of whitespace characters with a single space: (r'\s+', ' ')
    Remove spaces between numbers and 'mg': (r'(\d+(\.\d+)?)\s*mg', r'\1mg)
    Convert all letters to lowercase: (r'([a-zA-Z]+)', lambda x: x.group(0).lower())
    Remove whitespace around slashes: (r'\s*([/])\s*', r'\1')
    Remove whitespace around hyphens: (r'\s*-\s*', '-')
    Replace '&' with 'and': (r'&', 'and')
    Remove '\r\n': (r'\r\n', '')
    Replace '{' with '(': (r'\{', '(')
    Replace '}' with ')': (r'\}', ')')
    Replace any instance of '{}' with '()': (r'\{.*?\}', '()')
'''


# Define transformations for each DataFrame
transformations_1 = {
    'drug_name': [
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
    ]
}


transformations_2 = {
    'generic_name_1': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_2': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_3': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_4': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_5': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
}


transformations_3 = {
    'use_case_1': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
    ],
    'use_case_2': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
    ],
}


transformations_4 = {
    'chemical_class': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'&', 'and'),
        (r'\r\n', ''),
        (r'\{', '('),
        (r'\}', ')'),
        (r'\{.*?\}', '()'),
        (r'\s*-\s*', '-'),
        (r'\s*([/])\s*', r'\1'),
    ],
    'therapeutic_class': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\r\n', ''),
        (r'\s*-\s*', '-'),
        (r'\s*([/])\s*', r'\1'),
    ],
    'action_class': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'&', 'and'),
        (r'\r\n', ''),
        (r'\{', '('),
        (r'\}', ')'),
        (r'\{.*?\}', '()'),
        (r'\s*-\s*', '-'),
        (r'\s*([/])\s*', r'\1'),
    ]
}


transformations_5 = {
    'use_case_1': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'&', 'and'),
        (r'\r\n', ''),
        (r'\{', '('),
        (r'\}', ')'),
        (r'\{.*?\}', '()'),
        (r'\s*-\s*', '-'),
        (r'\s*([/])\s*', r'\1'),
    ],
    'generic_name_1': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_2': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_3': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_4': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'generic_name_5': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'(\d+(\.\d+)?)\s*mg', r'\1mg'),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
    ],
    'therapeutic_class': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\r\n', ''),
        (r'\s*-\s*', '-'),
        (r'\s*([/])\s*', r'\1'),
    ],
}


transformations_6 = {
    'side_effect_1': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
        (r'&', 'and'),
        (r'\r\n', ''),
    ],
    'side_effect_2': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
        (r'&', 'and'),
        (r'\r\n', ''),
    ],
    'side_effect_3': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
        (r'&', 'and'),
        (r'\r\n', ''),
    ],
    'side_effect_4': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
        (r'&', 'and'),
        (r'\r\n', ''),
    ],
    'side_effect_5': [
        (r'([a-zA-Z]+)', lambda x: x.group(0).lower()),
        (r'^\s+|\s+$', ''),
        (r'\s+', ' '),
        (r'\s*([/])\s*', r'\1'),
        (r'\s*-\s*', '-'),
        (r'&', 'and'),
        (r'\r\n', ''),
    ],
}


def change_column_names(dataframe, cols):
    dataframe.rename(cols, inplace=True)
    return dataframe


def normalize_strings(df, transformations):
    """
    Function to normalize strings in specified columns of a DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the columns to be normalized.
        transformations (dict): Dictionary where keys are column names and values are lists of regular expressions to apply to each respective column.
    
    Returns:
        pandas.DataFrame: DataFrame with normalized strings in specified columns.
    """
    # Apply transformations to each specified column
    for column, regex_list in transformations.items():
        if column in df.columns:
            for regex in regex_list:
                df[column] = df[column].str.replace(regex[0], regex[1], regex=True)
    
    return df