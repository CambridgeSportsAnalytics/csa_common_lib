import sys
import os
import numpy as np

from csa_common_lib.custom_class.vault_metadata import VaultMetadata
from csa_common_lib.custom_class.prediction_options import PredictionOptions


def validate_vault_npz_data(y, X, theta, yhat_details, Metadata:VaultMetadata, Options:PredictionOptions) -> bool:
    """Validates npz formatting before saving to .npz file. Ensures data is loaded cleanly.

    Args:
        y : y input data
        X : X input data
        theta : theta input data
        yhat_details : result data generated from a prediction
        Metadata (VaultMetadata): Custom object for storing supporting experiment data
        Options (PredictionOptions, optional): Custom object for storing optional prediction paramaters 
            Defaults to PredictionOptions().

    Raises:
        ValueError: Description of formatting error

    Returns:
        bool: flag describing if data is formatted correctly
    """

    k = int(Options.k)

    # Check that column dimensions match accross data 
    if len(theta) < 1:
        raise ValueError("Theta is empty. Please supply experiment conditions")
    if len(theta) > 0:
        if len(theta[0]) != k:
            raise ValueError("The number of variables in theta does not match k")
    if len(Metadata.x_labels) != k: 
        raise ValueError("The number of supplied X_labels does not match k")
    if len(y) != len(X):
        raise ValueError("Mismatch in # of observations between X and y (inputs)")
    if not isinstance(Metadata.observations, list):
        raise ValueError("Metadata.observations needs to be of type list. It is of type: ", str(type(Metadata.observations)))
    if not isinstance(Metadata.y_metric, list):
        raise ValueError("Metadata.y_metric needs to be of type list. It is of type: ", str(type(Metadata.y_metric)))
    
    # If not of the above formatting errors come up, return True.
    return True