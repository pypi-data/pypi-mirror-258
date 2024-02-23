import pandas as pd

def Precision_Check(source_df, target_df, precision_info):
    """
    Precision Check Function
    
    Parameters:
    - source_df: pandas DataFrame representing the source table
    - target_df: pandas DataFrame representing the target table
    - precision_info: Dictionary where keys represent column names, and values represent the expected precision for each column
    
    Returns:
    - validation_result: True if the precision of values in the target table matches the expected precision, False otherwise.
    """
    validation_result = True
    
    # Check column existence and data types
    for column, expected_precision in precision_info.items():
        if column not in source_df.columns:
            print(f"Column '{column}' not found in the source DataFrame.")
            validation_result = False
        elif column not in target_df.columns:
            print(f"Column '{column}' not found in the target DataFrame.")
            validation_result = False
        elif source_df[column].dtype != target_df[column].dtype:
            print(f"Data type mismatch for column '{column}': Source data type is {source_df[column].dtype}, target data type is {target_df[column].dtype}.")
            validation_result = False
        else:
            # Convert source and target columns to strings to handle NaNs and get precision
            source_precision = source_df[column].apply(lambda x: len(str(x).split('.')[-1]) if '.' in str(x) else 0)
            target_precision = target_df[column].apply(lambda x: len(str(x).split('.')[-1]) if '.' in str(x) else 0)
            
            # Check if precision matches the expected precision for the column
            if not (source_precision == expected_precision).all() or not (target_precision == expected_precision).all():
                print(f"Precision Check: FAILED for column '{column}'. Expected precision: {expected_precision}")
                validation_result = False
    
    if validation_result:
        print("Precision Check: PASSED")
    else:
        print("Precision Check: FAILED")
    
    return validation_result
