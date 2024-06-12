import os
import numpy as np
import json
import sys

# Move path to access helper functions
current_file_path = os.path.abspath(__file__)
three_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
sys.path.insert(0, three_levels_up)

# Import necessary csa_common_lib modules
from helpers._conversions import convert_to_float32
from toolbox.classes.class_utils import class_obj_to_dict, is_obj_userdefined_class

sys.path.insert(0, os.path.dirname(three_levels_up))



def load_npz(file_path: str) -> dict:
    """Loads passed .npz and returns a dictionary object

    Args:
        file_path (str): Path to npz file 

    Returns:
        obj (dict): dictionary of key/values in the npz
    """
    if os.path.exists(file_path):
        # Try loading the npz into an obj variable to be parsed
        try:
            with np.load(os.path.normpath(file_path), allow_pickle=True) as npz_file:
                # Initialize an empty dictionary to store the contents
                obj = {}
                
                # Iterate over the keys in the npz file and populate the dictionary
                for key in npz_file.files:
                    # Convert ndarrays to lists
                    if isinstance(npz_file[key], np.ndarray):
                        obj[key] = npz_file[key].tolist()
                    else:
                        obj[key] = npz_file[key]
                        
                return obj

        except Exception as e:
            print("Failed to load npz: ", e)
            return {}
    else:
        print(f"Invalid file path {file_path}")
        return {}

        
def save_to_npz(filename:str=None, single_precision:bool=False, **data):
    """ Saves the data into a compressed file.

    Parameters
    ----------
    **data
        Varargin of data types, input variables. Name of variables are
        preserved for the payload.

    Returns
    -------
    npz_file : TemporaryFile
        Compressed file object
    """
    """
    # Ensure the filename ends with '.npz'
    if not filename.endswith(".npz"):
        filename += ".npz"

    print(1, data["Options"])
    dict_options = class_to_dict(data["Options"])
    print("dictionary", dict_options)

    # Convert Options object to dictionary
    data["Options"] = dict_options
    print(2, data["Options"])
    """

    # Iterate over data keys and convert user-defined-classes to dictionaries
    for key, value in data.items():
        if is_obj_userdefined_class(data[key]):
            data[key] = class_obj_to_dict(value)


     # Convert all data to float32 before saving, if requested
    if single_precision:
        data = {k: convert_to_float32(v) for k, v in data.items()}

        
    # save numpy array(s) or data types into a compressed file
    np.savez_compressed(filename, **data)

    # return the file
    return filename