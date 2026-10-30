.. plotly-extend-wrapper documentation master file, created by
   sphinx-quickstart on Fri Apr 12 16:08:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to plotly-extend-wrapper's documentation!
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/introduction
   source/wrapper
   source/updater
   source/common


=========

.. image:: https://img.shields.io/github/last-commit/Laplusdestiny/plotly_extend_wrapper?display_timestamp=author&logo=github
   :alt: GitHub last commit
   :target: https://github.com/Laplusdestiny/plotly_extend_wrapper/commits/main/

.. image:: https://img.shields.io/codecov/c/github/Laplusdestiny/plotly_extend_wrapper?style=flat&logo=codecov
   :alt: Codecov
   :target: https://app.codecov.io/gh/Laplusdestiny/plotly_extend_wrapper

.. image:: https://img.shields.io/github/release-date/Laplusdestiny/plotly_extend_wrapper?logo=github
   :alt: GitHub Release Date
   :target: https://github.com/Laplusdestiny/plotly_extend_wrapper/releases

.. image:: https://img.shields.io/pypi/v/plotly-extend-wrapper?logo=pypi
   :alt: PyPI - Version
   :target: https://pypi.org/project/plotly-extend-wrapper/

Plotly-Extend-Wrapper: Extended Plotly for Interactive Graphs
-------------------------------------------------------------

Overview: Plotly-Extend-Wrapper is a Python library that extends the capabilities of Plotly, an interactive graphing library. While Plotly provides powerful tools for creating visualizations, Plotly-Extend-Wrapper offers additional features that are not readily available through simple options or methods in the official Plotly library.


Key Features:
-------------

1. Seamless Integration with Plotly: Every function returns a standard ``plotly.graph_objects.Figure``, so you can keep using familiar Plotly methods such as ``update_layout`` or ``write_html``.
2. Advanced Methods for Common Tasks: Line charts with a secondary y-axis, highlighted periods and vertical lines, bubble charts with trend lines, and smoothed 3D surfaces can be created with a single function call.
3. Automated Data Preprocessing: Value counting, rounding and pivoting required by certain graph types are handled automatically.
4. pandas and polars Support: ``pandas.DataFrame``, ``polars.DataFrame`` and ``polars.LazyFrame`` are accepted as input (polars is an optional dependency).
