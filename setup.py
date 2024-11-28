from setuptools import setup, find_packages

setup(
    name="medication-dashboard",
    version="0.1.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'streamlit',
        'pandas',
        'plotly',
        'sqlalchemy',
        'psycopg2-binary',
        'python-dotenv'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'mypy'
        ]
    },
    author="Leonardo Muntaner",
    description="Medication Dashboard Streamlit Application",
    long_description=open('docs/README.md').read(),
    long_description_content_type="text/markdown",
)