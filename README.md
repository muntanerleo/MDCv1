# Medical Data Connections (MDCv1)

## Overview
Medical Data Connections (MDCv1) is a comprehensive platform designed to analyze and visualize medical data, specifically focusing on drug details, side effects, and therapeutic uses. The platform leverages data preprocessing, database management, and interactive dashboards to provide insights into various medications and their effects.

## Project Structure

### Main Directories
- **src/**: Contains the main source code for the project.
  - **dashboard/**: Modules related to the dashboard components.
    - `main.py`: Main logic for the Streamlit dashboard.
  - **db/**: Modules for data handling.
    - `database.py`: Database connection logic.
    - `preprocessing.py`: Data preprocessing functions.
  - **utils/**: Utility functions.
    - `viz_utils.py`: Reusable visualization helpers.

- **notebooks/**: Jupyter notebooks for data exploration and analysis.
  - `preprocess_analysis.ipynb`: Notebook for preprocessing and analyzing drug data.

- **docs/**: Documentation files.
  - `DATASET_INFO.md`: Information about the dataset used.

- **tests/**: Unit and integration tests.
  - `test_database.py`: Tests for database connections.
  - `test_preprocessing.py`: Tests for data preprocessing functions.

### Key Files
- **app.py**: Main entry point for the Streamlit application.
- **requirements.txt**: Production dependencies.
- **setup.py**: Package configuration.
- **.gitignore**: Git ignore file.

## Getting Started
1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/MDCv1.git
   cd MDCv1

## Install dependencies:
2. **Install requirements**:
   ```sh
   pip install -r requirements.txt

## Run the application:
3. **Try running the Streamlit app**:
   ```sh
   streamlit run app.py

### Contact
For any inquiries or contributions, please contact the project maintainer at muntanerleo@gmail.com