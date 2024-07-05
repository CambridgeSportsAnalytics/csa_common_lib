import numpy as np
import pandas as pd
import statsmodels.api as sm

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


    def head(self, y_actuals=None):

        df = pd.DataFrame({
            'yhat': self.yhat,
            'y_linear': self.y_linear,
            'fit': self.fit,
            'adj_fit': self.adjusted_fit,
            'agreement': self.agreement
            
        })

        df['yhat_nonlin'] = df['yhat'] - df['y_linear']

        # If y_actuals are supplied, we generate t-stats as well
        if y_actuals is not None:
            # Flatten ndarray and convert to regular array
            if isinstance(y_actuals, np.ndarray):
                y_actuals = y_actuals.flatten().tolist()

            if isinstance(y_actuals, pd.Series):
                y_actuals = y_actuals.astype(int).tolist()    

            # Check dimensions to ensure y_actual matches
            if len(y_actuals) != len(self.yhat) or len(y_actuals) != len(self.y_linear):
                raise Exception("y_actual dimensions do not match y_hat and/or y_linear")
            

            #### PROTOTYPING Replace tstats lib call below with our own function that will go in the csa_common_lib.toolbox.stats module isntead
            """
            # Perform regression and calculate t-stats
            X = sm.add_constant(df[['y_linear', 'yhat_nonlin']])

            # Set y_actuals as a constant and model
            model = sm.OLS(y_actuals, X)
            results = model.fit()

            # Retrieve t-stats
            t_stats = results.tvalues

            print("T-Statistics:")
            print(t_stats)
            """

        print(df.head())
        return df


    def attributes(self):
        attribute_list = [key for key in self.__dict__.keys() if not key.startswith('__')]
        print("Results Attributes:")
        for attribute in attribute_list:
            print(f"  .{attribute}")

    
    # TODO --> Change repr to be simpler
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key, value in self.__dict__.items())
        return f"\nResults:\n--------- \n{attributes}\n--------- "