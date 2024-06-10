import os
import numpy as np
import json


def parse_data(data):
    """Accepts loaded npz data and formats it into json to be added to the vault db

    Args:
        data (ndarray): Loaded npz data

    Returns:
        inputs (str): json string of experiment input data
        results (str): json string of experiment results. (copy of yhat_details)
        checksum (str): checksum string of results dict.
    """


    # Parse input fields and add to dict 
    input_fields = ['y','X','theta','Options']
    inputs = {}
    
    # Loop through fields and add their data to an inputs dictionary
    for field in input_fields:
        inputs[field] = data[field]

    # Parse results fields 
    results = data['yhat_details']

    # add checksum to this logic here
    

    # Return json formatted inputs and results
    return json.dumps(inputs), json.dumps(results), "checksum will be here"



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
                    inputs, results, checksum = parse_data(obj)
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
    