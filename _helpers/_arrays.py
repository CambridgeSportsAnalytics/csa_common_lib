

# Helper function to flatten nested lists
def flatten_nested_list(nested_list):
    if isinstance(nested_list, list) and len(nested_list) == 1 and isinstance(nested_list[0], list):
        return nested_list[0][0]  # Return the first element of the nested list
    return nested_list  # Return the element as is if not nested
