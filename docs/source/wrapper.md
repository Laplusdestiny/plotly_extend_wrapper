# wrapper

Plotting functions provided by `plotly_extend_wrapper.wrapper`.

All `data` / `df` parameters accept `pandas.DataFrame`, `polars.DataFrame` and `polars.LazyFrame` (polars support requires the optional `polars` dependency).

## Plot_pie

> Plot_pie(data: `pd.DataFrame | pl.DataFrame | pl.LazyFrame`, target: `str`, **kwargs)

Make pie plot. The value counts of `target` column are calculated automatically.

### Parameters
- data : `pd.DataFrame`, `pl.DataFrame` or `pl.LazyFrame`
    - DataFrame included data to make pie chart
- target : `str`
    - String which column you would like to use for pie chart
- **kwargs : dict
    - Additional keyword arguments passed to `plotly.express.pie`

### Returns

`plotly.graph_objects.Figure`

Object of pie chart

### Example

```python
import pandas as pd
from plotly_extend_wrapper import Plot_pie

df = pd.DataFrame({"category": ["A", "B", "A", "C", "B"]})
fig = Plot_pie(df, "category", title="Category ratio")
```


## Plot_sunburst

> Plot_sunburst(data: `pd.DataFrame | pl.DataFrame | pl.LazyFrame`, groups: `list`, **kwargs)

Make sunburst plot. The value counts of the combination of `groups` columns are calculated automatically.

### Parameters
- data : `pd.DataFrame`, `pl.DataFrame` or `pl.LazyFrame`
    - DataFrame included data to make sunburst chart
- groups : `list`
    - Strings list of group (from the innermost to the outermost)
    - Changed when you replace the order
- **kwargs : dict
    - Additional keyword arguments passed to `plotly.express.sunburst`

### Returns

`plotly.graph_objects.Figure`

Object of sunburst chart

### Example

```python
import pandas as pd
from plotly_extend_wrapper import Plot_sunburst

df = pd.DataFrame({
    "region": ["East", "East", "West", "West"],
    "product": ["A", "B", "A", "A"],
})
fig = Plot_sunburst(df, ["region", "product"])
```

## Plot_bubble_chart

> Plot_bubble_chart(df: `pd.DataFrame | pl.DataFrame | pl.LazyFrame`, x: `str`, y: `str`, color=None, facet_col=None, facet_row=None, rounded=None, decimals=None, normalize=False, smoothing=False, offset=0, **kwargs)

Make bubble chart. The bubble size is the frequency of each (x, y) pair (counted for each `color` / `facet_col` / `facet_row` group).

```{note}
`Plot_bubble_chart` is a **class**. Call the instance (`bubble()`) or use the `plot` attribute to get the figure.
```

### Parameters
- df : `pd.DataFrame`, `pl.DataFrame` or `pl.LazyFrame`
    - DataFrame included data to make plot
- x : `str`
    - X-axis column's name
- y : `str`
    - Y-axis column's name
- color : `str`, optional
    - Column name you want colorize with data, by default None
- facet_col : `str`, optional
    - Column name you want plot separated vertically, by default None
- facet_row : `str`, optional
    - Column name you want plot separated horizontally, by default None
- rounded : `list`, optional
    - Columns list which columns you want to round data, by default None
    - Only `x` and/or `y` column can be specified
    - Rounded values are stored in `{column}_rounded` column and used as the axis
- decimals : `list` or `int`, optional
    - Decimals list what level you want to round for each columns, by default None
    - If `int` is given, the same value is applied to all `rounded` columns
- normalize : `bool`, optional
    - If True, bubble size is calculated as normalized, by default False
- smoothing : `bool`, optional
    - If True, bubble size is scaled so that the maximum size of each group becomes the same, by default False
- offset : `int`, optional
    - Offset value added to bubble size, by default 0
- **kwargs : dict
    - Additional keyword arguments passed to `plotly.express.scatter`

### Attributes
- plot : `plotly.graph_objects.Figure`
    - Bubble chart
- vc : `pd.DataFrame`
    - Aggregated data used for the plot (`count` column is the bubble size)

### Returns

`Plot_bubble_chart` instance. `instance()` returns `plotly.graph_objects.Figure`.

### Example

```python
import pandas as pd
from plotly_extend_wrapper import Plot_bubble_chart

df = pd.DataFrame({
    "x": [1.12, 1.14, 2.21, 2.25, 2.31],
    "y": [1, 1, 2, 3, 3],
    "group": ["a", "a", "b", "b", "a"],
})
bubble = Plot_bubble_chart(df, x="x", y="y", color="group", rounded=["x"], decimals=1)
fig = bubble()
```

## Plot_line

> Plot_line(df: `pd.DataFrame | pl.DataFrame | pl.LazyFrame`, x: `str`, y: `list`, secondary_y: `list`, xtitle=None, ytitle=None, secondary_ytitle=None, save_html_path=None, vspan=None, vspan_color_randomize=False, vline=None, vline_color=None, sort_column=True, sort_x=True, opacity=0.2, px_kwargs=dict(), **kwargs)

Make line graph with secondary y using plotly.express. Lines on the secondary y-axis are drawn as dashed lines.

### Parameters
- df : `pd.DataFrame`, `pl.DataFrame` or `pl.LazyFrame`
    - Original dataframe
- x : `str`
    - X-axis column name
- y : `list`
    - Y-axis columns name
    - Columns also included in `secondary_y` are drawn only on the secondary y-axis
- secondary_y : `list` or `str`
    - Secondary y-axis columns name
    - Pass an empty list `[]` if you don't need the secondary y-axis
- xtitle : `str`, optional
    - X-axis title, by default None
- ytitle : `str`, optional
    - Y-axis title, by default None
- secondary_ytitle : `str`, optional
    - Secondary y-axis title, by default None
- save_html_path : `str` or `pathlib.Path`, optional
    - Path to output graph as html file. Parent directories are created automatically
- vspan : `list`, optional
    - Tuple list for filling color in specify period, by default None
    - Each tuple is `(x0, x1)` or `(x0, x1, color)`
    - Default color is `#fdb913`
- vspan_color_randomize : `bool`, optional
    - If True, choose random color for `vspan` without color, by default False
- vline : `list` or single value, optional
    - List of x values (e.g. timestamps) to add vertical lines, by default None
- vline_color : `str`, optional
    - Color of vertical lines, by default None (random color)
- sort_column : `bool`, optional
    - If True, sort y column list, by default True
- sort_x : `bool`, optional
    - If True, sort by x column, by default True
- opacity : `float`, optional
    - Opacity of `vspan`, by default 0.2
- px_kwargs : `dict`, optional
    - Kwargs dictionary used for original plotly.express.line object, by default dict()
- **kwargs : dict
    - Additional keyword arguments passed to `update_layout`

### Returns

`plotly.graph_objects.Figure`

Plot graph with secondary y-axis

### Raises

- `ValueError`
    - If columns in `y` or `secondary_y` are not in the dataframe

### Example

```python
import pandas as pd
from plotly_extend_wrapper import Plot_line

df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=48, freq="h"),
    "sales": range(48),
    "temperature": [i % 24 for i in range(48)],
})
fig = Plot_line(
    df,
    x="date",
    y=["sales"],
    secondary_y=["temperature"],
    ytitle="Sales",
    secondary_ytitle="Temperature",
    vspan=[("2024-01-01 06:00", "2024-01-01 12:00", "red")],
    vline=["2024-01-02 00:00"],
    vline_color="black",
    save_html_path="output/line.html",
)
```

## Plot_bubble_chart_with_line

> Plot_bubble_chart_with_line(bubble_plot: `Figure`, line_info: `dict`, x1: `float`, x2: `float`, xtitle=None, ytitle=None, **kwargs)

Making bubble chart with linear plot (`y = a * x + b`). The layout of `bubble_plot` is kept.

### Parameters
- bubble_plot : `plotly.graph_objects.Figure`
    - Bubble chart object (e.g. `Plot_bubble_chart(...)()`)
- line_info : `dict`
    - Line dictionary with following structure. The key is used as line color:
    ```python
    {
        "red": {"a": 0.015, "b": -4.3},
        "yellow": {"a": 0.015, "b": -2.5},
    }
    ```
- x1 : `float`
    - Start x-axis value
- x2 : `float`
    - End x-axis value
- xtitle : `str`, optional
    - String of x-axis
- ytitle : `str`, optional
    - String of y-axis
- **kwargs : dict
    - Additional keyword arguments passed to `update_layout`

### Returns

`plotly.graph_objects.Figure`

Combined figure of bubble chart and line plot

### Example

```python
from plotly_extend_wrapper import Plot_bubble_chart, Plot_bubble_chart_with_line

bubble = Plot_bubble_chart(df, x="x", y="y")
fig = Plot_bubble_chart_with_line(
    bubble(),
    line_info={"red": {"a": 1.0, "b": 0.0}},
    x1=0,
    x2=3,
)
```

## Plot_surface

> Plot_surface(df: `pd.DataFrame | pl.DataFrame | pl.LazyFrame`, x: `str`, y: `str`, z: `str`, fill_value=0, smoothing=False, smooth_point_num=100, title=None, height=None, width=None, **kwargs)

Generates a 3D surface plot using Plotly

- If `smoothing=False`, data is converted to a pivot table (index: `x`, columns: `y`, values: `z`). Note that the `y` column is shown on the horizontal axis of the scene and the `x` column on the depth axis.
- If `smoothing=True`, data is interpolated on a `smooth_point_num` x `smooth_point_num` grid by cubic interpolation (`scipy.interpolate.griddata`). Points outside the data range are filled with 0.

### Parameters
- df : `pd.DataFrame`, `pl.DataFrame` or `pl.LazyFrame`
    - The input data frame containing the data to plot
- x : `str`
    - The column name for the x-axis
- y : `str`
    - The column name for the y-axis
- z : `str`
    - The column name for the z-axis
- fill_value : `int`, optional
    - The value to fill missing data in the pivot table, by default 0
- smoothing : `bool`, optional
    - Whether to apply smoothing to the data, by default False
- smooth_point_num : `int`, optional
    - The number of points to use for smoothing, by default 100
- title : `str`, optional
    - The title of the plot, by default None
- height : `int`, optional
    - The height of the plot, by default None
- width : `int`, optional
    - The width of the plot, by default None
- **kwargs : dict
    - Currently not used (reserved)

### Returns

`plotly.graph_objects.Figure`

3D surface plot

### Example

```python
import numpy as np
import pandas as pd
from plotly_extend_wrapper import Plot_surface

xs, ys = np.meshgrid(np.arange(10), np.arange(10))
df = pd.DataFrame({"x": xs.ravel(), "y": ys.ravel()})
df["z"] = np.sin(df["x"]) + np.cos(df["y"])
fig = Plot_surface(df, "x", "y", "z", smoothing=True, title="Surface")
```
