from pathlib import Path


def check_directory(file_path):
    """
    Ensures that the directory for the given file path exists, creating it if necessary.

    Args:
        file_path (str or Path): The file path for which to check the directory.

    Returns:
        Path: The resolved absolute path of the given file path.
    """
    file_path = Path(file_path)
    if not file_path.suffix:
        dir_p = file_path
    else:
        dir_p = file_path.parent
    if not dir_p.is_dir():
        dir_p.mkdir(parents=True, exist_ok=True)
    return file_path.resolve()
