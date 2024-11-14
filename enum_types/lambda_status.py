from enum import Enum

class LambdaStatus(Enum):
    """Enumeration of lambda status codes + messages.

    Parameters
    ----------
    Enum : PSR Result Types
        AWS lambda status codes and assigned messages. 
    """
    # Post-job
    INITIALIZED = (0, 'initalized') # Inputs initialized in the database
    PENDING = (1, 'pending') # Inputs are waiting to be processed

    # Process Job    
    PROCESSING = (10, 'processing') # Currently processing the job
    COMPLETED = (11, 'completed') # Prediction task has been completed
