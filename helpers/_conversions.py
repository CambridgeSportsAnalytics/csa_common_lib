import numpy as np
import os

# Conditionally import pandas if not in a Lambda environment
if os.getenv('LAMBDA_ENV') is None:
    import pandas as pd


def convert_to_float32(obj):
    """
    Recursively converts all numerical values in a dictionary or list to 
    float32. If `obj` is neither a dictionary nor a list, it directly attempts 
    to convert `obj` to float32.

    Parameters
    ----------
    obj : dict, list, or any
        The dictionary, list, or numerical value to convert.

    Returns
    -------
    obj : dict, list, or any
        The converted object with all numerical values as float32, or the 
        original object if conversion is not applicable.
    """
    
    if isinstance(obj, dict):
        # Recursively convert all values in the dictionary to float32.
        return {k: convert_to_float32(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively convert all elements in the list to float32.
        return [convert_to_float32(elem) for elem in obj]
    else:
        # Attempt to convert the object to float32 if it is a numerical value.
        try:
            return np.float32(obj)
        except (ValueError, TypeError):
            # Return the object as-is if it cannot be converted.
            return obj


def convert_dict_to_list(obj):
    """
    Recursively converts numpy arrays and pandas Series in the dictionary 
    to lists. It handles nested dictionaries and lists as well.

    Parameters
    ----------
    obj : dict, list, np.ndarray, pd.Series, or any
        The dictionary, list, numpy array, pandas Series, or other object 
        to convert.

    Returns
    -------
    obj : dict, list, or any
        The converted object with all numpy arrays and pandas Series 
        converted to lists, or the original object if conversion is not applicable.
    """
    if isinstance(obj, dict):
        # Recursively convert all values in the dictionary.
        return {k: convert_dict_to_list(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively convert all elements in the list.
        return [convert_dict_to_list(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        # Convert numpy array to a list.
        return obj.tolist()
    elif 'pd' in globals() and isinstance(obj, pd.Series):
        # Convert pandas Series to a list if pandas is available.
        return obj.tolist()
    else:
        # Return the object as-is if no conversion is applicable.
        return obj
    
    
def convert_ndarray_to_list(obj):
    """
    Recursively converts numpy ndarrays within an object to lists.
    
    Parameters:
    obj (any): The input object which may contain numpy ndarrays.

    Returns:
    any: The converted object with all numpy ndarrays turned into lists.
    """

    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarray_to_list(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarray_to_list(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_ndarray_to_list(item) for item in obj)
    else:
        return obj
    