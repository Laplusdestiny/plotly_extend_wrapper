# Introduction

`plotly_extend_wrapper` is a wrapper library designed to simplify data visualization using Plotly. It provides an intuitive interface for creating complex plots with simple function calls.

## Overview

The library offers various plotting functions and utilities to streamline the creation of common visualization types:

### Plotting Functions

- `Plot_pie()`: Create pie charts from DataFrame columns
- `Plot_sunburst()`: Generate hierarchical sunburst charts
- `Plot_bubble_chart`: Create bubble charts with customizable size mapping
- `Plot_line()`: Draw line plots with support for secondary y-axis
- `Plot_bubble_chart_with_line()`: Combine bubble charts with trend lines
- `Plot_surface()`: Generate 3D surface plots with optional smoothing

### Utility Functions

- `Update_plotly_object`: Customize plot properties after creation
- `check_directory()`: Manage file paths and directory creation

## Quick Start

Here's a simple example to get you started:

```python
import pandas as pd
from plotly_extend_wrapper import Plot_pie, Plot_line

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
    secondary_ytitle='Secondary Axis'
)
```

For detailed documentation on each function and its parameters, please refer to the respective sections in this documentation.
