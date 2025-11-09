# plotly_extend_wrapper

[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Laplusdestiny/plotly_extend_wrapper/main?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper/commits/main/)
[![Codecov](https://img.shields.io/codecov/c/gh/Laplusdestiny/plotly_extend_wrapper?style=flat&logo=codecov)](https://app.codecov.io/gh/Laplusdestiny/plotly_extend_wrapper)
[![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/Laplusdestiny/plotly_extend_wrapper?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper/releases)
[![PyPI - Version](https://img.shields.io/pypi/v/plotly_extend_wrapper?logo=pypi)](https://pypi.org/project/plotly-extend-wrapper/)

A Python library that extends Plotly functionality to create sophisticated visualizations with minimal code. This wrapper simplifies the process of creating complex plots while maintaining the flexibility of Plotly.

## Features

- **Simple Interface**: Create complex visualizations with just a few lines of code
- **Pandas Integration**: Seamless integration with pandas DataFrames
- **Multiple Plot Types**: Support for various chart types including pie charts, sunburst diagrams, and 3D surfaces
- **Customization**: Easy plot customization through a unified interface
- **Automatic Layout**: Smart default settings for common plot configurations

For detailed documentation and examples, visit our [Documentation](https://laplusdestiny.github.io/plotly_extend_wrapper/)

## Install

```
pip install plotly-extend-wrapper
```

## Requirement

- Python >= 3.9
- Plotly >= 5.0.0
- kaleido = 0.2.1
- pandas >= 2.2.0
- scipy >= 1.12.0

## Available Plots

- **Pie Charts** (`wrapper.Plot_pie`): Create pie charts with automatic value counting
- **Sunburst Charts** (`wrapper.Plot_sunburst`): Visualize hierarchical data structures
- **Bubble Charts** (`wrapper.Plot_bubble_chart`): Generate scatter plots with size-encoded data points
- **Line Plots** (`wrapper.Plot_line`): Create line charts with support for secondary y-axis and vertical spans
- **Bubble Charts with Trend Lines** (`wrapper.Plot_bubble_chart_with_line`): Combine bubble charts with linear trends
- **3D Surface Plots** (`wrapper.Plot_surface`): Create 3D surface plots with optional smoothing

## Example

```python
import pandas as pd
from plotly_extend_wrapper import Plot_line

# Create sample data
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', '2023-01-10'),
    'sales': range(10),
    'profit': [x * 1.5 for x in range(10)]
})

# Create a line plot with secondary y-axis
plot = Plot_line(
    df,
    x='date',
    y=['sales'],
    secondary_y=['profit'],
    xtitle='Date',
    ytitle='Sales',
    secondary_ytitle='Profit'
)


## Issue
If there are some bugs, please make issue to tell me!

[![GitHub issues](https://img.shields.io/github/issues/Laplusdestiny/plotly_extend_wrapper?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper/issues)

## License
MIT License

[![GitHub](https://img.shields.io/github/license/Laplusdestiny/plotly_extend_wrapper?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper?tab=MIT-1-ov-file#MIT-1-ov-file)

