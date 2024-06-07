import inspect


def class_to_dict(obj):
    """Converts any class object into a dictionary containing its attributes and
    respective values

    Args:
        obj : Class object of any type and isntantiation method

    Returns:
        attributes (dict): Dictionary of class attributes 
    """


    if hasattr(obj, '__dict__'):
        # If the object has __dict__, meaning it's an instance of a class with __init__,
        # we can directly return its __dict__ attribute.
        return obj.__dict__
    else:
        # If __dict__ doesn't exist, we'll inspect the object to find its attributes.
        attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
        return {name: value for name, value in attributes if not name.startswith('_')}
