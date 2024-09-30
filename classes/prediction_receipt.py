import numpy as np
import pickle
import json
import uuid
from datetime import datetime
from psr_lambda._private._helpers import calc_crc64
from csanalytics_local.vault_upload.post_vault_results import convert_ndarray_to_list

class PredictionReceipt:
    """Saves and orgnaizes input dimensions, prediction durations, 
    timestamps, input options and more. This is meant to assist in
    the validation process of prediction results. 

    
    Returns
    -------
    PredictionReceipt
        Receipt class to store and persist information that is relavant
        to cross checking prediction requests

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the receipt dictionary.
    """

    def __init__(self, model_type, y, X, theta, options, yhat, prediction_duration=None):
        self.prediction_id = str(uuid.uuid4()) # Unique id for the prediction request
        self.timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Timestamp of the receipt
        self.prediction_duration =  round(prediction_duration, 3) # Time to run a prediction (in seconds) 
        self.model_type = str(model_type) # Prediction model that was run
        self.X_dim = X.shape  # Save input dimensions
        self.y_dim = y.shape  # Save input dimensions
        self.theta_dim = theta.shape  # Save input dimensions
        self.options = convert_ndarray_to_list(options.options) # Save input options
        self.yhat = yhat # Save output info
        self.y_checksum = calc_crc64(pickle.dumps(y)) # convert y to bytes and get checksum
        self.X_checksum = calc_crc64(pickle.dumps(X)) # convert X to bytes and get checksum
        self.theta_checksum = calc_crc64(pickle.dumps(theta)) # convert theta to bytes and get checksum

    def basic_display(self):
        """Displays basic validation info. Excludes lengthy results objects
        """        
        attributes = dir(self)
        remove_attributes = ['options', 'yhat']

        print("\nBasic Display (Call PredictionReceipt.full_display() to see more)\n")
        attributes = [attr for attr in attributes if attr not in remove_attributes]


        for attr in attributes:
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")
        

    def full_display(self):
        """Displays all validation info
        """

        attributes = dir(self)
        remove_attributes = ['options']

        print("\nFull Display\n")
        attributes = [attr for attr in attributes if attr not in remove_attributes]
        for attr in attributes:
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")

        print("\n Input Options: \n")
        self.options.display()
    

    def save_receipt(self):
        """Saves prediction_receipts as json in the local directory. Will 
        change this soon
        """

        # Convert any nd.arrays to lists (to be json serializable)
        for attr in dir(self):
            attr_value = getattr(self, attr)
            if isinstance(attr_value, np.ndarray):
                setattr(self, attr, attr_value.tolist())

        
        # Turn receipt object into dictionary so that it can be saved as a json file
        obj_dict = self.__dict__

        # Convert timestamp to filename
        timestamp = self.timestamp.replace(" ", "_").replace(":", "-")
        # Save to a JSON file
        with open(f'{timestamp}.json', 'w') as json_file:
            json.dump(obj_dict, json_file)