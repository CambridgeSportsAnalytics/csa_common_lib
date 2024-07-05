import numpy as np

class PredictionResults:
    """
    Prediction Results Class:
    Stores an array of dictionaries containing prediction results,
    filters specific attributes into their respective arrays.
    """

    def __init__(self, results):
        self.yhat = None
        self.weights = None
        self.weights_excluded = None
        self.relevance = None
        self.similarity = None
        self.info_x = None
        self.info_theta = None
        self.include = None
        self.lambda_sq = None
        self.n = None
        self.K = None
        self.phi = None
        self.r_star = None
        self.r_star_percent = None
        self.most_eval = None
        self.eval_type = None
        self.adjusted_fit = None
        self.fit = None
        self.rho = None
        self.agreement = None
        self.outlier_influence = None
        self.asymmetry = None
        self.y_linear = None
        self.raw_data = None

        self.flatten_and_store(results)

    def flatten_and_store(self, results):
        setattr(self,"raw_data",results)

        for result in results:
            for key, value in result.items():
                if isinstance(value, list) and len(value) == 1:
                    setattr(self, key, value[0])  # Flatten single-element list to scalar
                elif isinstance(value, list):
                    getattr(self, key).append(value)  # Store lists as-is
                else:
                    setattr(self, key, value)  # Store non-list values as-is

        # Convert attributes with shape (1, n) to flat arrays
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                value = getattr(self, attr)
                if isinstance(value, np.ndarray) and value.shape[0] == 1:
                    setattr(self, attr, np.squeeze(value))

    def display(self):
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")


    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key, value in self.__dict__.items())
        return f"\nResults:\n--------- \n{attributes}\n--------- "