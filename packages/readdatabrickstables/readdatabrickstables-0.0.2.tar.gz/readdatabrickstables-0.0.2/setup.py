from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Databricks connectors to read tables'

# Setting up
setup(
    name="readdatabrickstables",
    version=VERSION,
    author="Mateus Esteves",
    author_email="<mestev17@its.jnj.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
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