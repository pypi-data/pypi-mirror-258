import pandas as pd

def validate_numeric_data(source_df, target_df, format_info_json):
    """
    Validates numeric data between source and target DataFrames based on format information.

    Args:
        source_df: pandas DataFrame containing source data.
        target_df: pandas DataFrame containing target data.
        format_info_json: JSON object containing format specifications.

    Returns:
        dict: Validation results indicating which columns failed validation and the reasons.
    """

    source_format = format_info_json.get('source_format', {})
    target_format = format_info_json.get('target_format', {})

    validation_results = {'source_failures': {}, 'target_failures': {}}

    # Define a function to validate numeric values
    def validate_numeric_value(value, data_format):
        try:
            numeric_value = float(value)
            num_digits = len(str(int(numeric_value)))
            decimal_part = str(numeric_value).split('.')[1] if '.' in str(numeric_value) else ''
            decimal_places = len(decimal_part) if decimal_part else 0

            if num_digits != data_format['num_digits']:
                return False, f"Number of digits does not match {data_format['num_digits']}"

            if decimal_places != data_format['decimal_places']:
                return False, f"Number of decimal places does not match {data_format['decimal_places']}"

            if data_format['decimal_separator'] != '.' and '.' in str(numeric_value):
                return False, f"Decimal separator does not match '{data_format['decimal_separator']}'"

            return True, None
        except ValueError:
            return False, "Value is not a valid number"

    # Validate source data
    for column in source_df.columns:
        if source_df[column].dtype in ['int64', 'float64']:
            validation, reason = validate_numeric_value(source_df[column].iloc[0], source_format)
            if not validation:
                validation_results['source_failures'][column] = reason

    # Validate target data
    for column in target_df.columns:
        if target_df[column].dtype in ['int64', 'float64']:
            validation, reason = validate_numeric_value(target_df[column].iloc[0], target_format)
            if not validation:
                validation_results['target_failures'][column] = reason

    return validation_results
