import copy
import numpy as np

class PredictionOptions:
    """
    Prediction Options Class:
    Supports a master default list of all possible input options used by predict, maxfit and optvar.
    Some models overlap in input options but setting a parameter that is not used by a given model will
    not affect it.
    """

    def __init__(self, **kwargs):
        self.options = {
            'threshold': [0],
            'is_threshold_percent': True,
            'most_eval': True,
            'eval_type': 'both',
            'adj_fit_multiplier': 'K',
            'cov_inv': None,
        }

        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)


    def __getattr__(self, name):
        # Check if 'options' is in self.__dict__ to avoid KeyError
        if 'options' in self.__dict__ and name in self.__dict__['options']:
            return self.__dict__['options'][name]
        raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")


    def __setattr__(self, name, value):
        if name == "options":
            super().__setattr__(name, value)
        elif 'options' in self.__dict__ and name in self.options:
            self.options[name] = value
        else:
            raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")


    def display(self):
        for key, value in self.options.items():
            print(f"{key}: {value}")

    
    # def __repr__(self):
    #     class_type = str(type(self)).split(".")[-1].split("'")[0]
    #     f"{class_type}\n{self.display()}\n"


    def init_from_dict(self, inputs):
        """ Accepts a dictionary of inputs and returns a PredictionOptions obj 
        updated with all passed optional values. Essentially an update method

        Args:
            inputs (dict): Intakes a dictionary of inputs deconstructed in the 
            lambda function

        Returns:
            PredictionOptions:  PredictionOptions obj that holds all passed optional values. Non-passed options remain default setting
        """

        
        # Iterate through input dict key/value pairs
        for key, value in inputs.items():
            # If obj attribute matches key in input dict
            if hasattr(self, key):
                # Update corresponding attribute in options object to hold dictionary value
                super().__setattr__(key, value)  # Use super() to avoid calling custom __setattr__


    def clone_with(self, **kwargs):
        """ Returns a clone of the passed PredictionOptions object with user-specified 
        attribute overwrites (via key value pairs)

        Args:
            key/value pair (attr/value): Attributes to overwrite in the cloned obj 
            lambda function

        Returns:
            PredictionOptions:  PredictionOptions obj 
        """


        new_copy = copy.deepcopy(self)
        for key, value in kwargs.items():
            setattr(new_copy, key, value)
        return new_copy


class MaxFitOptions(PredictionOptions):
    """
    MaxFitOptions Class:
    Inherits from PredictionOptions and adds additional options.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options.update({
            'threshold': None,
            'threshold_range': (0, 1),
            'stepsize': 0.20,
            'objective': 'adjusted_fit',
            'is_return_grid': False,
        })
        
        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)


class OptVarOptions(MaxFitOptions):
    """
    OptVarOptions Class:
    Inherits from MaxFitOptions and adds additional options.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options.update({
            'attribute_combi': None,
            'max_iter': 1_000_000,
            'k': 1,
            'is_return_weights_grid': False,
        })
        
        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)