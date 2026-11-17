"""Common utility functions."""

from pathlib import Path
from plotly.io import get_chrome


def check_directory(file_path):
    """Ensure that the directory for the given file path exists.

    - If ``file_path`` has an extension (e.g. ``output/graph.html``), its
      parent directory is created.
    - If ``file_path`` has no extension (e.g. ``output/graphs``), the path
      itself is created as a directory.

    Parameters
    ----------
    file_path : str or pathlib.Path
        The file path for which to check the directory.

    Returns
    -------
    pathlib.Path
        The resolved absolute path of the given file path.

    Examples
    --------
    .. code-block:: python

        from plotly_extend_wrapper import check_directory

        output_path = check_directory("output/graphs/line.html")
        fig.write_html(output_path)
    """
    file_path = Path(file_path)
    if not file_path.suffix:
        dir_p = file_path
    else:
        dir_p = file_path.parent
    if not dir_p.is_dir():
        dir_p.mkdir(parents=True, exist_ok=True)
    return file_path.resolve()
