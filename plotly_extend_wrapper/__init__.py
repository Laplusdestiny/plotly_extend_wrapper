from plotly_extend_wrapper.wrapper import *
from plotly_extend_wrapper.updater import *
from plotly_extend_wrapper.common import *

from importlib.metadata import PackageNotFoundError, version as _version

try:
    __version__ = _version("plotly-extend-wrapper")
except PackageNotFoundError:
    __version__ = "unknown"
