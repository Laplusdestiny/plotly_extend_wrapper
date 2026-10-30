# common

Utility functions provided by `plotly_extend_wrapper.common`.

## check_directory

> check_directory(file_path: `str | pathlib.Path`)

Ensures that the directory for the given file path exists, creating it if necessary.

- If `file_path` has an extension (e.g. `output/graph.html`), its parent directory is created.
- If `file_path` has no extension (e.g. `output/graphs`), the path itself is created as a directory.

### Parameters
- file_path : `str` or `pathlib.Path`
    - The file path for which to check the directory

### Returns

`pathlib.Path`

The resolved absolute path of the given file path

### Example

```python
from plotly_extend_wrapper import check_directory

output_path = check_directory("output/graphs/line.html")
fig.write_html(output_path)
```
