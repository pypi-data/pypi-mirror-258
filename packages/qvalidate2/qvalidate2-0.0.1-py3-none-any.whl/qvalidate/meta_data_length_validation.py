import pandas as pd

def Length_of_Data_Validation(source_df, target_df):
    """
    Length of Data Validation Function
    
    Parameters:
    - source_df: pandas DataFrame representing the source table
    - target_df: pandas DataFrame representing the target table
    
    Returns:
    - validation_result: True if the data sizes of corresponding columns in the target table match those in the source table, False otherwise.
    """
    # Get column names from source and target DataFrames
    source_columns = source_df.columns
    target_columns = target_df.columns
    
    # Perform length of data validation
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
            else:
                # Check if the data size (length) matches
                source_length = source_df[column].apply(lambda x: len(str(x))).max()
                target_length = target_df[column].apply(lambda x: len(str(x))).max()
                if source_length != target_length:
                    print(f"Data size mismatch for column '{column}': Source data size is {source_length}, target data size is {target_length}.")
                    validation_result = False
    
    if validation_result:
        print("Length of Data Validation: PASSED")
    else:
        print("Length of Data Validation: FAILED")
    
    return validation_result

# Test Example:
# Assuming you have source_df and target_df representing source and target tables respectively

# Example usage:
# validation_result = Length_of_Data_Validation(source_df, target_df)
