import sys
import os

from .npz_io import save_to_npz

# Move path to access helper functions
current_file_path = os.path.abspath(__file__)
three_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
sys.path.insert(0, three_levels_up)

# Import necessary csa_common_lib modules
from custom_class.prediction_options import PredictionOptions
from custom_class.vault_metadata import VaultMetadata
from toolbox.classes.class_utils import class_obj_to_dict


def save(filename:str, y, X, theta, yhat_details, Metadata:VaultMetadata, Options:PredictionOptions=PredictionOptions()):
    """save_to_npz() wrapper for uploading to vault results. 

    Args:
        filename (str): name of the saved npz file
        y : y input data
        X : X input data
        theta : theta input data
        yhat_details : result data generated from a prediction
        Metadata (VaultMetadata): Custom object for storing supporting experiment data
        Options (PredictionOptions, optional): Custom object for storing optional prediction paramaters 
            Defaults to PredictionOptions().

    Returns:
        _type_: _description_
    """

    # Package all the input fields in a dictionary
    inputs = {'y': y,'X':X,'theta':theta,'options':class_obj_to_dict(Options)['options']}

    # Convert to dictionary 
    metadata = class_obj_to_dict(Metadata)['metadata']

    save_to_npz(filename=filename, single_precision= False, inputs=inputs,
                      results=yhat_details, Metadata=metadata)
    
    return f"{filename}.npz generated"