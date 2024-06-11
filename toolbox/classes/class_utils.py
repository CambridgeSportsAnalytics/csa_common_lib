import inspect


def class_obj_to_dict(obj):
    """Converts any class object into a dictionary containing its attributes and
    respective values

    Args:
        obj : Class object of any type and isntantiation method

    Returns:
        attributes (dict): Dictionary of class attributes 
    """


    if hasattr(obj, '__dict__'):
        # If the object has __dict__, return its __dict__ attribute.
        return obj.__dict__
    else:
        # If __dict__ doesn't exist, find object attributes.
        attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
        return {name: value for name, value in attributes if not name.startswith('_')}


def is_obj_userdefined_class(obj):
    """Check if the object is a user-defined class instance.

    Args:
        obj : Class object of any type and isntantiation method

    Returns:
        bool : is user-defined-class flag
    """


    obj_type = type(obj)

    # if object is type class + not builtin module --> user defined class: True
    if inspect.isclass(obj_type) and obj_type.__module__ != 'builtins':
        return True
    else:
        return False


