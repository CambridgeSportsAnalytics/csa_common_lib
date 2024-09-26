import sys
import os
import numpy as np

from csanalytics_local.private_classes._vault_metadata import VaultMetadata
from csa_common_lib.classes.prediction_options import PredictionOptions


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


    # check list types
    if not isinstance(Metadata.Xcol_labels, list):
        raise ValueError("Metadata.Xcol_labels needs to be of type list. It is of type: ", str(type(Metadata.Xcol_labels)))
    if not isinstance(Metadata.Xrow_labels, list):
        raise ValueError("Metadata.Xrow_labels needs to be of type list. It is of type: ", str(type(Metadata.Xrow_labels)))
    if not isinstance(Metadata.outcome_labels, list):
        raise ValueError("Metadata.outcome_labels needs to be of type list. It is of type: ", str(type(Metadata.outcome_labels)))


    # Check that column dimensions match accross data 
    if len(theta) > 0:
        if len(theta[0]) != len(Metadata.Xcol_labels):
            raise ValueError("The number of variables in theta does not match Metadata.Xcol_labels")
        if len(Metadata.outcome_labels) != len(theta):
            raise ValueError("Metadata.outcome_labels does not match the length of theta")
    
    if len(Metadata.Xrow_labels) != len(X):
        raise ValueError("Metadata.Xrow_labels does not match the length of t in the X matrix")
    if len(Metadata.Xrow_labels) != len(y):
        raise ValueError("Metadata.Xrow_labels does not match the length of y (inputs)")
    if len(theta) < 1:
        raise ValueError("Theta is empty. Please supply experiment conditions")
    if len(y) != len(X):
        raise ValueError("Mismatch in # of observations between X and y (inputs)")
    
    
    
    
    # If not of the above formatting errors come up, return True.
    return True