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


def test_check_directory_file_with_suffix(tmp_path):
    """Test check_directory with file path that has suffix"""
    test_file = tmp_path / "subdir" / "test.txt"
    result = check_directory(test_file)

    # Directory should be created
    assert test_file.parent.is_dir()
    assert result == test_file.resolve()


def test_check_directory_nested_path(tmp_path):
    """Test check_directory with deeply nested path"""
    test_path = tmp_path / "level1" / "level2" / "level3" / "file.csv"
    result = check_directory(test_path)

    # All directories should be created
    assert test_path.parent.is_dir()
    assert (tmp_path / "level1").is_dir()
    assert (tmp_path / "level1" / "level2").is_dir()
    assert result == test_path.resolve()


def test_check_directory_returns_absolute_path(tmp_path):
    """Test that check_directory returns absolute path"""
    test_path = tmp_path / "test_dir"
    result = check_directory(test_path)

    assert result.is_absolute()
    assert result == test_path.resolve()
