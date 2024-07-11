import numpy as np
import pandas as pd

from csanalytics_local.db_local.controller import connect
from csanalytics_local import vault_upload

from csa_common_lib.toolbox.stats import summary
from csa_common_lib.custom_class.vault_metadata import VaultMetadata
from csa_common_lib.custom_class.prediction_options import PredictionOptions
from csa_common_lib.toolbox.classes.class_utils import class_obj_to_dict


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
            'fit', 'rho', 'agreement', 'outlier_influence', 'asymmetry', 'y_linear',
            'yhat_grid', 'weights_grid', 'adjusted_fit_grid', 'max_attributes',
            'combi_grid', 'yhat_compound', 'adjusted_fit_compound', 'combi_compound',
            'weights_compound', 'fit_compound'
        ]

        if not self.raw_data:
            return
        
        if isinstance(self.raw_data, dict):
            first_item = self.raw_data
            self.raw_data = [self.raw_data]
        else:
            first_item = self.raw_data[0]

        if not isinstance(first_item, dict):
            raise TypeError("Items in raw_data must be dictionaries")
        
        keys_to_populate = [key for key in first_item if key in allowed_keys]

        for key in keys_to_populate:
            values = []
            for item in self.raw_data:
                if key in item:
                    value = item[key]
                    if isinstance(value, np.ndarray) and value.shape == (1, 1):
                        value = value[0][0]
                    values.append(value)
            setattr(self, key, values)

    def attributes(self):
        """
        Returns a list of all accessible attributes in the class
        """

        attribute_list = [key for key in self.__dict__.keys() if not key.startswith('__')]
        return attribute_list

    def display(self):
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")

    
    def __repr__(self):
        """
        Displays a list of all accessible attributes in the class

        """
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key in self.raw_data[0].keys())
        return f"\nResults:\n--------- \n{attributes}\n--------- "


    def head(self):
        """
        Returns a printout summary of basic yhat_details values

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


    def lin_comp(self, y_actuals):
        """Generates a summary of the influence of linear and non linear components
        in the prediction results

        Args:
            y_actuals (pandas series): Pandas series of correct prediction results 
                extracted from initial dataset to assess accuracy of the predictions
        """


        data = summary.rbp_linear_component(self.y_linear, self.yhat, y_actuals)
        print("Linear component analysis: \n", data)
    

    def save_results_to_vault(self, X, y, theta, metadata:VaultMetadata, options:PredictionOptions, db_username:str, db_password:str):
        """Saves experiment data to the vault_results database along with Metadata
        needed to display the raw information

        Args:
            X (np.ndarray, pd.Series or list): X input that was used to generate prediction results
            y (np.ndarray, pd.Series or list): y input that was used to generate prediction results
            theta (np.ndarray, pd.Series or list): theta matrix input that was used to generate prediction results
            metadata (VaultMetadata): Supporting information to make prediction data readable
            options (PredictionOptions): Optional parameter inputted into the prediction model
            db_username (str): Username used to access csa database
            db_password (str): Password used to access csa database
        """


        # Establish a connection with the database
        connection = connect(db_username, db_password)

        foreign_keys = vault_upload.post_vault_metadata(connection=connection, X=X, y=y, metadata=metadata)

        resp = vault_upload.post_vault_results(connection=connection, results=self.raw_data, options=class_obj_to_dict(options),
                                              foreign_keys = foreign_keys, metadata=class_obj_to_dict(metadata), theta=theta)


        print(resp)