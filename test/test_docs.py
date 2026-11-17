"""Keep the documentation in sync with the source code.

The API reference pages are generated from docstrings by Sphinx autodoc,
but the overview tables in ``docs/source/introduction.md`` list the public
API explicitly. These tests fail when a public function / class is added,
renamed or removed without updating the overview, or lacks a docstring.
"""

import inspect
import re
from pathlib import Path

import pytest

from plotly_extend_wrapper import common, updater, wrapper

ROOT = Path(__file__).resolve().parent.parent
INTRODUCTION = ROOT / "docs" / "source" / "introduction.md"
MODULES = [wrapper, updater, common]


def _public_api(module):
    return {
        f"{module.__name__}.{name}": obj
        for name, obj in vars(module).items()
        if not name.startswith("_")
        and (inspect.isfunction(obj) or inspect.isclass(obj))
        and obj.__module__ == module.__name__
    }


PUBLIC_API = {k: v for m in MODULES for k, v in _public_api(m).items()}


def test_introduction_lists_all_public_api():
    text = INTRODUCTION.read_text(encoding="utf-8")
    listed = set(re.findall(r"~(plotly_extend_wrapper\.\w+\.\w+)", text))
    assert listed == set(PUBLIC_API)


@pytest.mark.parametrize("name", sorted(PUBLIC_API))
def test_public_api_has_docstring(name):
    assert inspect.getdoc(PUBLIC_API[name]), f"{name} has no docstring"


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_api_reference_page_uses_automodule(module):
    page = ROOT / "docs" / "source" / f"{module.__name__.rsplit('.', 1)[1]}.md"
    assert f".. automodule:: {module.__name__}" in page.read_text(encoding="utf-8")
