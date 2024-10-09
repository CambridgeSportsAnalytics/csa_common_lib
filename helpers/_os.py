import os

def is_valid_path(path:str):
    # Get the directory part of the path
    directory = os.path.dirname(path)
    
    # Check if the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    # Check if the directory is writable
    if not os.access(directory, os.W_OK):
        raise PermissionError(f"The directory '{directory}' is not writable.")

    return True  # If no exceptions were raised, the path is valid