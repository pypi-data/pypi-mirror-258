import pandas as pd

def Data_Type_Validation(source_df, target_df):
    """
    Data Type Validation Function
    
    Parameters:
    - source_df: pandas DataFrame representing the source table
    - target_df: pandas DataFrame representing the target table
    
    Returns:
    - validation_result: True if the data types of corresponding columns in the target table match those in the source table, False otherwise.
    """
    # Get column names from source and target DataFrames
    source_columns = source_df.columns
    target_columns = target_df.columns
    
    # Perform data type validation
    validation_result = True
    for column in source_columns:
        # Check if the column exists in the target DataFrame
        if column not in target_columns:
            print(f"Column '{column}' present in source but not in target table.")
            validation_result = False
        else:
            # Check if the data types match
            source_dtype = str(source_df[column].dtype)
            target_dtype = str(target_df[column].dtype)
            if source_dtype != target_dtype:
                print(f"Data type mismatch for column '{column}': Source data type is {source_dtype}, target data type is {target_dtype}.")
                validation_result = False
    
    if validation_result:
        print("Data Type Validation: PASSED")
    else:
        print("Data Type Validation: FAILED")
    
    return validation_result

# Test Example:
# Assuming you have source_df and target_df representing source and target tables respectively

# Example usage:
# validation_result = Data_Type_Validation(source_df, target_df)
