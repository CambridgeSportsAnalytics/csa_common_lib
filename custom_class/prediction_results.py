import numpy as np
import pandas as pd
#import statsmodels.api as sm
from csa_common_lib.toolbox.stats import summary


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
        """
        Returns a printout summary of individual yhat_details values

        """


        df = pd.DataFrame({
            'yhat': self.yhat,
            'y_linear': self.y_linear,
            'fit': self.fit,
            'adj_fit': self.adjusted_fit,
            'agreement': self.agreement
            
        })

        df['yhat_nonlin'] = df['yhat'] - df['y_linear']

        print(df.head())
        return df


    def attributes(self):
        """
        Returns a list of all accessible attributes in the class

        """


        attribute_list = [key for key in self.__dict__.keys() if not key.startswith('__')]
        print("Results Attributes:")
        for attribute in attribute_list:
            print(f"  .{attribute}")


    def lin_comp(self, y_actuals):
        """Generates a summary of the influence of linear and non linear components
        in the prediction results

        Args:
            y_actuals (pandas series): Pandas series of correct prediction results 
                extracted from initial dataset to assess accuracy of the predictions
        """
        data = summary.rbp_linear_component(self.y_linear, self.yhat, y_actuals)
        print("Linear component analysis: \n", data)
    

    # TODO --> Change repr to be simpler
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key, value in self.__dict__.items())
        return f"\nResults:\n--------- \n{attributes}\n--------- "