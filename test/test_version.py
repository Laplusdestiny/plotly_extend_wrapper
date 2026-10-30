# encoding: utf-8

import re
from pathlib import Path

import plotly_extend_wrapper


def test_version_matches_pyproject():
    pyproject = (Path(__file__).resolve().parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    expected = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE).group(1)

    assert plotly_extend_wrapper.__version__ == expected
