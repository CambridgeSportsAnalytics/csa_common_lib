from enum import Enum

class LambdaError(Enum):
    """Enumeration of lambda error codes and messages

    Parameters
    ----------
    Enum : Lambda status codes
        AWS lambda status codes and assigned messages. 
    """

    # Post-job
    POST_JOB = (1, 'Something went wrong while posting a job to the server.')

    # Process Job    
    PROCESS_JOB = (2, 'Something went wrong while processing a job.')
    PREDICTION = (3, 'Prediction task failed.') # haven't come up with a good message yet.
    PAYLOAD = (4, 'Unable to parse input payload')
    X_INPUT = (5, 'Failed to load X_matrix input.')
    SAVE_RESULTS = (6, 'Failed to save prediction results.')
