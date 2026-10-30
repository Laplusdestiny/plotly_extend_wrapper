# plotly_extend_wrapper

[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Laplusdestiny/plotly_extend_wrapper/main?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper/commits/main/)
[![Codecov](https://img.shields.io/codecov/c/gh/Laplusdestiny/plotly_extend_wrapper?style=flat&logo=codecov)](https://app.codecov.io/gh/Laplusdestiny/plotly_extend_wrapper)
[![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/Laplusdestiny/plotly_extend_wrapper?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper/releases)
[![PyPI - Version](https://img.shields.io/pypi/v/plotly_extend_wrapper?logo=pypi)](https://pypi.org/project/plotly-extend-wrapper/)

Extended Python library for Plotly

- **Simple Interface**: Create complex visualizations with just a few lines of code
- **pandas / polars Support**: Accepts `pandas.DataFrame`, `polars.DataFrame` and `polars.LazyFrame`
- **Automated Preprocessing**: Value counting, rounding and pivoting are handled for you
- **Multiple Plot Types**: Pie, sunburst, bubble, line (with secondary y-axis), and 3D surface charts
- **Customization**: Update titles, legend, size and markers through a unified interface

For detailed documentation and examples, visit our [Documentation](https://laplusdestiny.github.io/plotly_extend_wrapper/)

## Install

``` bash
pip install plotly-extend-wrapper

# with polars support
pip install "plotly-extend-wrapper[polars]"
```

## Quick Start

``` python
import pandas as pd
from plotly_extend_wrapper import Plot_pie, Plot_line, Update_plotly_object

df = pd.DataFrame({"category": ["A", "B", "A", "C", "B"]})
fig = Plot_pie(df, "category")  # value counts are computed automatically

df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=100, freq="D"),
    "sales": range(100),
    "temperature": [i % 30 for i in range(100)],
})
fig = Plot_line(
    df,
    x="date",
    y=["sales"],
    secondary_y=["temperature"],
    ytitle="Sales",
    secondary_ytitle="Temperature",
    vline=["2024-02-01"],
)

updater = Update_plotly_object(fig)
updater.update(height=500, width=900, legend_position="h")
updater.write_image("output/line.png")
```

## Supported Functions

| Name | Description |
| --- | --- |
| `Plot_pie` | Pie chart from the value counts of a column |
| `Plot_sunburst` | Hierarchical sunburst chart from the value counts of multiple columns |
| `Plot_bubble_chart` | Bubble chart whose size is the frequency of (x, y) pairs |
| `Plot_bubble_chart_with_line` | Overlay linear lines (`y = a * x + b`) on a bubble chart |
| `Plot_line` | Line chart with secondary y-axis, highlighted periods and vertical lines |
| `Plot_surface` | 3D surface plot with optional cubic interpolation |
| `Update_plotly_object` | Update layout of an existing figure and export it as an image |
| `check_directory` | Create parent directories for an output path |

## Requirement

- Python >= 3.11
- plotly >= 6.1.0
- kaleido >= 0.2.1
- pandas >= 2.0.0
- pyarrow >= 10.0.0
- numpy >= 1.24.0
- scipy >= 1.8.0
- nbformat >= 4.2.0
- polars >= 0.20.0 (optional)

## Development

``` bash
uv sync                                    # install dependencies
uv run pytest test                         # run tests
uv run sphinx-build docs/ docs/_build      # build documentation
```

## Issue

If there are some bugs, please make issue to tell me!

[![GitHub issues](https://img.shields.io/github/issues/Laplusdestiny/plotly_extend_wrapper?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper/issues)

## License

MIT License

[![GitHub](https://img.shields.io/github/license/Laplusdestiny/plotly_extend_wrapper?logo=github)](https://github.com/Laplusdestiny/plotly_extend_wrapper?tab=MIT-1-ov-file#MIT-1-ov-file)
