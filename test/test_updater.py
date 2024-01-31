# encoding: utf-8

from plotly_extend_wrapper.wrapper import Plot_line
from plotly_extend_wrapper.updater import Update_plotly_object
import pandas as pd
from pathlib import Path


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


def CheckGraphSize(plot, axis, expected):
    if axis == "width":
        assert plot.layout.width == expected
    elif axis == "height":
        assert plot.layout.height == expected


def CheckLegend(plot, expected):
    assert plot.layout.showlegend == expected


def CheckMarkerSize(plot, expected):
    assert plot.data[0].marker.size == expected


def test_AxisTitle():
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


def test_GraphSize():
    plot = MakeTimeSeriesData()
    updater = Update_plotly_object(plot)
    updater.update(height=1000, width=1200)
    new_plot = updater()

    CheckGraphSize(new_plot, "width", 1200)
    CheckGraphSize(new_plot, "height", 1000)


def test_ShowLegend():
    plot = MakeTimeSeriesData()
    updater = Update_plotly_object(plot)
    updater.update(legend=False)
    new_plot = updater()

    CheckLegend(new_plot, False)


def test_WriteImage():
    plot = MakeTimeSeriesData()
    updater = Update_plotly_object(plot)
    output = Path("test.png")
    updater.write_image(output)
    assert output.is_file()


def test_MarkerSize():
    plot = MakeTimeSeriesData()
    updater = Update_plotly_object(plot)
    updater.update(marker_size=50)
    new_plot = updater()

    CheckMarkerSize(new_plot, 50)

def test_SetLegendPosition():
    plot = MakeTimeSeriesData()
    updater = Update_plotly_object(plot)
    updater.update(legend_position="v")
    new_plot = updater()

    assert new_plot.layout.legend["orientation"] == "v"