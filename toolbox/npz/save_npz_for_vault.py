import json
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


    Xcol_labels, Xrow_labels, outcome_labels, y_metric = Metadata.Xcol_labels, Metadata.Xrow_labels, Metadata.outcome_labels, Metadata.y_metric

    validate_data_flag = validate_vault_npz_data(y, X, theta, yhat_details, Metadata, Options=Options) 
    if validate_data_flag is True:

        # Use endpoint wrapper to post vault metadata and retrieve reference ids
        metadata_response = psr_lambda.post_vault_pointer_data(api_key=api_key, 
                                                            Xcol_labels=Xcol_labels,
                                                            Xrow_labels=Xrow_labels,
                                                            outcome_labels=outcome_labels,
                                                            y_metric=y_metric, X=X, y=y)
        metadata_ids = json.loads(metadata_response)
        
        """
        # Check that metadata post wrapper returns the data we need for saving
        if metadata_ids['pointers']:
            metadata_ids = json.loads(metadata_response)['pointers']

            # Check that metadata id arrays are not empty
            if len(metadata_ids['observations']) > 0 and metadata_ids['y_metric']:

                # Overwrite metadata fields with reference ids before packaging
                Metadata.observations = metadata_ids['observations']
                Metadata.y_metric = metadata_ids['y_metric']
            else:
                raise ValueError("Returned metadata list was empty")
        else:
            raise ValueError("Vault metadata not returned")
        """
    # Package metadata
    metadata = class_obj_to_dict(Metadata)['metadata']

    save_to_npz(filename=filename, single_precision= False, inputs=inputs,
                      results=yhat_details, metadata=metadata)
    
    return f"{filename}.npz generated"