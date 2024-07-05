import numpy as np
import pandas as pd

class PredictionResults:
    """
    Prediction Results Class:
    Stores an array of dictionaries containing prediction results,
    filters specific attributes into their respective arrays.
    """

    def __init__(self, results):
        self.raw_data = results
        self._initialize_attributes()

    def _initialize_attributes(self):
        allowed_keys = [
            'yhat', 'weights', 'weights_excluded', 'relevance', 'similarity',
            'info_x', 'info_theta', 'include', 'lambda_sq', 'n', 'K', 'phi',
            'r_star', 'r_star_percent', 'most_eval', 'eval_type', 'adjusted_fit',
            'fit', 'rho', 'agreement', 'outlier_influence', 'asymmetry', 'y_linear'
        ]

        for key in allowed_keys:
            values = []
            for item in self.raw_data:
                if key in item:
                    value = item[key]
                    if isinstance(value, np.ndarray) and value.shape == (1, 1):
                        value = value[0][0]
                    values.append(value)
            setattr(self, key, values)


    def display(self):
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")


    def head(self):
        df = pd.DataFrame({
            'yhat': self.yhat,
            'y_linear': self.y_linear,
            'fit': self.fit,
            'adj_fit': self.adjusted_fit,
            'agreement': self.agreement
            
        })

        print(df.head())
        return df


    def attributes(self):
        attribute_list = [key for key in self.__dict__.keys() if not key.startswith('__')]
        print("Results Attributes:")
        for attribute in attribute_list:
            print(f"  .{attribute}")

    
    # TODO --> Change repr to display Davids core summary stats so the user can immediately assess the results before digging deeper. 
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key, value in self.__dict__.items())
        return f"\nResults:\n--------- \n{attributes}\n--------- "