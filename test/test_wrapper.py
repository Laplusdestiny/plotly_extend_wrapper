# encoding: utf-8

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
import pytest

# Check if polars is available
try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None


def MakeTimeSeriesData():
    data = pd.DataFrame(
        [
            ["2024-01-01 00:00:00", 0, 100],
            ["2024-01-01 06:00:00", 0, 150],
            ["2024-01-01 12:00:00", 0, 200],
            ["2024-01-01 18:00:00", 0, 175],
            ["2024-01-02 00:00:00", 0, 150],
        ],
        columns=["timestamp", "y1", "y2"],
    )
    return data


def MakeScattterData():
    data = pd.DataFrame(
        [
            ["A", "a", 0, 10],
            ["A", "a", 5, 20],
            ["A", "b", 3, 8],
            ["A", "b", 6, 16],
            ["B", "a", -3, 4],
            ["B", "a", -6, 2],
            ["B", "b", -1, -1],
            ["B", "b", -4, -6],
            ["A", "a", 3, 15],
            ["B", "a", -4, 1],
            ["A", "b", 4, 14],
            ["B", "b", -2, -2],
        ],
        columns=["G1", "G2", "x", "y"],
    )
    return data


def MakeScattterDataPolars():
    if not POLARS_AVAILABLE:
        return MakeScattterData()
    data = pl.DataFrame(
        {
            "G1": ["A", "A", "A", "A", "B", "B", "B", "B", "A", "B", "A", "B"],
            "G2": ["a", "a", "b", "b", "a", "a", "b", "b", "a", "a", "b", "b"],
            "x": [0, 5, 3, 6, -3, -6, -1, -4, 3, -4, 4, -2],
            "y": [10, 20, 8, 16, 4, 2, -1, -6, 15, 1, 14, -2],
        }
    )
    return data


def test_Pie():
    data = load_iris(as_frame=True)

    plot = Plot_pie(data["frame"], "target")
    assert isinstance(plot, go.Figure)


def test_Sunburst():
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0

    plot = Plot_sunburst(data, ["target", "sex"])
    assert isinstance(plot, go.Figure)


def test_Line():
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        save_html_path="line.html",
    )

    assert isinstance(plot, go.Figure)


def test_LineVline():
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        save_html_path="line.html",
        vline=["2024-01-01 06:00:00"]
    )

    assert isinstance(plot, go.Figure)


def test_LineVlineinstr():
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        save_html_path="line.html",
        vline="2024-01-01 06:00:00"
    )

    assert isinstance(plot, go.Figure)


def test_LinewithVspan():
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y="y2",
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        save_html_path="line2.html",
        vspan=[
            ("2024-01-01 00:00:00", "2024-01-01 08:00:00"),
            ("2024-01-01 12:00:00", "2024-01-01 16:00:00"),
            ("2024-01-01 20:00:00", "2024-01-01 23:00:00"),
        ],
        vspan_color_randomize=True,
    )

    assert isinstance(plot, go.Figure)


def test_LinewithVspan2():
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y="y2",
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        save_html_path="line2.html",
        vspan=[
            ("2024-01-01 00:00:00", "2024-01-01 08:00:00", "blue"),
            ("2024-01-01 12:00:00", "2024-01-01 16:00:00", "yellow"),
            ("2024-01-01 20:00:00", "2024-01-01 23:00:00", "green"),
        ],
        vspan_color_randomize=True,
    )

    assert isinstance(plot, go.Figure)


def test_LinewithVspan3():
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y="y2",
        xtitle="timestamp",
        ytitle="value",
        secondary_ytitle="value2",
        save_html_path="line2.html",
        vspan=[
            ("2024-01-01 00:00:00", "2024-01-01 08:00:00"),
            ("2024-01-01 12:00:00", "2024-01-01 16:00:00"),
            ("2024-01-01 20:00:00", "2024-01-01 23:00:00"),
        ],
        vspan_color_randomize=False,
    )

    assert isinstance(plot, go.Figure)


def test_Bubble():
    data = load_iris(as_frame=True)

    bubble = Plot_bubble_chart(
        data["frame"],
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


def test_Bubble_rounded():
    data = load_iris(as_frame=True)

    bubble = Plot_bubble_chart(
        data["frame"],
        x="sepal length (cm)",
        y="petal length (cm)",
        color="target",
        rounded=["sepal length (cm)", "petal length (cm)"],
        decimals=1,
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Bubble_group():
    data = MakeScattterData()

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


def test_Bubble_simple():
    data = MakeScattterData()

    bubble = Plot_bubble_chart(
        data, x="x", y="y", smoothing=True, normalize=True)
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Bubble_simple2():
    data = MakeScattterData()

    bubble = Plot_bubble_chart(
        data, x="x", y="y", rounded=["x"], decimals=-1
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_BubbleWithLinear():
    data = load_iris(as_frame=True)

    bubble = Plot_bubble_chart(
        data["frame"],
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


def test_PlotlineNotIncludeCol():
    data = MakeScattterData()

    with pytest.raises(ValueError):
        Plot_line(data, x="timestamp", y=["x1"], secondary_y=["x2"])


def test_PlotBubbleStrangeParameter1():
    data = load_iris(as_frame=True)

    with pytest.raises(ValueError):
        bubble = Plot_bubble_chart(
            data["frame"],
            x="sepal length (cm)",
            y="petal length (cm)",
            color="target",
            rounded=["sepal length (cm)", "petal length (cm)", "error"],
            decimals=1,
            normalize=True,
            offset=0.01,
        )
        bubble()


def test_PlotBubbleStrangeParameter2():
    data = load_iris(as_frame=True)

    with pytest.raises(ValueError):
        bubble = Plot_bubble_chart(
            data["frame"],
            x="sepal length (cm)",
            y="petal length (cm)",
            color="target",
            rounded=["petal length (cm)", "sepal width (cm)"],
            decimals=[1, 1],
            normalize=True,
            offset=0.01,
        )
        bubble()


def test_PlotSurface():
    data = load_iris(as_frame=True)

    surface = Plot_surface(
        data["frame"],
        x="sepal length (cm)",
        y="petal length (cm)",
        z="petal width (cm)"
    )

    assert isinstance(surface, go.Figure)


def test_PlotSurface_with_smoothing():
    data = load_iris(as_frame=True)

    surface = Plot_surface(
        data["frame"],
        x="sepal length (cm)",
        y="petal length (cm)",
        z="petal width (cm)",
        smoothing=True
    )

    assert isinstance(surface, go.Figure)


def test_PlotSurface_with_all_options():
    data = load_iris(as_frame=True)

    surface = Plot_surface(
        data["frame"],
        x="sepal length (cm)",
        y="petal length (cm)",
        z="petal width (cm)",
        fill_value=1,
        smoothing=False,
        smooth_point_num=50,
        title="Test Surface",
        height=800,
        width=1000
    )

    assert isinstance(surface, go.Figure)
    assert surface.layout.title.text == "Test Surface"
    assert surface.layout.height == 800
    assert surface.layout.width == 1000


def test_PlotSurface_with_kwargs():
    data = load_iris(as_frame=True)

    surface = Plot_surface(
        data["frame"],
        x="sepal length (cm)",
        y="petal length (cm)",
        z="petal width (cm)",
        colorscale="Viridis",
        showscale=False,
    )

    assert isinstance(surface, go.Figure)
    assert surface.data[0].showscale is False
    assert surface.data[0].colorscale[0][1] == "#440154"


def test_Line_does_not_change_global_random_state():
    import random

    data = MakeTimeSeriesData()
    random.seed(0)
    expected = random.random()

    random.seed(0)
    Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y="y2",
        vspan=[("2024-01-01 00:00:00", "2024-01-01 08:00:00")],
        vspan_color_randomize=True,
        vline=["2024-01-01 06:00:00"],
    )

    assert random.random() == expected


def test_Line_with_sort_options():
    """Test line plot with different sorting options"""
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        sort_column=False,
        sort_x=False,
    )

    assert isinstance(plot, go.Figure)


def test_Line_with_save_html():
    """Test line plot with HTML save"""
    data = MakeTimeSeriesData()

    plot = Plot_line(
        data,
        x="timestamp",
        y=["y1"],
        secondary_y=["y2"],
        save_html_path="test_output.html",
    )

    assert isinstance(plot, go.Figure)
    # Check if file was created
    from pathlib import Path
    assert Path("test_output.html").exists()


def test_Bubble_with_color():
    """Test bubble chart with color parameter"""
    data = MakeScattterDataPolars()

    bubble = Plot_bubble_chart(
        data,
        x="x",
        y="y",
        color="G1",
        normalize=False,
        smoothing=False,
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Bubble_with_single_rounded():
    """Test bubble chart with single rounded column"""
    data = load_iris(as_frame=True)

    bubble = Plot_bubble_chart(
        data["frame"],
        x="sepal length (cm)",
        y="petal length (cm)",
        rounded=["sepal length (cm)"],
        decimals=0,
    )
    new_plot = bubble()

    assert isinstance(new_plot, go.Figure)


def test_Pie_with_kwargs():
    """Test pie chart with additional kwargs"""
    data = load_iris(as_frame=True)

    plot = Plot_pie(data["frame"], "target", hole=0.3)
    assert isinstance(plot, go.Figure)


def test_Sunburst_with_kwargs():
    """Test sunburst with additional kwargs"""
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0

    plot = Plot_sunburst(data, ["target", "sex"], maxdepth=2)
    assert isinstance(plot, go.Figure)


def test_WrapperWithoutPolars(monkeypatch):
    import importlib
    import sys
    from plotly_extend_wrapper import wrapper

    # Simulate an environment where polars is not installed
    monkeypatch.setitem(sys.modules, "polars", None)
    try:
        importlib.reload(wrapper)
        assert wrapper.POLARS_AVAILABLE is False
        assert wrapper.pl is None

        df = pd.DataFrame({"a": [1, 2, 3]})
        pd.testing.assert_frame_equal(wrapper._normalize_dataframe(df), df)
        with pytest.raises(TypeError):
            wrapper._normalize_dataframe([1, 2, 3])
    finally:
        monkeypatch.undo()
        importlib.reload(wrapper)
