import os
import numpy as np
import json
import sys

# Move path to access helper functions
current_file_path = os.path.abspath(__file__)
three_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
sys.path.insert(0, three_levels_up)

# Import necessary csa_common_lib modules
from helpers._vault_io import prepare_vault_data
from helpers._conversions import convert_to_float32
from toolbox.classes.class_utils import class_obj_to_dict, is_obj_userdefined_class


def load_npz(file_path:str):
    """Loads passed .npz and returns a dict object

    Args:
        file_path (str): Path to npz file 

    Returns:
        obj (dict): dictionary of key/values in the npz
    """


    if os.path.exists(file_path):

        # Try loading the npz into an obj variable to be parsed
        try:
            with np.load(os.path.normpath(file_path), allow_pickle=True) as obj:

                # Try parsing the npz file into database fields
                try:
                    inputs, results, checksum = prepare_vault_data(obj)
                    return inputs, results, checksum
                except Exception as e:
                    print("Failed to parse npz data: ", e)
                    return None, None, None
                
        except Exception as e:
            print("Failed to load npz: ", e)
            return None, None, None
    else:
        print(f"Invalid file path {file_path}")
        return None, None, None
    


        
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