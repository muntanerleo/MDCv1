# Medical Data Connections (MDC) v1

A comprehensive data processing pipeline for standardizing and connecting pharmaceutical and medical data sources.

## Overview

MDC is designed to process, clean, and standardize medical data with a focus on:
- Drug information and classifications
- Generic drug names and alternatives
- Side effects and usage information
- Drug state tracking
- Habit-forming drug identification

## Features

- Data standardization and cleaning
- Text normalization for medical terms
- Multiple-source data integration
- FDA API data integration
- Comprehensive drug name mapping
- Drug classification hierarchy

## Data Processing Pipeline

1. Raw Data Ingestion
   - Reads source data from CSV files
   - Integrates FDA API data
   - Initial validation checks

2. Data Transformation
   - Text standardization
   - Unit normalization
   - Format consistency
   - Special character handling

3. Data Organization
   - Drug mapping
   - Generic name associations
   - Side effect categorization

## Requirements

- Python 3.x
- Pandas
- Jupyter Notebook
- FDA API access (for certain features)

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MDCv1.git
cd MDCv1
```


## Documentation
Detailed documentation for each component can be found in the respective notebook files:
- notebooks/try_transform.ipynb: Main data transformation pipeline
- notebooks/fda_api_eda.ipynb: FDA API integration and analysis

## Contact
muntanerleo@gmail.com