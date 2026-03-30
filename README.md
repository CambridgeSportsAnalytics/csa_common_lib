# Cambridge Sports Analytics Common Library

[![PyPI version](https://img.shields.io/pypi/v/csa-common-lib.svg)](https://pypi.org/project/csa-common-lib/)
[![Python Version](https://img.shields.io/badge/python-%20v3.11-blue)](https://github.com/CambridgeSportsAnalytics/csa_common_lib)
[![CodeFactor](https://www.codefactor.io/repository/github/cambridgesportsanalytics/csa_common_lib/badge)](https://www.codefactor.io/repository/github/cambridgesportsanalytics/csa_common_lib)

`csa_common_lib` is a shared library that provides utility modules, class definitions, enumerations, and helper functions for the CSA Prediction Engine Python client. It standardizes and simplifies complex operations across the system.

## Installation

Install from PyPI:

```bash
pip install csa-common-lib
```

Requires Python 3.11.

## Package layout

```text
csa_common_lib/
├── classes/
│   ├── float32_encoder.py      # Float32 serialization helpers
│   ├── prediction_options.py   # Prediction, MaxFit, and grid option objects
│   ├── prediction_receipt.py   # Task receipt structures
│   └── prediction_results.py   # Prediction result containers
├── enum_types/
│   ├── errors.py               # Lambda error codes
│   ├── exit_flags.py           # Execution exit flags
│   ├── functions.py            # Function type identifiers
│   ├── job_types.py            # Job routing types
│   ├── lambda_status.py        # Lambda status codes
│   └── results.py              # Result keys and categories
├── helpers/
│   ├── _arrays.py              # Array utilities
│   ├── _conversions.py         # Data conversions
│   ├── _os.py                  # OS helpers
│   └── _vault.py               # Prediction Vault helpers
├── toolbox/
│   ├── _validate.py            # Shared validation helpers
│   ├── _notifier.py            # Notification helpers
│   ├── classes/                # Class-level utilities
│   ├── concurrency/            # Parallel execution helpers
│   ├── database/               # Lightweight DB utilities
│   └── npz/                    # NPZ I/O
└── __init__.py
```

## Usage

Example imports for prediction configuration types:

```python
from csa_common_lib.classes.prediction_options import (
    PredictionOptions,
    MaxFitOptions,
    GridOptions,
)
```

For end-to-end API usage, see the [`csa_prediction_engine`](https://github.com/CambridgeSportsAnalytics/csa_prediction_engine) package.

## Contributing

Bug reports and feature requests are welcome. Reach out to the team at support@csanalytics.io.

## License

Copyright (c) 2023–2026 Cambridge Prediction Analytics, LLC. All rights reserved.
