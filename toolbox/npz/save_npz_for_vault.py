import sys
import os

from npz_io import load_npz
from npz_io import save_to_npz

# Move path to access helper functions
current_file_path = os.path.abspath(__file__)
three_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
sys.path.insert(0, three_levels_up)

# Import necessary csa_common_lib modules
from custom_class.prediction_options import PredictionOptions
from custom_class.vault_metadata import VaultMetadata


sys.path.insert(0, os.path.dirname(three_levels_up))
import psr_lambda

# temp removing parameters: filename:str, y, X, theta, Metadata:VaultMetadata, Options:PredictionOptions=PredictionOptions()
def save():
    # If Prediction Options not supplied uses default settings.
    

    #save = save_to_npz(filename=filename, single_precision= False, y=y,
     #                   X=X, theta=theta, Options=Options, Metadata=Metadata)
    
    return None