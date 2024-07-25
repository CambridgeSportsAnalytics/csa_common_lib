import numpy as np
import pandas as pd

from csanalytics_local.db_local.controller import connect
from csanalytics_local import vault_upload

from csa_common_lib.toolbox.stats import summary
from csa_common_lib.custom_class.vault_metadata import VaultMetadata
from csa_common_lib.custom_class.prediction_options import PredictionOptions
from csa_common_lib.toolbox.classes.class_utils import class_obj_to_dict
from csa_common_lib.toolbox.stats.stats_to_excel import create_excel_sheet


class PredictionResults:
    """
    Prediction Results Class:
    Stores an array of dictionaries containing prediction results,
    filters specific attributes into their respective arrays.
    """

    def __init__(self, results):
        self.raw_data = results
        self._initialize_attributes()
        self.weights_concentration = [np.std(row) for row in self.weights]


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

        
        df = pd.DataFrame(X)
        rel_weights = df.apply(lambda row: row.nlargest(5).index.tolist(), axis=1)

        self.relevant_weights = [[metadata.Xrow_labels[i] for i in row_indices] for row_indices in rel_weights]

        matrices = self.combi_compound
        top_labels_all_matrices = []
        for matrix in matrices:
            df_row = pd.Series(matrix[0])
            top_indices = df_row.nlargest(5).index.tolist()
            top_labels = [metadata.Xcol_labels[i] for i in top_indices]
            top_labels_all_matrices.append(top_labels)

        self.variable_importance = top_labels_all_matrices
        
        # Establish a connection with the database
        connection = connect(db_username, db_password)

        foreign_keys = vault_upload.post_vault_metadata(connection=connection, X=X, y=y, metadata=metadata)

        resp = vault_upload.post_vault_results(connection=connection, results=self, options=class_obj_to_dict(options),
                                              foreign_keys = foreign_keys, metadata=class_obj_to_dict(metadata), theta=theta)


        print(resp)



    
        
    def model_analysis(self, y_actuals, X_cols):
        """Prints and returns tables of summary statistics of a given set of PredictionResults

        Args:
            y_actuals (pd.Series): Actual values (to be compared to yhats)
            X_cols (list): Array of variable (column) names

        Returns:
            analysis_list : Array of model_analysis tables 
                (y Actual Mean, Informativeness Weighted Co-occurence, Linear Component Analysis, Variable Importance)
        """

        if not hasattr(self, 'combi_compound'):
            raise Exception("Attribute: combi_compound required to model analysis results.\nPlease set is_return_grid=True in your prediction options")

        # Run analysis
        analysis_list = summary.model_analysis(yhats=self.yhat, y_actuals=y_actuals, y_linear=self.y_linear,
                               fits=self.fit, combi_compound=self.combi_compound, X_cols=X_cols)
        
        analysis_names = ["y Actual Mean: \n","Informativeness Weighted Co-occurence: \n",
                          "Linear Component Analysis: \n","Variable Importance: \n"]

        # Printout summary
        index = 0

        print("--------------\nSUMMARY STATS: \n")
        for analysis in analysis_list:
            print(analysis_names[index])
            print(analysis)
            index += 1
            print("\n")
        print("--------------")

        # Return list of pandas tables containing summary data. *Not required to see stats
        return analysis_list
    

    def save_to_excel(self, y_actuals, X_cols, outcome_labels, filepath:str):

        if not hasattr(self, 'combi_compound'):
            raise Exception("Attribute: combi_compound required to model analysis results.\nPlease set is_return_grid=True in your prediction options")

        # Run analysis
        analysis_list = summary.model_analysis(yhats=self.yhat, y_actuals=y_actuals, y_linear=self.y_linear,
                               fits=self.fit, combi_compound=self.combi_compound, X_cols=X_cols)
        
        create_excel_sheet.generate_workbook(analysis_list, result_path=filepath,
                                              PredictionResults=self, X_cols=X_cols,
                                              test_set_names=outcome_labels,y_actuals=y_actuals)
        
