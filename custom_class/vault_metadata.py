import numpy as np
import pandas as pd

from csanalytics_local.db_local.controller import connect
from csanalytics_local.db_local.vault_commands import get_ids_by_names



class VaultMetadata:
    """
    Vault Metadata Class:
    Supports a master default list of all possible metadata used in the vault.

    See documentation for option definitions: {put gitbook link here}
    """

    def __init__(self, **kwargs):
        self.metadata = {
            'y_metric': None,
            'product_id': None,
            'Xcol_labels': None,
            'Xrow_labels': None,
            'outcome_labels': None,
            'experiment_title': '',
            'experiment_description': '',
            'img_urls': None,
            'outcome_info': None
        }
            
        # Update attributes with any provided kwargs
        if kwargs:
            for key, value in kwargs.items():
                # Convert any pandas references in a list we can parse
                if isinstance(value, pd.Series):
                    value = value.tolist()

                self.__setattr__(key, value)


    def __getattr__(self, name):
        if name in self.metadata:
            return self.metadata[name]
        raise AttributeError(f"'VaultMetadata' object has no attribute '{name}'")


    def __setattr__(self, name, value):
        if name == "metadata":
            super().__setattr__(name, value)
        elif name in self.metadata:
            self.metadata[name] = value
        else:
            raise AttributeError(f"'VaultMetadata' object has no attribute '{name}'")


    def display(self):
        for key, value in self._metadata.items():
            print(f"{key}: {value}")


    def init_from_dict(self, inputs):
        """ Accepts a dictionary of inputs and returns a VaultMetadata obj 
        updated with all passed optional values

        Args:
            inputs (dict): Intakes a dictionary of inputs deconstructed in the 
            lambda function

        Returns:
            VaultMetadata:  VaultMetadata obj that holds all passed optional values. Non-passed options remain default setting
        """
        # Iterate through input dict key/value pairs
        for key, value in inputs.items():
            # If obj attribute matches key in input dict
            if hasattr(self, key):
                # Update corresponding attribute in options object to hold dictionary value
                setattr(self, key, value)


    def update_fields(self, field_list):
        """ Update the metadata fields dynamically based on the provided field list.

        Args:
            field_list (list): List of field names to update the metadata structure.
        """

        
        current_keys = set(self.metadata.keys())
        new_keys = set(field_list)

        # Remove keys that are no longer in the field list
        for key in current_keys - new_keys:
            del self.metadata[key]

        # Add new keys that are not in the current metadata
        for key in new_keys - current_keys:
            self.metadata[key] = None

        # Ensure all attributes are updated
        for key in self.metadata.keys():
            setattr(self, key, self.metadata[key])

    