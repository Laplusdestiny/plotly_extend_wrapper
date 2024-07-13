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

    bubble = Plot_bubble_chart(data, x="x", y="y", smoothing=True, normalize=True)
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