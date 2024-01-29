from pathlib import Path
from plotly import io as pio


class Update_plotly_object:
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
        """Update all options

        Parameters
        ----------
        xaxis_title : str
            Title name of X-axis
        yaxis_title : str
            Title name of Y-axis
        secondary_yaxis_title : str
            Title name of secondary Y-axis
        legend : bool
            ON/OFF legend
        legend_position : str
            Legend position
        height : int
            Figure height
        width : int
            Figure width
        marker_size: int or float
            Size of marker
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
        return self.po

    def write_image(self, filename):
        pio.write_image(self.po, Path(filename))

    def __call__(self):
        return self.get_plot()
