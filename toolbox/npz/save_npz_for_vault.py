from .npz_io import save_to_npz

# Import necessary csa_common_lib modules
from csa_common_lib.custom_class.prediction_options import PredictionOptions
from csa_common_lib.custom_class.vault_metadata import VaultMetadata
from csa_common_lib.helpers._vault import validate_vault_npz_data
from csa_common_lib.toolbox.classes.class_utils import class_obj_to_dict


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


    #observations, metric_id = Metadata.person_id, Metadata.y_metric_id

    #validate_data_flag = validate_vault_npz_data(y,X,theta,yhat_details, Metadata)
    # if validate_data_flag is true --> handle metadata
    # meta_data_flag = vault_metadata_handler(observations, metric_id) [endpoint --> lambda call]
    # if flag is True --> package metadata and save_to_npz

    # Package metadata
    metadata = class_obj_to_dict(Metadata)['metadata']

    save_to_npz(filename=filename, single_precision= False, inputs=inputs,
                      results=yhat_details, metadata=metadata)
    
    return f"{filename}.npz generated"