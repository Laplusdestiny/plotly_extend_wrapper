# encoding: utf-8

from sklearn.datasets import load_iris, load_diabetes
from plotly_extend_wrapper.wrapper import Plot_pie, Plot_sunburst, Plot_line
from plotly import graph_objects as go
import pandas as pd


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


def test_pie():
    data = load_iris(as_frame=True)

    plot = Plot_pie(data["frame"], "target")
    assert isinstance(plot, go.Figure)


def test_sunburst():
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0

    plot = Plot_sunburst(data, ["target", "sex"])
    assert isinstance(plot, go.Figure)


def test_line():
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
