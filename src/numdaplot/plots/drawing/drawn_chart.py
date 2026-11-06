"""
What a drawn chart tells the style of its Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.drawing.grid_axes import GridAxes


@dataclass(frozen=True)
class DrawnChart:
	"""
	What a drawn chart tells the style of its Plot: default labels, axis directions and grid lines.

	.. versionadded:: 0.1.0

	Parameters
	----------
	x_label
		The default label of the axis of the ``x`` values, or None.
	y_label
		The default label of the axis of the series, or None.
	x_on_vertical_axis
		True when the ``x`` values are on the vertical axis, as with horizontal bars.
	grid_axes
		The axes crossed by the grid lines, when the PlotStyle shows them.
	legend_title
		The title of the legend, such as the ``color_by`` column of a ScatterChart, or None.
	legend_outside
		True when ``LegendPosition.BEST`` places the legend past the axes, the chart filling them.

	Examples
	--------
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> DrawnChart("day", "price", False, GridAxes.BOTH, None).grid_axes
	<GridAxes.BOTH: 1>
	"""

	x_label: str | None
	y_label: str | None
	x_on_vertical_axis: bool
	grid_axes: GridAxes
	legend_title: str | None
	legend_outside: bool = False
