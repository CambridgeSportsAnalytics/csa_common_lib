import numpy as np


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
        
