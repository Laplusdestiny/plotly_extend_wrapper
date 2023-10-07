# encoding: utf-8

import pandas as pd
from sklearn.datasets import load_iris, load_diabetes
from plotly_extend_wrapper.wrapper import *

def test_pie():
    data = load_iris(as_frame=True)

    plot = Plot_pie(data["frame"], "target")

def test_sunburst():
    data = load_diabetes(as_frame=True)["frame"]
    data["sex"] = data["sex"] >= 0

    plot = Plot_sunburst(data, ["target", "sex"])

