# updater

Utility class provided by `plotly_extend_wrapper.updater`.

## Update_plotly_object

> Update_plotly_object(po: `plotly.graph_objects.Figure`)

Update layout of an existing Plotly figure through a unified interface. The figure is updated in place.

### Parameters
- po : `plotly.graph_objects.Figure`
    - Figure to update

### Methods

#### update

> update(xaxis_title=None, yaxis_title=None, secondary_yaxis_title=None, legend=None, legend_position=None, height=None, width=None, marker_size=None)

Update all options. Options given as `None` are not changed.

- xaxis_title : `str`, optional
    - Title name of X-axis
- yaxis_title : `str`, optional
    - Title name of Y-axis
- secondary_yaxis_title : `str`, optional
    - Title name of secondary Y-axis
- legend : `bool`, optional
    - ON/OFF legend
- legend_position : `str`, optional
    - Legend orientation (`"h"` or `"v"`). Ignored when `legend=False`
- height : `int`, optional
    - Figure height
- width : `int`, optional
    - Figure width
- marker_size : `int` or `float`, optional
    - Size of marker

#### get_plot

> get_plot()

Return the updated `plotly.graph_objects.Figure`. Calling the instance (`updater()`) is equivalent.

#### write_image

> write_image(filename: `str | pathlib.Path`)

Export the figure as a static image (format is decided by the extension, e.g. `.png`, `.svg`, `.pdf`) using `plotly.io.write_image`.

```{note}
Static image export requires [kaleido](https://github.com/plotly/Kaleido). kaleido >= 1.0 also requires Google Chrome / Chromium. If it is not installed, run `plotly_get_chrome` (or `plotly.io.get_chrome()`).
```

### Example

```python
from plotly_extend_wrapper import Plot_line, Update_plotly_object, check_directory

fig = Plot_line(df, x="date", y=["sales"], secondary_y=["temperature"])

updater = Update_plotly_object(fig)
updater.update(
    xaxis_title="Date",
    yaxis_title="Sales",
    secondary_yaxis_title="Temperature",
    legend_position="h",
    height=500,
    width=900,
)
updater.write_image(check_directory("output/line.png"))
fig = updater()
```
