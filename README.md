# Cambridge Sports Analytics Common Library

The **CSA Common Lib** is a shared library designed to provide utility modules, class definitions, enumerations, and helper functions for the **CSA Prediction Engine** package. It standardizes and simplifies complex operations across different parts of the system.

## Package Structure

The package is structured as follows:

```plaintext
csa_common_lib/
├── classes/
   ├── prediction_options.py       # Configurations and options for predictions
   ├── prediction_receipt.py       # Structures data for prediction receipts
   └── prediction_results.py       # Handles and organizes prediction results

├── enum_types/
   ├── exit_flags.py               # Execution exit flag states
   ├── functions.py                # Enumerates system functions
   └── job_types.py                # Defines job types for concurrency management

├── helpers/
   ├── _arrays.py                  # Array manipulation and utility functions
   ├── _conversions.py             # Data type conversion utilities
   └── _os.py                      # Operating system interaction functions

└── toolbox/
    ├── classes/
       └── utilities.py            # Utility functions for working with classes
    
    ├── concurrency/
       ├── parallel_executor.py    # Parallel execution tools
       └── parallel_helpers.py     # Helper functions for concurrency
     
    ├── database/
       └── information.py          # Database utility and information tools
     
    ├── npz/
       └── io_operations.py        # NPZ file input/output utilities
     
    └── stats/
       └──                         # Statistical computation tools and functions
```

## Installation

To install this package as part of the CSA environment, use:

```bash
pip install csa_common_lib
```

## Usage

Here’s an example of how to use the prediction class options from the common library:

```python
from csa_common_lib.classes.prediction_options import {
        PredictionOptions,
        MaxFitOptions,
        GridOptions
    }
```


## License
(c)2023-2024 Cambridge Sports Analytics, LLC. All rights reserved.
