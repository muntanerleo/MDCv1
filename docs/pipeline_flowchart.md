```
medication-dashboard/
├── src/                        # Main source code directory
│   ├── init.py             # Makes src a Python package
│   ├── dashboard/              # Dashboard-specific modules
│   │   ├── init.py
│   │   ├── overview_panel.py   # Separate file for overview panel
│   │   ├── drug_comparison.py  # Drug comparison panel logic
│   │   ├── safety_analysis.py  # Safety analysis panel
│   │   └── administration.py   # Administration panel
│   │
│   ├── data/                   # Data handling modules
│   │   ├── init.py
│   │   ├── database.py         # Database connection logic
│   │   └── preprocessing.py    # Data preprocessing functions
│   │
│   └── utils/                  # Utility functions
│       ├── init.py
│       ├── visualizations.py   # Reusable visualization helpers
│       └── config.py           # Configuration management
│
├── tests/                      # Unit and integration tests
│   ├── init.py
│   ├── test_database.py        # Database connection tests
│   ├── test_preprocessing.py   # Data preprocessing tests
│   └── test_dashboard.py       # Dashboard component tests
│
├── notebooks/                  # Jupyter notebooks for exploration
│   ├── data_exploration.ipynb
│   └── analysis_notes.ipynb
│
├── config/                     # Configuration files
│   ├── .env                    # Environment variables
│   └── logging.yaml            # Logging configuration
│
├── scripts/                    # Utility scripts
│   ├── data_import.py          # Data import/migration scripts
│   └── database_setup.py       # Database initialization
│
├── docs/                       # Documentation
│   ├── README.md               # Project overview
│   └── architecture.md         # System design details
│
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Package configuration
├── pyproject.toml              # Modern Python project configuration
├── .gitignore                  # Git ignore file
├── .env.example                # Template for environment variables
└── app.py                      # Main Streamlit application entry point
```