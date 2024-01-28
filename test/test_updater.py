# encoding: utf-8

from plotly_extend_wrapper.wrapper import Plot_line
from plotly_extend_wrapper.updater import Update_plotly_object
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

    plot = Plot_line(data, x="timestamp", y=["y1"], secondary_y=["y2"])
    return plot


def CheckTitle(plot, axis, expected):
    if axis == "x":
        assert plot.layout.xaxis.title.text == expected
    elif axis == "y":
        assert plot.layout.yaxis.title.text == expected
    elif axis == "secondary_y":
        assert plot.layout.yaxis2.title.text == expected


def testAxisTitle():
    plot = MakeTimeSeriesData()
    updater = Update_plotly_object(plot)
    updater.update(
        xaxis_title="new xTitle",
        yaxis_title="new yTitle",
        secondary_yaxis_title="new secondary yTitle",
    )

    new_plot = updater()

    CheckTitle(new_plot, "x", "new xTitle")
    CheckTitle(new_plot, "y", "new yTitle")
    CheckTitle(new_plot, "secondary_y", "new secondary yTitle")
