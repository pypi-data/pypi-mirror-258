# Prometheux

Prometheux is a Python package designed to simplify and automate the process of rule learning from structured data, leveraging the power of the PyClause library. It provides a streamlined interface for loading datasets, executing rule learning algorithms, and managing the resulting rules, all with minimal setup required from the user.

## Features

- Easy integration with PyClause for rule learning.
- Simplified dataset loading and preprocessing.
- Automated generation of rules from structured data.
- Convenient retrieval of learned rules for analysis and application.

## Installation

Before installing Prometheux, you must ensure that PyClause is properly installed in your environment. PyClause requires a C++ (14) compiler on Linux or C++ build tools on Windows.

### Installing PyClause

1. **For Linux Users**: Ensure you have a C++ compiler installed.
2. **For Windows Users**: Ensure you have Microsoft Visual C++ 14.0 or newer installed.

To install PyClause, run the following command:

```bash
pip install git+https://github.com/symbolic-kg/PyClause.git
```

### Installing Prometheux

Prometheux requires Python 3.7 or newer. It is recommended to install Prometheux in a virtual environment to avoid conflicting with system-wide packages.

### Install with pip

To install the latest version of Prometheux, run the following command:

```pip install prometheux```


### Post-Installation

Ensure that you have a C++ compiler installed, as required by PyClause for Linux users, or C++ build tools for Windows users.

## Usage

### Loading Datasets

Specify the path to your dataset specifications in a `specs.yaml` file:

```yaml
datasets:
  - path: "/path/to/your/dataset/train.txt"
```

### Running Rule Learning

Import Prometheux and use it to load datasets and execute rule learning:

```
import prometheux as pmtx

datasets_specs = "/path/to/your/specs.yaml" 
extensional = pmtx.load(datasets_specs)
intensional = pmtx.train(extensional)
print(intensional)
```

This will print the learned rules to the console.
