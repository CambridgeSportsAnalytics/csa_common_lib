from enum import Enum

class LambdaError(Enum):
    """
    Enumeration of AWS Lambda error codes and messages.

    This class defines error codes and corresponding messages for
    AWS Lambda status codes.

    Attributes
    ----------
    NO_ERROR : tuple
        Code and message for no error.
    POST_JOB : tuple
        Code and message for errors encountered while posting a job to the server.
    PROCESS_JOB : tuple
        Code and message for errors encountered during job processing.
    PREDICTION : tuple
        Code and message for failed prediction tasks.
    PAYLOAD : tuple
        Code and message for input payload parsing errors.
    X_INPUT : tuple
        Code and message for failed loading of X_matrix input.
    SAVE_RESULTS : tuple
        Code and message for failures in saving prediction results.
    """

    # No error
    NO_ERROR = (0, 'No error.')

    # Post-job
    POST_JOB = (10, 'GURU MEDITATION ERROR: A problem occured while posting a prediction task to the server.')

    # Process Job    
    PROCESS_JOB = (20, 'GURU MEDITATION ERROR: An issue occured while computing the prediction task.')
    PREDICTION = (30, 'GURU MEDITATION ERROR: The prediction task failed.')
    PAYLOAD = (40, 'GURU MEDITATION ERROR: Unable to parse input payload')
    X_INPUT = (50, 'GURU MEDITATION ERROR: Failed to load X_matrix input.')
    SAVE_RESULTS = (60, 'GURU MEDITATION ERROR: Unable to save prediction results.')


    @classmethod
    def error_by_code(cls, code):
        """
        Retrieve the full enum object based on the code.

        Parameters
        ----------
        code : int
            The error code to search for.

        Returns
        -------
        tuple or None
            The corresponding error tuple (code, message) if found,
            otherwise `None`.
        """

        for error in cls:
            if error.value[0] == code:
                return error.value
        return None  