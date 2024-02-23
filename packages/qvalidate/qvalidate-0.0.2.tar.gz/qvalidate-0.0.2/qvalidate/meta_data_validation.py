import pandas as pd

def Metadata_Structure_Validation(source_df, target_df):
    """
    Metadata and Structure Validation Function
    
    Parameters:
    - source_df: pandas DataFrame representing the source table
    - target_df: pandas DataFrame representing the target table
    
    Returns:
    - validation_result: True if the column names in the target table match those in the source table, False otherwise.
    """
    # Get column names from source and target DataFrames
    source_columns = set(source_df.columns)
    target_columns = set(target_df.columns)
    
    # Perform metadata and structure validation
    if source_columns == target_columns:
        validation_result = True
        print("Metadata and Structure Validation: PASSED")
    else:
        validation_result = False
        print("Metadata and Structure Validation: FAILED")
        # Print columns present in source but not in target
        missing_columns_in_target = source_columns - target_columns
        if missing_columns_in_target:
            print("Columns present in source but not in target:", missing_columns_in_target)
        # Print columns present in target but not in source
        extra_columns_in_target = target_columns - source_columns
        if extra_columns_in_target:
            print("Columns present in target but not in source:", extra_columns_in_target)
    
    return validation_result

# Test Example:
# Assuming you have source_df and target_df representing source and target tables respectively

# Example usage:
# validation_result = Metadata_Structure_Validation(source_df, target_df)
