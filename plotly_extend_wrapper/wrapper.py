"""Plotting functions.

Every ``data`` / ``df`` parameter accepts :class:`pandas.DataFrame`,
``polars.DataFrame`` and ``polars.LazyFrame`` (polars support requires the
optional ``polars`` dependency). polars objects are converted to
:class:`pandas.DataFrame` internally; any other type raises :class:`TypeError`.
"""

from plotly import express as px
from plotly.subplots import make_subplots
import pandas as pd
from plotly_extend_wrapper.common import check_directory
from plotly import graph_objects as go
from scipy.interpolate import griddata
import numpy as np
from copy import deepcopy
from typing import Union

# Optional polars support
try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None


def _normalize_dataframe(data) -> pd.DataFrame:
    """
    Convert various DataFrame formats to pandas.DataFrame.

    Supports pandas.DataFrame, polars.DataFrame, and polars.LazyFrame.

    Parameters
    ----------
    data : pd.DataFrame, pl.DataFrame, or pl.LazyFrame
        Input data frame

    Returns
    -------
    pd.DataFrame
        Normalized pandas DataFrame
    """
    if POLARS_AVAILABLE and pl is not None:
        if isinstance(data, pl.LazyFrame):
            return data.collect().to_pandas()
        elif isinstance(data, pl.DataFrame):
            return data.to_pandas()

    if isinstance(data, pd.DataFrame):
        return data

    raise TypeError(f"Unsupported data type: {type(data)}. Expected pandas.DataFrame, polars.DataFrame, or polars.LazyFrame.")


def Plot_pie(data: Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"], target: str, **kwargs):
    """Make pie chart from the value counts of a column.

    The value counts of ``target`` column are calculated automatically.

    Parameters
    ----------
    data : pandas.DataFrame, polars.DataFrame or polars.LazyFrame
        DataFrame included data to make pie chart.
    target : str
        Column name used for the pie chart.
    **kwargs
        Additional keyword arguments passed to :func:`plotly.express.pie`.

    Returns
    -------
    plotly.graph_objects.Figure
        Pie chart.

    Examples
    --------
    .. code-block:: python

        import pandas as pd
        from plotly_extend_wrapper import Plot_pie

        df = pd.DataFrame({"category": ["A", "B", "A", "C", "B"]})
        fig = Plot_pie(df, "category", title="Category ratio")
    """
    data = _normalize_dataframe(data)
    vc = data[target].value_counts().reset_index(name="count")
    return px.pie(vc, names=target, values="count", **kwargs)


def Plot_sunburst(data: Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"], groups: list, **kwargs):
    """Make hierarchical sunburst chart from the value counts of multiple columns.

    The value counts of the combination of ``groups`` columns are calculated
    automatically.

    Parameters
    ----------
    data : pandas.DataFrame, polars.DataFrame or polars.LazyFrame
        DataFrame included data to make sunburst chart.
    groups : list of str
        Column names of the hierarchy, from the innermost ring to the
        outermost ring. The chart changes when you change the order.
    **kwargs
        Additional keyword arguments passed to :func:`plotly.express.sunburst`.

    Returns
    -------
    plotly.graph_objects.Figure
        Sunburst chart.

    Examples
    --------
    .. code-block:: python

        import pandas as pd
        from plotly_extend_wrapper import Plot_sunburst

        df = pd.DataFrame({
            "region": ["East", "East", "West", "West"],
            "product": ["A", "B", "A", "A"],
        })
        fig = Plot_sunburst(df, ["region", "product"])
    """
    data = _normalize_dataframe(data)
    vc = data.value_counts(subset=groups).reset_index(name="count")
    return px.sunburst(vc, path=groups, values="count", **kwargs)


class Plot_bubble_chart:
    """Make bubble chart whose bubble size is the frequency of (x, y) pairs.

    The frequency is counted for each ``color`` / ``facet_col`` /
    ``facet_row`` group.

    .. note::

       ``Plot_bubble_chart`` is a **class**. Call the instance
       (``bubble()``) or use the :attr:`plot` attribute to get the figure.

    Parameters
    ----------
    df : pandas.DataFrame, polars.DataFrame or polars.LazyFrame
        DataFrame included data to make plot.
    x : str
        X-axis column name.
    y : str
        Y-axis column name.
    color : str, optional
        Column name used to colorize the bubbles, by default None.
    facet_col : str, optional
        Column name used to split the plot into columns, by default None.
    facet_row : str, optional
        Column name used to split the plot into rows, by default None.
    rounded : list of str, optional
        Columns to round, by default None. Only ``x`` and/or ``y`` can be
        specified. Rounded values are stored in a ``{column}_rounded``
        column, which is used as the axis.
    decimals : list of int or int, optional
        Number of decimals for each column in ``rounded``, by default None.
        If an ``int`` is given, the same value is applied to all ``rounded``
        columns.
    normalize : bool, optional
        If True, bubble size is calculated as normalized frequency,
        by default False.
    smoothing : bool, optional
        If True, bubble size is scaled so that the maximum size of each group
        becomes the same, by default False.
    offset : int, optional
        Offset value added to bubble size, by default 0.
    **kwargs
        Additional keyword arguments passed to :func:`plotly.express.scatter`.

    Attributes
    ----------
    plot : plotly.graph_objects.Figure
        Bubble chart.
    vc : pandas.DataFrame
        Aggregated data used for the plot (the ``count`` column is the
        bubble size).

    Raises
    ------
    ValueError
        If a column in ``rounded`` is neither ``x`` nor ``y``, or if
        ``decimals`` cannot be matched with ``rounded``.

    Examples
    --------
    .. code-block:: python

        import pandas as pd
        from plotly_extend_wrapper import Plot_bubble_chart

        df = pd.DataFrame({
            "x": [1.12, 1.14, 2.21, 2.25, 2.31],
            "y": [1, 1, 2, 3, 3],
            "group": ["a", "a", "b", "b", "a"],
        })
        bubble = Plot_bubble_chart(
            df, x="x", y="y", color="group", rounded=["x"], decimals=1
        )
        fig = bubble()
    """

    def __init__(
        self,
        df,
        x,
        y,
        color=None,
        facet_col=None,
        facet_row=None,
        rounded=None,
        decimals=None,
        normalize=False,
        smoothing=False,
        offset=0,
        **kwargs,
    ):
        df = _normalize_dataframe(df)
        self.df = df.copy()
        self.x = x
        self.y = y
        self.color = color
        self.facet_col = facet_col
        self.facet_row = facet_row
        self.rounded = rounded
        self.decimals = decimals
        self.normalize = normalize
        self.smoothing = smoothing
        self.offset = offset
        self.kwargs = kwargs

        self.df = self._rounding()
        self.vc, self.cols, self.grouper = self._value_counts()
        self.plot = self._make_bubble_chart()

    def _smoothing_probability(self, vc, grouper):
        if len(grouper) == 0:
            return vc
        else:
            max_probs = vc.groupby(
                grouper)["count"].max().reset_index(name="max")
            max_value = max_probs["max"].max()
            max_probs["ratio"] = max_value / max_probs["max"]
            smooth_dict = max_probs.set_index(grouper)["ratio"].to_dict()
            new_df = list()
            for key, df in vc.groupby(grouper):
                df["count"] = df["count"] * smooth_dict[key]
                new_df.append(df)
            new_df = pd.concat(new_df)
            return new_df

    def _value_counts(self):
        cols = [self.x, self.y]
        grouper = list(
            filter(None, [self.color, self.facet_col, self.facet_row]))
        if len(grouper) == 0:
            vc = self.df.value_counts(
                subset=cols, normalize=self.normalize
            ).reset_index(name="count")
        else:
            vc = (
                self.df.groupby(grouper)
                .value_counts(subset=cols, normalize=self.normalize)
                .reset_index(name="count")
            )
        if self.smoothing:
            vc = self._smoothing_probability(vc, grouper)
        vc["count"] = vc["count"] + self.offset
        return vc, cols, grouper

    def _rounding(self):
        df = self.df.copy()
        if self.rounded is not None and isinstance(self.rounded, list):
            if not isinstance(self.decimals, list):
                if isinstance(self.decimals, int) or isinstance(self.decimals, float):
                    if len(self.rounded) == 1:
                        self.decimals = [self.decimals]
                    elif len(self.rounded) == 2:
                        self.decimals = [self.decimals, self.decimals]
                    else:
                        raise ValueError(
                            "Parameter rounded seems to be strange, please check the parameter"
                        )

            for col, decimal in zip(self.rounded, self.decimals):
                df.loc[:, f"{col}_rounded"] = df.loc[:,
                                                     col].round(decimals=decimal)
                if self.x == col:
                    self.x = f"{col}_rounded"
                elif self.y == col:
                    self.y = f"{col}_rounded"
                else:
                    raise ValueError(
                        f"{col} is not indicated. Check parameters")

        return df

    def _make_bubble_chart(self):
        return px.scatter(
            self.vc,
            x=self.x,
            y=self.y,
            size="count",
            color=self.color,
            facet_col=self.facet_col,
            facet_row=self.facet_row,
            **self.kwargs,
        )

    def __call__(self):
        """Return the bubble chart.

        Returns
        -------
        plotly.graph_objects.Figure
            Same object as :attr:`plot`.
        """
        return self.plot


def Plot_line(
    df: Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"],
    x: str,
    y: list,
    secondary_y: list,
    xtitle=None,
    ytitle=None,
    secondary_ytitle=None,
    save_html_path=None,
    vspan=None,
    vspan_color_randomize=False,
    vline=None,
    vline_color=None,
    sort_column=True,
    sort_x=True,
    opacity=0.2,
    px_kwargs=dict(),
    **kwargs,
):
    """Make line chart with secondary y-axis using plotly.express.

    Lines on the secondary y-axis are drawn as dashed lines. Highlighted
    periods (``vspan``) and vertical lines (``vline``) can be added.

    Parameters
    ----------
    df : pandas.DataFrame, polars.DataFrame or polars.LazyFrame
        Original dataframe.
    x : str
        X-axis column name.
    y : list of str
        Y-axis column names. Columns also included in ``secondary_y`` are
        drawn only on the secondary y-axis.
    secondary_y : list of str or str
        Secondary y-axis column names. Pass an empty list ``[]`` if you don't
        need the secondary y-axis.
    xtitle : str, optional
        X-axis title, by default None.
    ytitle : str, optional
        Y-axis title, by default None.
    secondary_ytitle : str, optional
        Secondary y-axis title, by default None.
    save_html_path : str or pathlib.Path, optional
        Path to output the graph as an html file, by default None. Parent
        directories are created automatically.
    vspan : list of tuple, optional
        Periods to fill with color, by default None. Each tuple is
        ``(x0, x1)`` or ``(x0, x1, color)``. The default color is
        ``#fdb913``.
    vspan_color_randomize : bool, optional
        If True, choose a random color for ``vspan`` items without color,
        by default False.
    vline : list or scalar, optional
        X values (e.g. timestamps) to add vertical lines, by default None.
    vline_color : str, optional
        Color of vertical lines, by default None (random color).
    sort_column : bool, optional
        If True, sort ``y`` and ``secondary_y`` column lists, by default True.
    sort_x : bool, optional
        If True, sort rows by ``x`` column, by default True.
    opacity : float, optional
        Opacity of ``vspan``, by default 0.2.
    px_kwargs : dict, optional
        Keyword arguments passed to :func:`plotly.express.line`,
        by default ``dict()``.
    **kwargs
        Additional keyword arguments passed to ``Figure.update_layout``.

    Returns
    -------
    plotly.graph_objects.Figure
        Line chart with secondary y-axis.

    Raises
    ------
    ValueError
        If columns in ``y`` or ``secondary_y`` are not in the dataframe.

    Examples
    --------
    .. code-block:: python

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
    """
    import random

    rng = random.Random(42)

    df = _normalize_dataframe(df)

    def pick_color():
        return ["#" + "".join([rng.choice("0123456789ABCDEF") for j in range(6)])][0]

    if isinstance(secondary_y, str):
        secondary_y = [secondary_y]

    plot_all_cols = pd.Series(y + secondary_y)
    if (~plot_all_cols.isin(df.columns)).any():
        not_include_cols = plot_all_cols[~plot_all_cols.isin(
            df.columns)].tolist()
        raise ValueError(f"{not_include_cols} columns are not in dataframe")

    y = [c for c in y if c not in secondary_y]
    if sort_column:
        y.sort()
        secondary_y.sort()

    if sort_x:
        df = df.sort_values(by=x)

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = px.line(df, x=x, y=y, **px_kwargs)
    fig2 = px.line(df, x=x, y=secondary_y,
                   line_dash_sequence=["dash"], **px_kwargs)
    fig2.update_traces(yaxis="y2")

    subfig.add_traces(fig.data + fig2.data)
    subfig.update_layout(**kwargs)
    subfig.layout.xaxis.title = xtitle
    subfig.layout.yaxis.title = ytitle
    subfig.layout.yaxis2.title = secondary_ytitle

    if vspan is not None:
        for d in vspan:
            if len(d) == 3:
                x0 = d[0]
                x1 = d[1]
                color = d[2]
            else:
                x0 = d[0]
                x1 = d[1]
                if vspan_color_randomize:
                    color = pick_color()
                else:
                    color = "#fdb913"

            subfig.add_vrect(
                x0=x0,
                x1=x1,
                fillcolor=color,
                opacity=opacity,
                layer="below",
                line_width=0,
            )

    if vline is not None:
        if not isinstance(vline, list):
            vline = [vline]

        if vline_color is None:
            vline_color = pick_color()

        for v in vline:
            subfig.add_vline(x=v, line_color=vline_color)

    if save_html_path is not None:
        output_p = check_directory(save_html_path)
        subfig.write_html(output_p)
        print(f"Ouput html file [{output_p}]")

    return subfig


def Plot_bubble_chart_with_line(
    bubble_plot, line_info: dict, x1, x2, xtitle=None, ytitle=None, **kwargs
):
    """Overlay linear lines (``y = a * x + b``) on a bubble chart.

    The layout of ``bubble_plot`` is kept.

    Parameters
    ----------
    bubble_plot : plotly.graph_objects.Figure
        Bubble chart object (e.g. ``Plot_bubble_chart(...)()``).
    line_info : dict
        Line definitions. The key is used as the line color and the value is
        a dict with slope ``a`` and intercept ``b``::

            {
                "red": {"a": 0.015, "b": -4.3},
                "yellow": {"a": 0.015, "b": -2.5},
            }

    x1 : int or float
        Start x-axis value of the lines.
    x2 : int or float
        End x-axis value of the lines.
    xtitle : str, optional
        X-axis title, by default None.
    ytitle : str, optional
        Y-axis title, by default None.
    **kwargs
        Additional keyword arguments passed to ``Figure.update_layout``.

    Returns
    -------
    plotly.graph_objects.Figure
        Combined figure of the bubble chart and the lines.

    Examples
    --------
    .. code-block:: python

        from plotly_extend_wrapper import Plot_bubble_chart, Plot_bubble_chart_with_line

        bubble = Plot_bubble_chart(df, x="x", y="y")
        fig = Plot_bubble_chart_with_line(
            bubble(),
            line_info={"red": {"a": 1.0, "b": 0.0}},
            x1=0,
            x2=3,
        )
    """
    linear_df = pd.DataFrame(columns=["x", "y", "color"])
    color_dict = {}
    for color in line_info.keys():
        a = line_info[color]["a"]
        b = line_info[color]["b"]
        linear_df = pd.concat(
            [
                linear_df,
                pd.Series([x1, a * x1 + b, color], index=linear_df.columns)
                .to_frame()
                .T,
            ]
        )
        linear_df = pd.concat(
            [
                linear_df,
                pd.Series([x2, a * x2 + b, color], index=linear_df.columns)
                .to_frame()
                .T,
            ]
        )
        color_dict[color] = color
    line_plot = px.line(
        linear_df, x="x", y="y", color="color", color_discrete_map=color_dict
    )

    subfig = make_subplots()
    for trace in bubble_plot.data + line_plot.data:
        subfig.add_trace(trace)
    if xtitle is not None:
        subfig.layout.xaxis.title = xtitle
    if ytitle is not None:
        subfig.layout.yaxis.title = ytitle
    original_layout = deepcopy(bubble_plot.layout)
    subfig.update_layout(original_layout, **kwargs)
    return subfig


def Plot_surface(
    df: Union[pd.DataFrame, "pl.DataFrame", "pl.LazyFrame"],
    x: str,
    y: str,
    z: str,
    fill_value=0,
    smoothing=False,
    smooth_point_num=100,
    title=None,
    height=None,
    width=None,
    **kwargs,
):
    """Generate 3D surface plot with optional cubic interpolation.

    - If ``smoothing=False``, data is converted to a pivot table
      (index: ``x``, columns: ``y``, values: ``z``). Note that the ``y``
      column is shown on the horizontal axis of the scene and the ``x``
      column on the depth axis.
    - If ``smoothing=True``, data is interpolated on a
      ``smooth_point_num`` x ``smooth_point_num`` grid by cubic interpolation
      (:func:`scipy.interpolate.griddata`). Points outside the data range are
      filled with 0.

    Parameters
    ----------
    df : pandas.DataFrame, polars.DataFrame or polars.LazyFrame
        The input data frame containing the data to plot.
    x : str
        The column name for the x-axis.
    y : str
        The column name for the y-axis.
    z : str
        The column name for the z-axis.
    fill_value : int, optional
        The value to fill missing data in the pivot table, by default 0.
    smoothing : bool, optional
        Whether to apply smoothing to the data, by default False.
    smooth_point_num : int, optional
        The number of points per axis used for smoothing, by default 100.
    title : str, optional
        The title of the plot, by default None.
    height : int, optional
        The height of the plot, by default None.
    width : int, optional
        The width of the plot, by default None.
    **kwargs
        Additional keyword arguments passed to
        :class:`plotly.graph_objects.Surface` (e.g. ``colorscale``,
        ``showscale``).

    Returns
    -------
    plotly.graph_objects.Figure
        3D surface plot.

    Examples
    --------
    .. code-block:: python

        import numpy as np
        import pandas as pd
        from plotly_extend_wrapper import Plot_surface

        xs, ys = np.meshgrid(np.arange(10), np.arange(10))
        df = pd.DataFrame({"x": xs.ravel(), "y": ys.ravel()})
        df["z"] = np.sin(df["x"]) + np.cos(df["y"])
        fig = Plot_surface(df, "x", "y", "z", smoothing=True, title="Surface")
    """

    def smooth_df(x: np.ndarray, y: np.ndarray, z: np.ndarray, num: int):
        xi = np.linspace(x.min(), x.max(), num)
        yi = np.linspace(y.min(), y.max(), num)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata((x, y), z, (xi.ravel(), yi.ravel()), method="cubic")
        zi = zi.reshape(xi.shape)
        zi = np.nan_to_num(zi)
        return xi, yi, zi

    df = _normalize_dataframe(df)

    if smoothing:
        X = df[x].values
        Y = df[y].values
        Z = df[z].values
        X, Y, Z = smooth_df(X, Y, Z, smooth_point_num)
    else:
        pivot_df = pd.pivot_table(
            df, index=x, columns=y, values=z, fill_value=fill_value
        )

        X = pivot_df.columns.values
        Y = pivot_df.index.values
        Z = pivot_df.values

    data = [go.Surface(x=X, y=Y, z=Z, **kwargs)]
    layout = go.Layout(
        title=title,
        scene=dict(
            xaxis=dict(title=y),  # need to be replaced
            yaxis=dict(title=x),
            zaxis=dict(title=z),
        ),
        height=height,
        width=width,
    )
    fig = go.Figure(data=data, layout=layout)
    return fig
