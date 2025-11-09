# encoding: utf-8

from plotly_extend_wrapper.common import check_directory


def test_create_directory(tmp_path):
    test_path = tmp_path / "test_dir/test_file.txt"
    result = check_directory(test_path)
    assert (tmp_path / "test_dir").is_dir()
    assert result == test_path.resolve()


def test_existing_directory(tmp_path):
    test_path = tmp_path / "existing_dir/test_file.txt"
    (tmp_path / "existing_dir").mkdir(parents=True, exist_ok=True)
    result = check_directory(test_path)
    assert (tmp_path / "existing_dir").is_dir()
    assert result == test_path.resolve()


def test_directory_path(tmp_path):
    test_path = tmp_path / "new_dir"
    result = check_directory(test_path)
    assert test_path.is_dir()
    assert result == test_path.resolve()
