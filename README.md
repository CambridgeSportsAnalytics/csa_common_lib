# CSA Common Library
[![PyPI version](https://img.shields.io/pypi/v/csa-common-lib.svg)](https://pypi.org/project/csa-common-lib/)
[![Python Version](https://img.shields.io/badge/python-%20v3.11-blue)](https://github.com/CambridgeSportsAnalytics/csa_common_lib)
[![CodeFactor](https://www.codefactor.io/repository/github/cambridgesportsanalytics/csa_common_lib/badge)](https://www.codefactor.io/repository/github/cambridgesportsanalytics/csa_common_lib)

The **CSA Common Library** is a shared Python package that provides utility classes, enums, helper functions, and parallel processing tools used across the Cambridge Sports Analytics prediction ecosystem.

It serves as the foundation for [`csa_prediction_engine`](https://github.com/CambridgeSportsAnalytics/csa_prediction_engine), offering standardized structures and operations for job execution, result handling, configuration, and concurrency.

## 🧱 Package Structure

```bash
csa_common_lib/
├── classes/                      # Core data models and result containers
│   ├── float32_encoder.py        # Optimized encoder for float32 serialization
│   ├── prediction_options.py     # Configuration objects for prediction jobs
│   ├── prediction_receipt.py     # Receipt structure for submitted tasks
│   └── prediction_results.py     # Interfaces for organizing prediction outputs
│
├── enum_types/                   # Enumerations for function types, job control, and result metadata
│   ├── errors.py                 # Lambda error codes and messages
│   ├── exit_flags.py             # Execution exit status indicators
│   ├── functions.py              # Function type identifiers
│   ├── job_types.py              # Job types for task routing
│   ├── lambda_status.py          # Lambda execution status codes
│   └── results.py                # Keys and categories for result objects
│
├── helpers/                      # Internal utility modules
│   ├── _arrays.py                # Array manipulation and reshaping
│   ├── _conversions.py           # Type and structure conversions
│   ├── _os.py                    # OS-level interactions
│   └── _vault.py                 # Tools for interfacing with the Prediction Vault
│
├── toolbox/                      # Utilities for parallelism, data I/O, and statistical helpers
│   ├── classes/                  # Class-level utilities
│   ├── concurrency/              # Parallel execution and thread helpers
│   ├── database/                 # Lightweight DB information tools
│   ├── npz/                      # NPZ file I/O utilities
│   └── stats/                    # Statistical computation modules (in progress)
│
└── __init__.py                   # Package initializer
```

## 📦 Installation

Install via PypI:

```bash
pip install csa-common-lib
```
Requires Python 3.11.

## 🧪 Example Usage

Here’s an example of how to use the prediction class options from the common library:

```python
from csa_common_lib.classes.prediction_options import {
        PredictionOptions,
        MaxFitOptions,
        GridOptions
    }
```
For usage examples and integration, see the
👉 [csa_prediction_engine](https://github.com/CambridgeSportsAnalytics/csa_prediction_engine) package.

## 🤝 Contributing

Bug reports and feature requests are welcome. Reach out to our team 📧 support@csanalytics.io

## ⚖️ License
Copyright (c) 2023-2025 Cambridge Prediction Analytics, LLC. All rights reserved.
