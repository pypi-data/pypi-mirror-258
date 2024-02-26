
from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'add one simple'

# Setting up
setup(
    name="example_addone_v01",
    version=VERSION,
    author="matin (Florian Dedov)",
    author_email="matingottasickmind@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
