from csanalytics_local.classes._vault_metadata import VaultMetadata
from csa_common_lib.classes.prediction_options import PredictionOptions


def validate_vault_npz_data(y, X, theta, yhat_details, 
                            Metadata: VaultMetadata, Options: PredictionOptions = None) -> bool:
    """
    Validates the formatting of input data before saving to a .npz file.
    Ensures that all data arrays and metadata are consistent and correctly formatted.

    Parameters
    ----------
    y : ndarray
        Array of dependent variable data.
    X : ndarray
        Matrix of independent variables data.
    theta : ndarray
        Matrix of experimental conditions or circumstances.
    yhat_details : dict
        Result data generated from a prediction.
    Metadata : VaultMetadata
        Custom object for storing supporting experiment data, such as labels 
        and additional metadata information.
    Options : PredictionOptions, optional
        Custom object for storing optional prediction parameters.
        Also accepts MaxFitOptions and GridOptions 
        (inherits from PredictionOptions), defaults to None.

    Raises
    ------
    ValueError
        If any of the data or metadata formats are inconsistent or incorrect.

    Returns
    -------
    bool
        True if all data and metadata are formatted correctly.
    """

    # Check that Metadata attributes are lists
    if not isinstance(Metadata.Xcol_labels, list):
        raise ValueError(
            f"Metadata.Xcol_labels needs to be of type list. It is of type: {type(Metadata.Xcol_labels)}"
        )
    if not isinstance(Metadata.Xrow_labels, list):
        raise ValueError(
            f"Metadata.Xrow_labels needs to be of type list. It is of type: {type(Metadata.Xrow_labels)}"
        )
    if not isinstance(Metadata.outcome_labels, list):
        raise ValueError(
            f"Metadata.outcome_labels needs to be of type list. It is of type: {type(Metadata.outcome_labels)}"
        )

    # Check that column dimensions match across data
    if len(theta) > 0:
        if len(theta[0]) != len(Metadata.Xcol_labels):
            raise ValueError("The number of variables in theta does not match Metadata.Xcol_labels.")
        if len(Metadata.outcome_labels) != len(theta):
            raise ValueError("Metadata.outcome_labels does not match the length of theta.")

    if len(Metadata.Xrow_labels) != len(X):
        raise ValueError("Metadata.Xrow_labels does not match the number of rows in the X matrix.")
    if len(Metadata.Xrow_labels) != len(y):
        raise ValueError("Metadata.Xrow_labels does not match the number of observations in y (inputs).")
    if len(theta) < 1:
        raise ValueError("Theta is empty. Please supply experimental conditions.")
    if len(y) != len(X):
        raise ValueError("Mismatch in the number of observations between X and y (inputs).")

    # If no formatting errors are detected, return True
    return True