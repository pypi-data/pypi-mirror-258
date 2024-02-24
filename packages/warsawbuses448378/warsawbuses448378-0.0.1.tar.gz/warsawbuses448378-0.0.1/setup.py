from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Analysing buses traffic in Warsaw'

# Setting up
setup(
    name="warsawbuses448378",
    version=VERSION,
    author="Michal Nowicki ",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pandas', 'warsaw_data_api', 'shapely'],
    keywords=['python', 'bus'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)