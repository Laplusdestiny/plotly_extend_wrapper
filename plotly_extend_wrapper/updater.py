"""Utility class to update an existing Plotly figure."""

from pathlib import Path
from plotly import io as pio


class Update_plotly_object:
    """Update layout of an existing Plotly figure through a unified interface.

    The figure is updated **in place**.

    Parameters
    ----------
    po : plotly.graph_objects.Figure
        Figure to update.

    Examples
    --------
    .. code-block:: python

        from plotly_extend_wrapper import Plot_line, Update_plotly_object, check_directory

        fig = Plot_line(df, x="date", y=["sales"], secondary_y=["temperature"])

        updater = Update_plotly_object(fig)
        updater.update(
            xaxis_title="Date",
            yaxis_title="Sales",
            secondary_yaxis_title="Temperature",
            legend_position="h",
            height=500,
            width=900,
        )
        updater.write_image(check_directory("output/line.png"))
        fig = updater()
    """

    def __init__(self, po):
        self.po = po

    def _update_xaxis(self, title):
        if title is not None:
            self.po.update_xaxes(title_text=title)

    def _update_yaxis(self, title):
        if title is not None:
            self.po.update_yaxes(title_text=title)

    def _update_secondary_yaxis(self, title):
        if title is not None:
            self.po.update_yaxes(title_text=title, secondary_y=True)

    def _set_legend_position(self, position: str):
        if position is not None:
            self.po.update_layout(legend={"orientation": position})

    def _set_height(self, height: int):
        if height is not None:
            self.po.layout.height = height

    def _set_width(self, width: int):
        if width is not None:
            self.po.layout.width = width

    def _show_legend(self, legend: bool):
        if legend is not None:
            self.po.layout.showlegend = legend

    def _set_marker_size(self, marker_size: float):
        if marker_size is not None:
            self.po.update_traces(marker={"size": marker_size})

    def update(
        self,
        xaxis_title=None,
        yaxis_title=None,
        secondary_yaxis_title=None,
        legend=None,
        legend_position=None,
        height=None,
        width=None,
        marker_size=None,
    ):
        """Update all options.

        Options given as ``None`` are not changed.

        Parameters
        ----------
        xaxis_title : str, optional
            Title of the x-axis.
        yaxis_title : str, optional
            Title of the y-axis.
        secondary_yaxis_title : str, optional
            Title of the secondary y-axis.
        legend : bool, optional
            Show (True) or hide (False) the legend.
        legend_position : str, optional
            Legend orientation (``"h"`` or ``"v"``). Ignored when
            ``legend=False``.
        height : int, optional
            Figure height.
        width : int, optional
            Figure width.
        marker_size : int or float, optional
            Size of markers.
        """
        self._update_xaxis(xaxis_title)
        self._update_yaxis(yaxis_title)
        self._update_secondary_yaxis(secondary_yaxis_title)
        self._show_legend(legend)
        if legend in (None, True):
            self._set_legend_position(legend_position)
        self._set_height(height)
        self._set_width(width)
        self._set_marker_size(marker_size)

    def get_plot(self):
        """Return the updated figure.

        Calling the instance (``updater()``) is equivalent.

        Returns
        -------
        plotly.graph_objects.Figure
            The updated figure.
        """
        return self.po

    def write_image(self, filename):
        """Export the figure as a static image.

        The format is decided by the extension (e.g. ``.png``, ``.svg``,
        ``.pdf``). :func:`plotly.io.write_image` is used internally.

        .. note::

           Static image export requires
           `kaleido <https://github.com/plotly/Kaleido>`_. kaleido >= 1.0 also
           requires Google Chrome / Chromium. If it is not installed, run
           ``plotly_get_chrome`` (or ``plotly.io.get_chrome()``).

        Parameters
        ----------
        filename : str or pathlib.Path
            Output file path. The parent directory must exist
            (see :func:`~plotly_extend_wrapper.common.check_directory`).
        """
        pio.write_image(self.po, Path(filename))

    def __call__(self):
        """Return the updated figure (same as :meth:`get_plot`)."""
        return self.get_plot()
