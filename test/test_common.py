# encoding: utf-8

from plotly_extend_wrapper import common
import pytest
from pathlib import Path


@pytest.mark.parametrize("path", ["./test_dir/test.png", "./test_dir_only"])
def testCheckDirectory(path):
    checked_path = common.check_directory(path)

    if checked_path.suffix == "":
        assert isinstance(checked_path, Path) and checked_path.is_dir()
    else:
        assert isinstance(checked_path, Path) and checked_path.parent.is_dir()
