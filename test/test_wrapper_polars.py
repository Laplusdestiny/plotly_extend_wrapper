# encoding: utf-8

import pytest

# Check if polars is available
try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None

from sklearn.datasets import load_iris, load_diabetes
from plotly_extend_wrapper.wrapper import (
    Plot_pie,
    Plot_sunburst,
    Plot_line,
    Plot_bubble_chart,
    Plot_bubble_chart_with_line,
    Plot_surface
)
from plotly import graph_objects as go
import pandas as pd

# Skip all tests in this module if polars is not available
pytestmark = pytest.mark.skipif(not POLARS_AVAILABLE, reason="polars not installed")


def MakeTimeSeriesDataPolars():
    data = pl.DataFrame(
        {
            "timestamp": ["2024-01-01 00:00:00", "2024-01-01 06:00:00", "2024-01-01 12:00:00", "2024-01-01 18:00:00", "2024-01-02 00:00:00"],
            "y1": [0, 0, 0, 0, 0],
            "y2": [100, 150, 200, 175, 150],
        }
    )
    return data


def MakeScattterDataPolars():
    data = pl.DataFrame(
        {
            "G1": ["A", "A", "A", "A", "B", "B", "B", "B", "A", "B", "A", "B"],
            "G2": ["a", "a", "b", "b", "a", "a", "b", "b", "a", "a", "b", "b"],
            "x": [0, 5, 3, 6, -3, -6, -1, -4, 3, -4, 4, -2],
            "y": [10, 20, 8, 16, 4, 2, -1, -6, 15, 1, 14, -2],
        }
    )
    return data


def test_Pie_polars_dataframe():
    data = load_iris(as_frame=True)
    # Convert to polars DataFrame
    pl_data = pl.from_pandas(data["frame"])

    plot = Plot_pie(pl_data, "target")
    assert isinstance(plot, go.Figure)


def test_Pie_polars_lazyframe():
    data = load_iris(as_frame=True)
    # Convert to polars LazyFrame
    pl_data = pl.from_pandas(data["frame"]).lazy()

    plot = Plot_pie(pl_data, "target")
    assert isinstance(plot, go.Figure)


def test_Sunburst_polars_dataframe():
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0
    # Convert to polars DataFrame
    pl_data = pl.from_pandas(data)

    plot = Plot_sunburst(pl_data, ["target", "sex"])
    assert isinstance(plot, go.Figure)


def test_Sunburst_polars_lazyframe():
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0
    # Convert to polars LazyFrame
    pl_data = pl.from_pandas(data).lazy()

    plot = Plot_sunburst(pl_data, ["target", "sex"])
    assert isinstance(plot, go.Figure)


def test_Line_polars_dataframe():
    data = MakeTimeSeriesDataPolars()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
    )

    assert isinstance(plot, go.Figure)


def test_Line_polars_lazyframe():
    data = MakeTimeSeriesDataPolars().lazy()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
    )

    assert isinstance(plot, go.Figure)


def test_LineVline_polars():
    data = MakeTimeSeriesDataPolars()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        vline=["2024-01-01 06:00:00"]
    )

    assert isinstance(plot, go.Figure)


def test_LinewithVspan_polars():
    data = MakeTimeSeriesDataPolars()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y="y2",
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        vspan=[
            ("2024-01-01 00:00:00", "2024-01-01 08:00:00"),
            ("2024-01-01 12:00:00", "2024-01-01 16:00:00"),
        ],
        vspan_color_randomize=True,
    )

    assert isinstance(plot, go.Figure)


def test_Bubble_polars_dataframe():
    data = load_iris(as_frame=True)
    pl_data = pl.from_pandas(data["frame"])

    bubble = Plot_bubble_chart(
        pl_data,
        x="sepal length (cm)",
        y="petal length (cm)",
        color="target",
        rounded=["sepal length (cm)", "petal length (cm)"],
        decimals=[1, 1],
        normalize=True,
        offset=0.01,
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Bubble_polars_lazyframe():
    data = load_iris(as_frame=True)
    pl_data = pl.from_pandas(data["frame"]).lazy()

    bubble = Plot_bubble_chart(
        pl_data,
        x="sepal length (cm)",
        y="petal length (cm)",
        color="target",
        rounded=["sepal length (cm)", "petal length (cm)"],
        decimals=1,
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Bubble_group_polars():
    data = MakeScattterDataPolars()

    bubble = Plot_bubble_chart(
        data,
        x="x",
        y="y",
        facet_col="G1",
        facet_row="G2",
        smoothing=True,
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Bubble_simple_polars():
    data = MakeScattterDataPolars()

    bubble = Plot_bubble_chart(
        data, x="x", y="y", smoothing=True, normalize=True)
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_BubbleWithLinear_polars():
    data = load_iris(as_frame=True)
    pl_data = pl.from_pandas(data["frame"])

    bubble = Plot_bubble_chart(
        pl_data,
        x="sepal length (cm)",
        y="petal length (cm)",
        color="target",
        rounded=["sepal length (cm)", "petal length (cm)"],
        decimals=[1, 1],
        normalize=True,
        offset=0.01,
    )
    new_plot = bubble()

    new_bubble = Plot_bubble_chart_with_line(
        new_plot,
        line_info={"red": {"a": 0.1, "b": 0.1}},
        x1=0,
        x2=10,
        xtitle="xaxis",
        ytitle="yaxis",
    )

    assert isinstance(new_bubble, go.Figure)


def test_PlotSurface_polars_dataframe():
    data = load_iris(as_frame=True)
    pl_data = pl.from_pandas(data["frame"])

    surface = Plot_surface(
        pl_data,
        x="sepal length (cm)",
        y="petal length (cm)",
        z="petal width (cm)"
    )

    assert isinstance(surface, go.Figure)


def test_PlotSurface_polars_lazyframe():
    data = load_iris(as_frame=True)
    pl_data = pl.from_pandas(data["frame"]).lazy()

    surface = Plot_surface(
        pl_data,
        x="sepal length (cm)",
        y="petal length (cm)",
        z="petal width (cm)",
        smoothing=True
    )

    assert isinstance(surface, go.Figure)


def test_PlotlineNotIncludeCol_polars():
    data = MakeScattterDataPolars()

    with pytest.raises(ValueError):
        Plot_line(data, x="timestamp", y=["x1"], secondary_y=["x2"])


def test_unsupported_datatype():
    """Test that unsupported data types raise appropriate error"""
    invalid_data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    
    with pytest.raises(TypeError, match="Unsupported data type"):
        Plot_pie(invalid_data, "col1")
