import numpy as np


class PredictionOptions:
    """
    Prediction Options Class:
    Supports a master default list of all possible input options used by predict, maxfit and optvar.
    Some models overlap in input options but setting a parameter that is not used by a given model will
    not affect it.

    See documentation for option definitions: {put gitbook link here}
    """

    def __init__(self):
        self.threshold = None
        self.is_threshold_percent = True
        self.threshold_range = np.array((0, 0.20, 0.50, 0.80))
        self.stepsize = 0.20
        self.most_eval = True
        self.eval_type = "relevance" 
        self.attribute_combi = None
        self.max_num_combi = 1_000_000
        self.k = None
        self.cov_inv = None
        self.objective = "adjusted_fit"
        self.adj_fit_multiplier = "K"
        self.is_return_grid = False
        self.is_return_weights_grid = False
        


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

