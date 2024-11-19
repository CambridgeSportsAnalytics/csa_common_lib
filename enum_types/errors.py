from enum import Enum

class LambdaError(Enum):
    """Enumeration of lambda error codes and messages

    Parameters
    ----------
    Enum : Lambda status codes
        AWS lambda status codes and assigned messages. 
    """

    # No error
    NO_ERROR = (0, 'No error')

    # Post-job
    POST_JOB = (1, 'GURU MEDITATION ERROR: Something went wrong while posting a job to the server.')

    # Process Job    
    PROCESS_JOB = (2, 'GURU MEDITATION ERROR: Something went wrong while processing a job.')
    PREDICTION = (3, 'GURU MEDITATION ERROR: Prediction task failed.') # haven't come up with a good message yet.
    PAYLOAD = (4, 'GURU MEDITATION ERROR: Unable to parse input payload')
    X_INPUT = (5, 'GURU MEDITATION ERROR: Failed to load X_matrix input.')
    SAVE_RESULTS = (6, 'GURU MEDITATION ERROR: Failed to save prediction results.')

    @classmethod
    def error_by_code(cls, code):
        """Retrieve the full enum object based on the code."""

        for error in cls:
            if error.value[0] == code:
                return error.value
        return None  