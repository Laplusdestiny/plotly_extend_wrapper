from pathlib import Path


def check_directory(file_p):
    file_p = Path(file_p)
    if file_p.suffix == "":
        dir_p = file_p
    else:
        dir_p = file_p.parent
    if not dir_p.is_dir():
        dir_p.mkdir(parents=True)
    return file_p.resolve()
