import psr_lambda

from .npz_io import save_to_npz

# Import necessary csa_common_lib modules
from csa_common_lib.custom_class.prediction_options import PredictionOptions
from csa_common_lib.custom_class.vault_metadata import VaultMetadata
from csa_common_lib.helpers._vault import validate_vault_npz_data
from csa_common_lib.toolbox.classes.class_utils import class_obj_to_dict


def save(api_key:str, filename:str, y, X, theta, yhat_details, Metadata:VaultMetadata, Options:PredictionOptions = PredictionOptions()):
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
        Status printout and .npz file
    """


    # Package all the input fields in a dictionary
    inputs = {'y': y,'X':X,'theta':theta,'options':class_obj_to_dict(Options)['options']}


    observations, y_metrics = Metadata.observations, Metadata.y_metric

    validate_data_flag = validate_vault_npz_data(y, X, theta, yhat_details, Metadata, Options=Options) 
    if validate_data_flag is True:
        # Use endpoint wrapper to post vault metadata and retrieve reference ids
        metadata_ids = psr_lambda.post_vault_metadata(api_key=api_key,observations=observations, y_metrics=y_metrics)

        # Check that metadata post wrapper returns the data we need for saving
        if 'observations' in metadata_ids.keys() and 'y_metrics' in metadata_ids.keys():

            # Check that metadata id arrays are not empty
            if len(metadata_ids['observations']) > 0 and len(metadata_ids['y_metrics']) > 0:

                # Overwrite metadata fields with reference ids before packaging
                Metadata.observations = metadata_ids['observations']
                Metadata.y_metric = metadata_ids['y_metrics']
            else:
                raise ValueError("Returned metadata id list was empty")
        else:
            raise ValueError("Vault metadata not returned")
        
    # Package metadata
    metadata = class_obj_to_dict(Metadata)['metadata']

    save_to_npz(filename=filename, single_precision= False, inputs=inputs,
                      results=yhat_details, metadata=metadata)
    
    return f"{filename}.npz generated"