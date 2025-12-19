# Usage Guide

This document provides instructions on how to use the TCGA-UCEC project scripts.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mylaila/TCGA_UCEC_project.git
cd TCGA_UCEC_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Downloading Data

To download TCGA-UCEC data:

```bash
python scripts/download_data.py --data-type all --output-dir data
```

Options:
- `--data-type`: Choose from `clinical`, `molecular`, or `all`
- `--output-dir`: Directory to save downloaded data (default: `data`)

## Preprocessing Data

To preprocess the downloaded data:

```bash
python scripts/preprocess_data.py --input data/clinical/raw_data.csv --output data/clinical/processed_data.csv --data-type clinical
```

Options:
- `--input`: Path to raw data file
- `--output`: Path for preprocessed data output
- `--data-type`: Choose from `clinical` or `molecular`

## Analysis

To perform analysis on the preprocessed data:

```bash
python scripts/analyze_data.py --input data/clinical/processed_data.csv --analysis-type survival
```

Options:
- `--input`: Path to preprocessed data
- `--analysis-type`: Choose from `survival`, `differential-expression`, or `clustering`

## Project Structure

```
TCGA_UCEC_project/
├── README.md           # Project overview
├── requirements.txt    # Python dependencies
├── docs/              # Documentation
│   └── USAGE.md       # Usage guide
├── scripts/           # Analysis scripts
│   ├── download_data.py
│   ├── preprocess_data.py
│   └── analyze_data.py
└── notebooks/         # Jupyter notebooks for exploratory analysis
```

## Notes

- Data files are not included in the repository due to size constraints
- Results and output files are excluded via .gitignore
- Refer to individual script help messages for more options: `python scripts/script_name.py --help`
