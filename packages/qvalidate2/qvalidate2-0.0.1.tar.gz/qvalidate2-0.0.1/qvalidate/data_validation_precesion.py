import pandas as pd

def Precision_Check(source_df, target_df, precision_info):
    """
    Precision Check Function
    
    Parameters:
    - source_df: pandas DataFrame representing the source table
    - target_df: pandas DataFrame representing the target table
    - precision_info: Dictionary where keys represent column names or identifiers, and values represent the expected precision for each column
    
    Returns:
    - validation_result: True if the precision of transaction amounts in the target table matches the expected precision, False otherwise.
    """
    validation_result = True
    
    # Iterate over each column and its expected precision
    for column, expected_precision in precision_info.items():
        # Get source column name corresponding to the identifier (if different names are used)
        source_column = next((key for key, value in precision_info.items() if value == expected_precision), None)
        
        # Convert source and target columns to strings to handle NaNs and get precision
        source_precision = source_df[source_column].astype(str).apply(lambda x: len(x.split('.')[-1]) if '.' in x else 0)
        target_precision = target_df[column].astype(str).apply(lambda x: len(x.split('.')[-1]) if '.' in x else 0)
        
        # Check if precision matches the expected precision for the column
        if not (source_precision == expected_precision).all() or not (target_precision == expected_precision).all():
            print(f"Precision Check: FAILED for column '{column}'. Expected precision: {expected_precision}")
            validation_result = False
    
    if validation_result:
        print("Precision Check: PASSED")
    else:
        print("Precision Check: FAILED")
    
    return validation_result

# Example usage:
# Assuming you have source_df and target_df representing source and target tables respectively
# Also, you have a precision_info dictionary defining expected precision for each column

# precision_info = {
#     'source_amount': 3,
#     'target_value': 2,
#     'source_price': 4,
#     'target_balance': 2
# }

# validation_result = Precision_Check(source_df, target_df, precision_info)
