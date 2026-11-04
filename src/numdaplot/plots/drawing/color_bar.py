"""
Color bar showing the color scale of a chart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

import numpy
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure
from numpy.typing import NDArray

from numdaplot.plots.drawing.whole_numbers import place_whole_ticks


def add_color_bar(
	axes: Axes, scaled_artist: ScalarMappable, scale_label: str, scaled_numbers: NDArray[numpy.float64]
) -> None:
	"""
	Draw the color scale of a chart next to its axes, with a label.

	Its ticks are on whole numbers only when every number colored is whole.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	scaled_artist
		The points or the cells colored along the scale.
	scale_label
		The label of the color bar, such as the ``color_by`` column of a ScatterChart, empty for none.
	scaled_numbers
		The numbers colored, NaN where a value is missing.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.color_bar import add_color_bar
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> add_color_bar(axes, axes.scatter([0.0], [1.0], c=[5.0]), "rooms", numpy.array([5.0]))
	>>> figure.axes[1].get_ylabel()
	'rooms'
	"""
	figure = cast(Figure, axes.figure)
	color_bar = figure.colorbar(scaled_artist, ax=axes, label=scale_label)
	place_whole_ticks(color_bar.ax.yaxis, scaled_numbers)
