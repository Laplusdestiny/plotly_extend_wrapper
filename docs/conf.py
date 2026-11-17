# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'plotly-extend-wrapper'
copyright = '2024-2026, Laplusdestiny'
author = 'Laplusdestiny'

import re
import sys
from pathlib import Path

# Make the package importable for autodoc without installing it
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Single source of truth for the version is pyproject.toml
_pyproject = (Path(__file__).resolve().parent.parent / "pyproject.toml").read_text(encoding="utf-8")
version = re.search(r'^version\s*=\s*"([^"]+)"', _pyproject, re.MULTILINE).group(1)
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',  # add .nojekyll so that _static/ is served
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# -- API reference (generated from docstrings) -------------------------------
# The API reference pages only contain ``automodule`` directives, so the
# docstrings in the source code are the single source of truth.
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__call__',
}
# Type hints are written in the numpy-style docstrings; hide raw annotations
# such as ``Union[pd.DataFrame, 'pl.DataFrame', 'pl.LazyFrame']`` in signatures.
autodoc_typehints = 'none'
# Show ``Plot_line(...)`` instead of ``plotly_extend_wrapper.wrapper.Plot_line(...)``
add_module_names = False
autosummary_generate = False
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_rtype = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
# html_static_path = ['_static']
