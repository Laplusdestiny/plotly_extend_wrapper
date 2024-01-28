# encoding: utf-8

from sklearn.datasets import load_iris, load_diabetes
from plotly_extend_wrapper.wrapper import Plot_pie, Plot_sunburst
from plotly import graph_objects as go


def test_pie():
    data = load_iris(as_frame=True)

    plot = Plot_pie(data["frame"], "target")
    assert isinstance(plot, go.Figure)


def test_sunburst():
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0

    plot = Plot_sunburst(data, ["target", "sex"])
    assert isinstance(plot, go.Figure)
