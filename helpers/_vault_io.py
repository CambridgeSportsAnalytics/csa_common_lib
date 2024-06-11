import json


def prepare_vault_data(data):
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
