# wrapper

## Plot_pie

> Plot_pie(data: `pd.DataFrame`, target: `str`, **kwargs)

Make pie plot

### Parameters
- data : `pd.DataFrame`
    - pandas.DataFrame included data to make pie chart
- target : `str`
    - String which column you would like to use for pie chart
- **kwargs : dict
    - Additional keyword arguments passed to `plotly.express.pie`

### Returns

`plotly.graph_objects`

Object of pie chart


## Plot_sunburst

> Plot_sunburst(data: `pd.DataFrame`, groups: `list`, **kwargs)

Make sunburst plot

### Parameters
- data : `pd.DataFrame`
    - pandas.DataFrame included data to make sunburst chart
- groups : `list`
    - Strings list of group
    - Changed when you replace the order
- **kwargs : dict
    - Additional keyword arguments passed to `plotly.express.sunburst`

### Returns

`plotly.graph_objects`

Object of sunburst chart

## Plot_bubble_chart

> Plot_bubble_chart(df: `pd.DataFrame`, x: `str`, y: `str`, color=None, facet_col=None, facet_row=None, rounded=None, decimals=None, normalize=False, smoothing=False, offset=0, **kwargs)

Make bubble chart

### Parameters
- df : `pandas.DataFrame`
    - pandas.DataFrame included data to make plot
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
- decimals : `list`, optional
    - Decimals list what level you want to round for each columns, by default None
- normalize : `bool`, optional
    - If True, bubble size is calculated as normalized, by default False
- smoothing : `bool`, optional
    - If True, bubble size were smoothed between each plot, by default False
- offset : `int`, optional
    - Offset value for bubble size, by default 0
- **kwargs : dict
    - Additional keyword arguments passed to `plotly.express.scatter`

### Returns

`plotly.graph_objects`

Object of bubble chart

## Plot_line

> Plot_line(df: `pd.DataFrame`, x: `str`, y: `list`, secondary_y: `list`, xtitle=None, ytitle=None, secondary_ytitle=None, save_html_path=None, vspan=None, vspan_color_randomize=False, sort_column=True, sort_x=True, opacity=0.2, px_kwargs=dict(), **kwargs)

Make line graph with secondary y using plotly.express

### Parameters
- df : `pd.DataFrame`
    - Original dataframe
- x : `str`
    - X-axis column name
- y : `list`
    - Y-axis columns name
- secondary_y : `list`
    - Secondary y-axis columns name
- xtitle : `str`, optional
    - X-axis title, by default None
- ytitle : `str`, optional
    - Y-axis title, by default None
- secondary_ytitle : `str`, optional
    - Secondary y-axis title, by default None
- save_html_path : `str` or `pathlib.Path`, optional
    - Path to output graph as html file
- vspan : `list`, optional
    - Tuple list for filling color in specify period, by default None
- vspan_color_randomize : `bool`, optional
    - If True, choose random color, by default False
- sort_column : `bool`, optional
    - If True, sort y column list
- sort_x : `bool`, optional
    - If True, sort by x column
- opacity : `float`, optional
    - Same option of plotly.express.line, by default 0.2
- px_kwargs : `dict`, optional
    - Kwargs dictionary used for original plotly.express.line object, by default dict()
- **kwargs : dict
    - Additional keyword arguments for layout update

### Returns

`plotly.graph_objects`

Plot graph with secondary y-axis

## Plot_bubble_chart_with_line

> Plot_bubble_chart_with_line(bubble_plot: `Figure`, line_info: `dict`, x1: `float`, x2: `float`, xtitle=None, ytitle=None, **kwargs)

Making bubble chart with linear plot

### Parameters
- bubble_plot : `Figure`
    - Bubble chart object
- line_info : `dict`
    - Line dictionary with following structure:
    ```python
    {
        "color": {
            "a": slope,
            "b": intercept
        }
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
    - Additional keyword arguments for layout update

### Returns

`plotly.graph_objects`

Combined figure of bubble chart and line plot

## Plot_surface

> Plot_surface(df: `pd.DataFrame`, x: `str`, y: `str`, z: `str`, fill_value=0, smoothing=False, smooth_point_num=100, title=None, height=None, width=None, **kwargs)

Generates a 3D surface plot using Plotly

### Parameters
- df : `pd.DataFrame`
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
    - Additional keyword arguments for the plot

### Returns

`plotly.graph_objects`

3D surface plot


