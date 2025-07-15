# CSA Common Library
[![PyPI version](https://img.shields.io/pypi/v/csa-common-lib.svg)](https://pypi.org/project/csa-common-lib/)
[![Python Version](https://img.shields.io/badge/python-%20v3.11-blue)](https://github.com/CambridgeSportsAnalytics/csa_common_lib)

The **CSA Common Library** is a shared Python package that provides utility classes, enums, helper functions, and parallel processing tools used across the Cambridge Sports Analytics prediction ecosystem.

It serves as the foundation for [`csa_prediction_engine`](https://github.com/CambridgeSportsAnalytics/csa_prediction_engine), offering standardized structures and operations for job execution, result handling, configuration, and concurrency.

## 🧱 Package Structure

```bash
.
├── classes/                      # Core data classes and result structures
│  ├── float32_encoder.py
│  ├── prediction_options.py
│  ├── prediction_receipt.py
│  └── prediction_results.py
├── enum_types/                   # Enumerations for flags, job types, functions, and results
│  ├── errors.py
│  ├── exit_flags.py
│  ├── functions.py
│  ├── job_types.py
│  ├── lambda_status.py
│  └── results.py
├── helpers/                      # Low-level helper modules
│  ├── _arrays.py
│  ├── _conversions.py
│  ├── _os.py
│  └── _vault.py
├── toolbox/                      # Utility modules for classes, concurrency, file I/O, and stats
│  ├── classes/
│  ├── concurrency/
│  ├── database/
│  ├── npz/
│  └── stats/
└── __init__.py                   # Package initialization_init__.py                  # Package initialization
```

## 📦 Installation

Install via PypI:

```bash
pip install csa_common_lib
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
(c)2023-2025 Cambridge Sports Analytics, LLC. All rights reserved.
