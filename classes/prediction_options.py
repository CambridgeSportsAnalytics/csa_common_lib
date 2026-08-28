import copy
import numpy as np
from random import getrandbits

from csa_common_lib.enum_types.missing_moments import MissingMoments

# Accepted on construction / clone_with / init_from_dict, then folded into
# missing_moments. Not stored in options after normalize.
_MISSING_MOMENTS_ALIAS = "verify_missing_data"


# Grid object keys valid for _retain_grid_objects when passed as a list.
# Used for validation to catch typos early.
VALID_RETAIN_KEYS = frozenset({
    'yhat_cells', 'adjusted_fit_cells', 'n_cells', 'weights_cells',
    'k_cells', 'combi_cells', 'ysolo_distribution', 'ysolo_cells',
})


def _parse_bool_flag(value, name="flag"):
    """Parse a bool from bool / 0/1 / true-false strings."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, np.integer)) and value in (0, 1):
        return bool(value)
    s = str(value).strip().lower()
    if s in ("true", "1", "yes", "on"):
        return True
    if s in ("false", "0", "no", "off"):
        return False
    raise ValueError(f"{name} must be true/false; got {value!r}")


class _OptionsMeta(type):
    """Internal Metaclass for preventing incorrect attribute references on Options classes"""

    def __init__(cls, name, bases, dct):
        if not hasattr(cls, '_allowed_keys'):
            cls._allowed_keys = set([])  # Initialize as an empty set if not defined
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        extra_keys = kwargs.keys() - cls._allowed_keys # Extra keys that don't belong. Ie. Mistaken attributes
        if extra_keys:
            # Throw error and list invalid keys for user to correct
            raise AttributeError(f"Invalid class attribute(s): {extra_keys}. Allowed keys are: {cls._allowed_keys}")
        if hasattr(instance, "_normalize_missing_moments"):
            instance._normalize_missing_moments()
        return instance
    

class PredictionOptions(metaclass=_OptionsMeta):
    """A configurable options class for relevance-based predictions, including
    predict, maxfit, and grid models. This class provides a comprehensive 
    list of all possible input parameters, ensuring flexibility across 
    different prediction models. While some parameters are shared across 
    inherrited models, setting an unused option for a specific model 
    will have no effect, ensuring compatibility and ease of use.
    
    threshold : float or ndarray [1-by-T], optional (default=None)
        Evaluation threshold to determine whether observations will be 
        included or excluded from the censor function in the 
        partial-sample regression. If threshold = None, the model 
        will evaluate across thresholds from [0, 0.90) in 0.10 increments.
    is_threshold_percent : bool, optional (default=True)
        Specify whether threshold is in percentage (decimal) units.
    most_eval : bool, optional (default=True)
        Specify the direction of the censor evaluation of the threshold.
        True:  [eval_type] score > threshold
        False: [eval_type] score < threshold
    eval_type : str, optional (default="both")
        Specify evaluation censor type, relevance, similarity, or both.
    adj_fit_multiplier : str, optional (default='K')
        Adjusted fit multiplier. Specify either 'log', 'K', or '1'.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.
    missing_moments : {"pairwise", "complete"} or MissingMoments, optional
        How μ, Σ, and PSR N treat NaNs. Does **not** drop the row from ŷ
        (incomplete X rows still get weight 0). Default ``"pairwise"``.
        ``"complete"`` is listwise complete-case (MATLAB ``'complete'``).
    verify_missing_data : bool, optional
        Deprecated alias: ``True`` → ``missing_moments="complete"``,
        ``False`` leaves ``missing_moments`` as given (default pairwise).
    inv_method : str, optional (default='gaussian')
        Method to use for inverse covariance matrix.
    _output_scale : str, optional (default='default')
        Scale of the returned prediction. ``default`` is the response
        (linear) scale. ``logistic`` maps the finished composite ŷ
        through Chapter 4 once (mix on the response scale, then map).
        Inner grid and maxfit cells always stay on the response scale.

    Returns
    -------
    PredictionsOptions
        Options class to organize and persist parameters used in the
        the prediction models.

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the options dictionary.
    """

    def __init__(self, **kwargs):

        self.options = {
            'threshold': [0.5],
            'is_threshold_percent': True,
            'most_eval': True,
            'eval_type': 'both',
            'adj_fit_multiplier': 'K',
            'cov_inv': None,
            'missing_moments': MissingMoments.PAIRWISE,
            'inv_method':'gaussian',
            '_output_scale': 'default'
        }

        self.__class__._allowed_keys = set(self.options.keys()) | {_MISSING_MOMENTS_ALIAS}

        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)


    def _normalize_missing_moments(self):
        """Fold verify_missing_data into missing_moments; store the enum.

        ``verify_missing_data=True`` forces complete (same as Rust FFI).
        ``False`` leaves ``missing_moments`` as given.
        """
        opts = self.options
        alias = opts.pop(_MISSING_MOMENTS_ALIAS, None)
        raw = opts.get("missing_moments", MissingMoments.PAIRWISE)
        if alias is None:
            opts["missing_moments"] = MissingMoments.parse(raw)
            return
        if MissingMoments.parse(alias) is MissingMoments.COMPLETE:
            opts["missing_moments"] = MissingMoments.COMPLETE
        else:
            opts["missing_moments"] = MissingMoments.parse(raw)

    def __getattr__(self, name):
        # Avoid recursion by checking if the attribute is already present in __dict__
        if name in self.__dict__:
            return self.__dict__[name]

        if name == _MISSING_MOMENTS_ALIAS and "options" in self.__dict__:
            mm = self.__dict__["options"].get("missing_moments", MissingMoments.PAIRWISE)
            return MissingMoments.parse(mm).drop_na()

        # Check if 'options' is in self.__dict__ to avoid KeyError
        if 'options' in self.__dict__ and name in self.__dict__['options']:
            return self.__dict__['options'][name]

        # Raise an AttributeError if the attribute is not found
        raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")


    def __setattr__(self, name, value):
        if name == "options":
            super().__setattr__(name, value)
        elif name == _MISSING_MOMENTS_ALIAS and "options" in self.__dict__:
            self.options["missing_moments"] = (
                MissingMoments.COMPLETE if value else MissingMoments.PAIRWISE
            )
        elif name == "missing_moments" and "options" in self.__dict__:
            self.options["missing_moments"] = MissingMoments.parse(value)
        elif name == "adjust_impact_for_missing" and "options" in self.__dict__:
            self.options["adjust_impact_for_missing"] = _parse_bool_flag(
                value, name="adjust_impact_for_missing"
            )
        elif 'options' in self.__dict__ and name in self.options:
            self.options[name] = value
        else:
            raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")


    def display(self):
        for key, value in self.options.items():
            print(f"{key}: {value}")



    def init_from_dict(self, inputs):
        """ Accepts a dictionary of inputs and returns a 
        PredictionOptions object updated with all passed optional values. 
        Essentially, this is an update method.

        Args:
            inputs (dict): Intakes a dictionary of inputs deconstructed 
            in an AWS Lambda function.

        Returns:
            PredictionOptions: PredictionOptions obj that 
            holds all passed optional values. Non-passed options 
            remain default setting
        """

        
        # Iterate through input dict key/value pairs
        for key, value in inputs.items():
            if key in self.__class__._allowed_keys:
                setattr(self, key, value)


    def clone_with(self, **kwargs):
        """ Returns a clone of the passed PredictionOptions object 
        with user-specified attribute overwrites (via key value pairs)

        Args:
            key/value pair (attr/value): Attributes to overwrite in 
            the cloned object lambda function

        Returns:
            PredictionOptions: PredictionOptions obj 
        """
        
         # Create a new instance of PredictionOptions to avoid recursive loop in .deepcopy()
        new_copy = self.__class__()

        # Copy attributes from the original instance to the new instance
        for attr, value in self.__dict__.items():
            setattr(new_copy, attr, copy.deepcopy(value))

        # Overwrite attributes with passed parameter
        for key, value in kwargs.items():
            setattr(new_copy, key, value)

        return new_copy


class MaxFitOptions(PredictionOptions):
    """
    MaxFitOptions Class:
    Inherits from PredictionOptions and adds additional options specific
    max fit problems.
    
    threshold : not applicable
        Max fit solves for the optimal threshold that maximizes the 
        fit (or adjusted fit) value, by default [0.0, 0.2, 0.5, 0.8].
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation on the censor score.
        The censor score is determined by eval_type.
        True:  censor score > threshold
        False: censor score < threshold
    eval_type : str, optional (default="both")
        Specify censor threshold type, relevance, similarity, or both.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.
    objective : str, optional (default="adjusted_fit)
        Objective function to optimize, either fit or adjusted_fit.
    
    Returns
    -------
    MaxFitOptions
        Options class to organize and persist parameters used for the
        maximum fit prediction model.

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the options dictionary.        
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        maxfit_options = {
            'threshold': np.array([0.0, 0.2, 0.5, 0.8]),
            'objective': 'kfit',
            }
        
        self.__class__._allowed_keys = self.__class__._allowed_keys.union(
            maxfit_options.keys()
        ) | {_MISSING_MOMENTS_ALIAS}

        self.options.update(maxfit_options)
        
        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)


class GridOptions(MaxFitOptions):
    """
    GridOptions Class:
    Inherits from MaxFitOptions and adds additional options.
    
    threshold : ndarray
        Vector of threshold values to evaluate, 
        by default [0.0, 0.2, 0.5, 0.8]
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation on the censor score.
        The censor score is determined by eval_type.
        True:  censor score > threshold
        False: censor score < threshold
    eval_type : str, optional (default="both")
        Specify censor threshold type, relevance, similarity, or both.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.
    objective : str, optional (default="adjusted_fit)
        Objective function to optimize, either fit or adjusted_fit.
    attribute_combi : ndarray [Q-by-K], optional (default=None)
        Matrix of binary row vectors to indicate variable choices.
        Each row is a combination of variables to evaluate.
        If not specified, function will evaluate all possible combinations.
    max_iter : int, optional (default=1_000_000)
        Maximum number of grid cells to evaluate. Since this is a O(n^K)
        computational time, we suggest balancing computation time
        and memory with the maximum number of cells to evaluate.
    k : int, optional (default=1)
        Lower bound for the number of variables to include for any 
        combination Q, by default 1.
    adjust_impact_for_missing : bool, optional (default=True)
        Incomplete-column IOF / IOP vs an uninformative include-k null
        with the same missingness, mean, and sd as column k (NaNs kept).
        Off is the pre-adjustment baseline. Complete columns, composite
        yhat, fit, variable weights, and CCTP are unchanged.
    _retain_grid_objects : bool, list of str, or None, optional (default=False)
        Controls which grid objects to retain. True retains all; False or None
        retains none; list retains only the specified keys (see VALID_RETAIN_KEYS).
        
    Returns
    -------
    GridOptions
        Options class to organize and persist parameters used for the
        grid (and grid singularity) prediction model.

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the options dictionary.      
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        grid_options = {
                        'attribute_combi': None,
                        'max_iter': 1_000,
                        'k': 1,
                        'adjust_impact_for_missing': True,
                        '_retain_grid_objects': False,
                        '_seed': getrandbits(32) # initialize for combi
                    }
        
        self.__class__._allowed_keys = self.__class__._allowed_keys.union(
            grid_options.keys()
        ) | {_MISSING_MOMENTS_ALIAS}

        self.options.update(grid_options)
        
        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)
        self.options['adjust_impact_for_missing'] = _parse_bool_flag(
            self.options.get('adjust_impact_for_missing', True),
            name='adjust_impact_for_missing',
        )