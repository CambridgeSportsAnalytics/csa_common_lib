
# Third-party library imports
import numpy as np  # Third-party library import

# Local application / library-specific imports
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # For parallel processing
from csa_common_lib.toolbox import _notifier # For notification handling
from dotenv import load_dotenv

# Import api credentials from a .env file as environment variables
load_dotenv() 

def run_tasks_local(inputs, dispatcher, max_workers:int, notifier):
    """
    Generic function to run parallel tasks using the provided dispatcher.

    Parameters
    ----------
    inputs : list of tuples
        List of arguments to be passed to the dispatcher function.
    dispatcher : callable
        The dispatcher function that will handle each task.
    max_workers : int
        Maximum number of workers to use in the ProcessPoolExecutor.
    notifier : object
        Notifier object to manage notifications and state.

    Returns
    -------
    yhat : ndarray
        Aggregated prediction outcomes.
    yhat_details : list
        List of detailed model results.
    """
    
    
    # Get the current notifier state and disable the notifier
    n_state = notifier.get_notifier_status()
    notifier.disable_notifier()

    # Execute tasks in multi-threaded pool
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(dispatcher, inputs))

    # Restore notifier state
    notifier.set_notifier_status(n_state)

    # Unpack yhat results
    yhat = np.vstack([result[0] for result in results])

    # Unpack output_details results using list comprehension
    yhat_details = [result[1] for result in results]

    return yhat, yhat_details


def run_tasks_api(inputs, dispatcher, get_results_dispatcher, max_workers:int, notifier):
    """
    Generic function to run parallel tasks using the 
    provided dispatcher for CSA API calls.

    Parameters
    ----------
    inputs : list of tuples
        List of arguments to be passed to the dispatcher function.
    dispatcher : callable
        The dispatcher function that will handle each task.
    get_results_dispatcher : callabale
        The dispatcher function that will retrieve results from the API.
    max_workers : int
        Maximum number of workers to use in the ProcessPoolExecutor.
    notifier : object
        Notifier object to manage notifications and state.

    Returns
    -------
    yhat : ndarray
        Aggregated prediction outcomes.
    yhat_details : list
        List of detailed model results.
    """
    
    
    # Get the current notifier state and disable the notifier
    n_state = notifier.get_notifier_status()
    notifier.disable_notifier()

    # Execute tasks in multi-threaded pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        jobs = list(executor.map(dispatcher, inputs))

    # Unpack job_id and job_code using list comprehension
    job_id, job_code = zip(*jobs)
    
    # Once we have all the job_id and job_codes for all the corresponding
    # prediction tasks, we can get the results from CSA's server
    inputs_for_get = [
        (job_id[q], job_code[q]) for q in range(len(jobs))
    ]
    
    # Dispatch the get_results task in a multi-threaded pool
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(get_results_dispatcher, inputs_for_get))
        
    # restore notifier state
    _notifier.set_notifier_status(n_state)

    # Unpack yhat results
    yhat = np.vstack([result[0] for result in results])
    
    # Unpack output_details results using list comprehension
    yhat_details = [result[1] for result in results]

    # Return results
    return yhat, yhat_details