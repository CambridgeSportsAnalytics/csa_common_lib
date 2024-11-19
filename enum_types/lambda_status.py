from enum import Enum

class LambdaStatus(Enum):
    """Enumeration of lambda status codes + messages.

    Parameters
    ----------
    Enum : Lambda status codes
        AWS lambda status codes and assigned messages. 
    """

    # Post-job
    INITIALIZED = (0, 'initialized') # Inputs initialized in the database
    PENDING = (1, 'pending') # Inputs are waiting to be processed

    # Process Job    
    PROCESSING = (10, 'processing') # Currently processing the job
    COMPLETED = (11, 'completed') # Prediction task has been completed

    @classmethod
    def status_by_code(cls, code):
        """Retrieve the full enum object based on the code."""
        for status in cls:
            if status.value[0] == code:
                return status.value
        return None  