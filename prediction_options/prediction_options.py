

class PredictionOptions:

    """
    Prediction Options Class:
        Supports a master default list of all possible input options used by predict, maxfit and optvar. 
        Some models overlap in input options but setting a parameter that is not used by a given model will
        not affect it. 
        
        See documentation for option definitions: {put gitbook link here}

    """

    def __init__(self):
        self.threshold_range = (0, 1)
        self.stepsize = 0.20
        self.most_eval = True
        self.eval_type = "relevance"  # Default value is "relevance"
        self.cov_inv = None
        self.objective = "adjusted_fit"
        self.adj_fit_multiplier = "K"
        self.return_grid = False
        self.attribute_combi = None
        self.k = None
        self.return_weights_grid = False
        self.threshold = None
        self.is_threshold_percent = True


# Not a method. This function creates a new object and returns it
def update_options(inputs):
    options = PredictionOptions()
    for key, value in inputs.items():
        if hasattr(options, key):
            setattr(options, key, value)
    return options