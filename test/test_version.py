# encoding: utf-8

import importlib
import importlib.metadata
import re
from pathlib import Path

import plotly_extend_wrapper


def test_version_matches_pyproject():
    pyproject = (Path(__file__).resolve().parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    expected = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE).group(1)

    assert plotly_extend_wrapper.__version__ == expected


def test_version_without_installed_package(monkeypatch):
    def raise_not_found(name):
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(importlib.metadata, "version", raise_not_found)
    try:
        importlib.reload(plotly_extend_wrapper)
        assert plotly_extend_wrapper.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(plotly_extend_wrapper)

    assert plotly_extend_wrapper.__version__ != "unknown"
