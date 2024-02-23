

from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Qvalidate'
LONG_DESCRIPTION = 'A package to find area of different figures'


# Setting up
setup(
    name="qvalidate",
    version=VERSION,
    author="SAG",
    author_email="chiragb@quinnox.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
    ],
    keywords=['python', 'validation', 'ETL'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

