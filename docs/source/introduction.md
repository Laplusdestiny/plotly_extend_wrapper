# Introduction

`plotly_extend_wrapper` is a wrapper library designed to simplify data visualization using Plotly. It provides an intuitive interface for creating complex plots with simple function calls.

## Installation

```bash
pip install plotly-extend-wrapper

# with polars support
pip install "plotly-extend-wrapper[polars]"
```

## Overview

The library offers various plotting functions and utilities to streamline the creation of common visualization types:

### Plotting Functions

- `Plot_pie()`: Create pie charts from the value counts of a column
- `Plot_sunburst()`: Generate hierarchical sunburst charts from the value counts of multiple columns
- `Plot_bubble_chart`: Create bubble charts whose bubble size is the frequency of (x, y) pairs
- `Plot_line()`: Draw line plots with secondary y-axis, highlighted periods and vertical lines
- `Plot_bubble_chart_with_line()`: Combine bubble charts with linear lines
- `Plot_surface()`: Generate 3D surface plots with optional smoothing

### Utility Functions

- `Update_plotly_object`: Customize plot properties after creation and export images
- `check_directory()`: Manage file paths and directory creation

## Supported Data Types

All plotting functions accept the following data types. polars objects are converted to `pandas.DataFrame` internally.

| Type | Note |
| --- | --- |
| `pandas.DataFrame` | |
| `polars.DataFrame` | requires `polars` |
| `polars.LazyFrame` | requires `polars` (collected automatically) |

Any other type raises `TypeError`.

## Quick Start

Here's a simple example to get you started:

```python
import pandas as pd
from plotly_extend_wrapper import Plot_pie, Plot_line, Plot_bubble_chart

# Create a pie chart
df = pd.DataFrame({'category': ['A', 'B', 'A', 'C', 'B']})
pie_chart = Plot_pie(df, 'category')

# Create a line plot with secondary y-axis
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', '2023-12-31', freq='D'),
    'value1': range(365),
    'value2': range(0, 730, 2)
})
line_plot = Plot_line(
    df,
    x='date',
    y=['value1'],
    secondary_y=['value2'],
    xtitle='Date',
    ytitle='Primary Axis',
    secondary_ytitle='Secondary Axis',
    vspan=[('2023-03-01', '2023-04-01')],
    vline=['2023-06-01'],
)

# Plot_bubble_chart is a class. Call the instance to get the figure.
df = pd.DataFrame({'x': [1, 1, 2, 2, 2], 'y': [1, 1, 2, 3, 3]})
bubble = Plot_bubble_chart(df, x='x', y='y')
bubble_fig = bubble()
```

### Using polars

```python
import polars as pl
from plotly_extend_wrapper import Plot_pie

df = pl.DataFrame({'category': ['A', 'B', 'A', 'C', 'B']})
pie_chart = Plot_pie(df, 'category')

# LazyFrame is also accepted
pie_chart = Plot_pie(df.lazy(), 'category')
```

For detailed documentation on each function and its parameters, please refer to the respective sections in this documentation.
