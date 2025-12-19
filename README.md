# TCGA UCEC Project

A data analysis project for The Cancer Genome Atlas (TCGA) Uterine Corpus Endometrial Carcinoma (UCEC) dataset.

## Overview

This project provides tools and scripts for downloading, preprocessing, and analyzing TCGA-UCEC data. The project includes:

- Data download utilities
- Data preprocessing pipelines
- Analysis scripts for survival analysis, differential expression, and clustering
- Documentation and usage guides

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

1. **Download data:**
   ```bash
   python scripts/download_data.py --data-type all
   ```

2. **Preprocess data:**
   ```bash
   python scripts/preprocess_data.py --input data/raw.csv --output data/processed.csv --data-type clinical
   ```

3. **Run analysis:**
   ```bash
   python scripts/analyze_data.py --input data/processed.csv --analysis-type survival
   ```

## Project Structure

```
TCGA_UCEC_project/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── docs/                  # Documentation
│   └── USAGE.md          # Detailed usage guide
├── scripts/              # Analysis scripts
│   ├── download_data.py
│   ├── preprocess_data.py
│   └── analyze_data.py
└── notebooks/            # Jupyter notebooks
```

## Documentation

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md).

## Data

The TCGA-UCEC dataset includes:
- Clinical data (patient demographics, treatment, outcomes)
- Molecular data (gene expression, mutations, copy number variations)

Data files are not included in this repository and must be downloaded separately.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided for research and educational purposes.
