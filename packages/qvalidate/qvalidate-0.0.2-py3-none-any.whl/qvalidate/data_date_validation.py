import pandas as pd

def Date_Format_Validation(source_df, target_df, allowed_formats):
    """
    Date Format Validation Function
    
    Parameters:
    - source_df: pandas DataFrame representing the source dataset
    - target_df: pandas DataFrame representing the target dataset
    - allowed_formats: List of strings representing the allowed date formats (e.g., ['YYYY-MM-DD', 'YYYY/MM/DD'])
    
    Returns:
    - validation_result: True if the date formats in the target dataset match any of the allowed formats, False otherwise.
    """
    # Validate date formats
    for format in allowed_formats:
        formatted_target_dates = pd.to_datetime(target_df, errors='coerce').dt.strftime(format)
        if formatted_target_dates.equals(target_df):
            print(f"Date Format Validation: PASSED. Target date format is {format}")
            return True
    
    print("Date Format Validation: FAILED")
    return False

# Example usage:
# Assuming you have source_df and target_df representing source and target datasets respectively
# Also, you have a list of allowed date formats, for example: ['YYYY-MM-DD', 'YYYY/MM/DD']

# validation_result = Date_Format_Validation(source_df, target_df, ['YYYY-MM-DD', 'YYYY/MM/DD'])
