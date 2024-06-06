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
        self.eval_type = "relevance"  # Default value is "relevance"
        self.attribute_combi = None
        self.max_num_combi = 1000000
        self.k = None
        self.cov_inv = None
        self.objective = "adjusted_fit"
        self.adj_fit_multiplier = "K"
        self.return_grid = False
        self.return_weights_grid = False
        

    def options_to_ndarray(self):
        """Converts passed PredctionOptions obj into an ndarray so that it can be easily packaged locally into
        .npz outputs

        Returns:
            ndarray: Numpy array able to formatted easily into a .npz file
        """


        options_ndarray = []
        for attribute in dir(self):
            if not attribute.startswith("__"):
                options_ndarray.append(getattr(self, attribute))
        return np.array(options_ndarray)


def update_options(inputs):
    """ Accepts a dictionary of inputs and returns a PredictionOptions obj updated with all passed optional values

    Args:
        inputs (dict): Intakes a dictionary of inputs deconstructed in the lambda function

    Returns:
        PredictionOptions:  PredictionOptions obj that holds all passed optional values. Non-passed options remain default setting
    """


    options = PredictionOptions()
    for key, value in inputs.items():
        if hasattr(options, key):
            setattr(options, key, value)

    return options
