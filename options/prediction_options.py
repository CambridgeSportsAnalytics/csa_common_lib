import numpy as np


class PredictionOptions:
    """
    Prediction Options Class:
    Supports a master default list of all possible input options used by predict, maxfit and optvar.
    Some models overlap in input options but setting a parameter that is not used by a given model will
    not affect it.

    See documentation for option definitions: {put gitbook link here}
    """

    def __init__(self, **kwargs):
        self._options = {
            'threshold_range': (0, 1),
            'stepsize': 0.20,
            'most_eval': True,
            'eval_type': 'relevance',
            'cov_inv': None,
            'objective': 'adjusted_fit',
            'adj_fit_multiplier': 'K',
            'return_grid': False,
            'attribute_combi': None,
            'k': None,
            'return_weights_grid': False,
            'threshold': None,
            'is_threshold_percent': True
        }
            
        # Update attributes with any provided kwargs
        if kwargs:
            for key, value in kwargs.items():
                self.__setattr__(key,value)


    def __getattr__(self, name):
        if name in self._options:
            return self._options[name]
        raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == "_options":
            super().__setattr__(name, value)
        elif name in self._options:
            self._options[name] = value
        else:
            raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")

    def display(self):
        for key, value in self._options.items():
            print(f"{key}: {value}")


    def update_options(self, inputs):
        """ Accepts a dictionary of inputs and returns a PredictionOptions obj updated with all passed optional values

        Args:
            inputs (dict): Intakes a dictionary of inputs deconstructed in the lambda function

        Returns:
            PredictionOptions:  PredictionOptions obj that holds all passed optional values. Non-passed options remain default setting
        """

        # Iterate through input dict key/value pairs
        for key, value in inputs.items():

            # If obj attribute matches key in input dict
            if hasattr(self, key):

                # Update corresponding attribute in options object to hold dictionary value
                setattr(self, key, value)

