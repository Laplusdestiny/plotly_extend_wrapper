from plotly import express as px
from plotly.subplots import make_subplots
import pandas as pd
from plotly_extend_wrapper.common import check_directory
from plotly import graph_objects as go
from scipy.interpolate import griddata
import numpy as np


def Plot_pie(data: pd.DataFrame, target: str, **kwargs):
    """Make pie plot

    Parameters
    ----------
    data : pd.DataFrame
        pandas.DataFrame included data to make pie chart
    target : str
        String which column you would like to use for pie chart

    Returns
    -------
    plotly.graph_objects
        Object of pie chart
    """
    vc = data[target].value_counts().reset_index(name="count")
    return px.pie(vc, names=target, values="count", **kwargs)


def Plot_sunburst(data: pd.DataFrame, groups: list, **kwargs):
    """Make sunburst plot

    Parameters
    ----------
    data : pd.DataFrame
        pandas.DataFrame included data to make sunburst chart
    groups : list
        Strings list of group
        Changed when you replace the order

    Returns
    -------
    plotly.graph_objects
        Object of sunburst chart
    """
    vc = data.value_counts(subset=groups).reset_index(name="count")
    return px.sunburst(vc, path=groups, values="count", **kwargs)


class Plot_bubble_chart:
    """Make bubble chart"""

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
        """Initialize function

        Parameters
        ----------
        df : pandas.DataFrame
            pandas.DataFrame included data to make plot
        x : str
            X-axis column's name
        y : str
            Y-axis column's name
        color : str, optional
            Column name you want colorize with data, by default None
        facet_col : str, optional
            Column name you want plot separeted vertically, by default None
        facet_row : str, optional
            Column name you want plot separeted horizontally, by default None
        rounded : list, optional
            Columns list which columns you want to round data, by default None
        decimals : list, optional
            Decimals list what level you want to round for each columns, by default None
        normalize : bool, optional
            If True, bubble size is calculated as normalized, by default False
        smoothing : bool, optional
            If True, bubble size were smoothed between each plot, by default False
        offset : int, optional
            Offset value for bubble size, by default 0
        """
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
            max_probs = vc.groupby(grouper)["count"].max().reset_index(name="max")
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
        grouper = list(filter(None, [self.color, self.facet_col, self.facet_row]))
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
                df.loc[:, f"{col}_rounded"] = df.loc[:, col].round(decimals=decimal)
                if self.x == col:
                    self.x = f"{col}_rounded"
                elif self.y == col:
                    self.y = f"{col}_rounded"
                else:
                    raise ValueError(f"{col} is not indicated. Check parameters")

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
        return self.plot


def Plot_line(
    df: pd.DataFrame,
    x: str,
    y: list,
    secondary_y: list,
    xtitle=None,
    ytitle=None,
    secondary_ytitle=None,
    save_html_path=None,
    vspan=None,
    vspan_color_randomize=False,
    sort_column=True,
    sort_x=True,
    opacity=0.2,
    px_kwargs=dict(),
    **kwargs,
):
    """Make line graph with secondary y using plotly.express

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe
    x : str
        X-axis column name
    y : list
        Y-axis columns name
    secondary_y : list
        Secondary y-axis columns name
    xtitle : str, optional
        X-axis title, by default None
    ytitle : str, optional
        Y-axis title, by default None
    secondary_ytitle : str, optional
        Secondary y-axis title, by default None
    save_html_path: str or pathlib.Path
        Path to output graph as html file
    vspan : list, optional
        Tuple list for filling color in specify period , by default None
    vspan_color_randomize : bool, optional
        If True, choose random color, by default False
    sort_column: boolean, optional
        If True, sort y column list
    sort_x: boolean, optional
        if True, sort by x column
    opacity : float, optional
        Same option of plotly.express.line, by default 0.2
    px_kwargs : dict, optional
        Kwargs dictionary used for original plotly.express.line object, by default dict()

    Returns
    -------
    plotly.graph_objects
        Plot graph
    """
    import random

    random.seed(42)

    def pick_color():
        return ["#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])][0]

    if isinstance(secondary_y, str):
        secondary_y = [secondary_y]

    plot_all_cols = pd.Series(y + secondary_y)
    if (~plot_all_cols.isin(df.columns)).any():
        not_include_cols = plot_all_cols[~plot_all_cols.isin(df.columns)].tolist()
        raise ValueError(f"{not_include_cols} columns are not in dataframe")

    y = [c for c in y if c not in secondary_y]
    if sort_column:
        y.sort()
        secondary_y.sort()

    if sort_x:
        df = df.sort_values(by=x)

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = px.line(df, x=x, y=y, **px_kwargs)
    fig2 = px.line(df, x=x, y=secondary_y, line_dash_sequence=["dash"], **px_kwargs)
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

    if save_html_path is not None:
        output_p = check_directory(save_html_path)
        subfig.write_html(output_p)
        print(f"Ouput html file [{output_p}]")

    return subfig


def Plot_bubble_chart_with_line(
    bubble_plot, line_info: dict, x1, x2, xtitle=None, ytitle=None, **kwargs
):
    """Making bubble chart with linear plot

    Parameters
    ----------
    bubble_plot : Figure
        Bubble chart object
    line_info : dict
        line dictionary
        Layer is below
            1. color
            2. a, b
        example: {
            "red": {
                "a": 0.015,
                "b": -4.3
            },
            "yellow": {
                "a": 0.015,
                "b": -2.5
            }
        }
    x1 : int or float
        start x-axis value
    x2 : int or float
        end x-axis value
    xtitle: str
        string of x-axis
    ytitle: str
        string of y-axis

    Returns
    -------
    Figure
        Combined figure
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
    subfig.add_traces(bubble_plot.data + line_plot.data)
    subfig.layout.xaxis.title = xtitle
    subfig.layout.yaxis.title = ytitle
    subfig.update_layout(**kwargs)
    return subfig


def Plot_surface(
    df: pd.DataFrame,
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
    def smooth_df(x: np.ndarray, y: np.ndarray, z: np.ndarray, num: int):
        xi = np.linspace(x.min(), x.max(), num)
        yi = np.linspace(y.min(), y.max(), num)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata((x,y), z, (xi.ravel(), yi.ravel()), method="cubic")
        zi = zi.reshape(xi.shape)
        zi = np.nan_to_num(zi)
        return xi, yi, zi

    if smoothing:
        X = df[x].values
        Y = df[y].values
        Z = df[z].values
        X, Y, Z = smooth_df(X, Y, Z, smooth_point_num)
    else:
        pivot_df = pd.pivot_table(df, index=x, columns=y, values=z, fill_value=fill_value)

        X = pivot_df.columns.values
        Y = pivot_df.index.values
        Z = pivot_df.values


    data = [go.Surface(x=X, y=Y, z=Z)]
    layout = go.Layout(
        title=title,
        scene=dict(
            xaxis=dict(title=y),    # need to be replaced
            yaxis=dict(title=x),
            zaxis=dict(title=z),
        ),
        height=height,
        width=width,
    )
    fig = go.Figure(data=data, layout=layout)
    return fig
