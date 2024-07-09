import numpy as np
import pandas as pd


def convert_to_float32(obj):
    """
    Recursively converts all numerical values in a dictionary or 
    a list to float32. If `obj` is neither a dictionary nor a list, 
    it directly attempts to convert `obj` to float32.

    Parameters:
    obj (dict or list): The dictionary, list, or numerical value to convert.

    Returns:
    The converted object with all numerical values as float32.
    """
    
    
    if isinstance(obj, dict):
        # If the object is a dictionary, recursively apply to all its values.
        return {k: convert_to_float32(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If the object is a list, recursively apply to all its elements.
        return [convert_to_float32(elem) for elem in obj]
    else:
        # Attempt to convert to float32 if it's a numerical value.
        try:
            return np.float32(obj)
        except:
            # Return the object as-is if it cannot be converted.
            return obj
    

def convert_dict_to_list(obj):
    """
    Recursively converts numpy arrays and pandas Series in the dictionary
    to lists. It handles nested dictionaries and lists as well.
    """
    if isinstance(obj, dict):
        return {k: convert_dict_to_list(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dict_to_list(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        # Convert the numpy array to a list
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        # Convert the pandas Series to a list
        return obj.tolist()
    else:
        # Return the object if it's not a dict, list, np.ndarray, or pd.Series
        return obj