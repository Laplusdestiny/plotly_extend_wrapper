# encoding: utf-8
# Author: Laplusdestiny <prayonshootingstars@gmail.com>
# Copyright (c) 2023-2023 Laplusdestiny
# License: MIT

from setuptools import setup
import plotly_extend_wrapper

DESCRIPTION = "plotly-extend-wrapper: Extended Python library for Plotly"
NAME = "plotly-extend-wrapper"
AUTHOR = "Laplusdestiny"
AUTHOR_EMAIL = "prayonshootingstars@gmail.com"
URL = "https://github.com/Laplusdestiny/plotly_extend_wrapper"
LICENSE = "MIT"
DOWNLOAD_URL = "https://github.com/Laplusdestiny/plotly_extend_wrapper"
VERSION = plotly_extend_wrapper.__version__
PYTHON_REQUIRES = ">=3.7"

INSTALL_REQUIRES = [
    "plotly>=5.0.0",
    "kaleido==0.2.1",
    "pandas>=1.1.5"

]
PACKAGES = [
    "plotly_extend_wrapper"
]
CLASSIFIERS = [

]

with open("README.md", "r") as fp:
    readme = fp.read()

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    README=readme,
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    classifiers=CLASSIFIERS
)
