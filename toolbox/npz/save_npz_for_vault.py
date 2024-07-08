import json
import requests
import psr_lambda
import numpy as np
import boto3

from .npz_io import save_to_npz

# Import necessary csa_common_lib modules
from csa_common_lib.custom_class.prediction_options import PredictionOptions
from csa_common_lib.custom_class.vault_metadata import VaultMetadata
from csa_common_lib.custom_class.prediction_results import PredictionResults
from csa_common_lib.helpers._vault import validate_vault_npz_data
from csa_common_lib.toolbox.classes.class_utils import class_obj_to_dict

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


def save(api_key:str, filename:str, y, X, theta, Results:PredictionResults, Metadata:VaultMetadata, Options:PredictionOptions):
    """save_to_npz() wrapper for uploading to vault results. 

    Args:
        filename (str): name of the saved npz file
        y : y input data
        X : X input data
        theta : theta input data
        Results : PredictionResults() obj containing result data generated from a prediction
        Metadata (VaultMetadata): Custom object for storing supporting experiment data
        Options (PredictionOptions, optional): Custom object for storing optional prediction paramaters 
            Defaults to PredictionOptions().

    Returns:
        Status printout and .npz file
    """

    # Set raw prediction data to a variable 
    yhat_details = Results.raw_data

    # Package all the input fields in a dictionary
    inputs = {'y': y,'X':X,'theta':theta,'options':class_obj_to_dict(Options)['options']}


    Xcol_labels, Xrow_labels, outcome_labels, y_metric = Metadata.Xcol_labels, Metadata.Xrow_labels, Metadata.outcome_labels, Metadata.y_metric

    validate_data_flag = validate_vault_npz_data(y, X, theta, yhat_details, Metadata, Options=Options) 
    if validate_data_flag is True:

        # Use endpoint wrapper to post vault metadata and retrieve reference ids
        metadata_response = psr_lambda.post_vault_fk_data(api_key=api_key, 
                                                            Xcol_labels=Xcol_labels,
                                                            Xrow_labels=Xrow_labels,
                                                            outcome_labels=outcome_labels,
                                                            y_metric=y_metric, X=X, y=y)
        metadata_ids = json.loads(metadata_response)

        print('Successfully posted metadata to db')
        # Prepare the payload for the POST request
        payload = {
            'metadata_ids': json.dumps(metadata_ids),
            'options': json.dumps(class_obj_to_dict(Options)['options']),
            'Metadata':json.dumps(class_obj_to_dict(Metadata)['metadata']),
            'results': json.dumps(convert_ndarray_to_list(yhat_details)),  # Assuming yhat_details is in an appropriate format
            'theta': json.dumps(convert_ndarray_to_list(theta))
        }

        # Convert payload to JSON string
        payload_json = json.dumps(payload)

        # Upload payload to S3
        s3 = boto3.client('s3')
        bucket_name = 'post-vault'
        s3_key = f'vault_payloads/testing.json'
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=payload_json)
        print("s3 file successfully generated. Waiting for response from post-vault")

        response = requests.post("https://v9spadcya3.execute-api.us-east-1.amazonaws.com/v1/vault", json={'s3_key':str(s3_key)}, headers={'x-api-key': f'{api_key}'})

        return response
        
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
    #metadata = class_obj_to_dict(Metadata)['metadata']

    #save_to_npz(filename=filename, single_precision= False, inputs=inputs,
                     # results=yhat_details, metadata=metadata)
    
    #return f"{filename}.npz generated"