from setuptools import setup, find_packages
from databricks import sql
import pandas as pd
import re
import time
import requests


VERSION = '0.0.5'
DESCRIPTION = 'Databricks connectors to read tables'

# Setting up
setup(
    name="readdatabrickstables",
    version=VERSION,
    author="Mateus Esteves",
    author_email="<mestev17@its.jnj.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['databricks-sql-connector==2.9.4', 'pandas', 'requests'],
    keywords=['databricks', 'pandas', 'sql', 'table', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)