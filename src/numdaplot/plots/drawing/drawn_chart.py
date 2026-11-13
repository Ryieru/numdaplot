"""
What a drawn chart tells the style of its Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.drawing.axes.grid_axes import GridAxes


@dataclass(frozen=True)
class DrawnChart:
	"""
	What a drawn chart tells the style of its Plot: default labels, axis directions and grid lines.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Adds ``x_title_name`` and ``y_title_name``, the names of the values in the default title when they differ
		from the labels of the axes.

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
	title
		The default title when it is not the ``y`` label by the ``x`` label, or None.
	legend_outside
		True when ``LegendPosition.BEST`` places the legend past the axes, the chart filling them.
	x_title_name
		The name of the ``x`` values in the default title, the ``x`` label when None.
	y_title_name
		The name of the series in the default title, the ``y`` label when None.

	Examples
	--------
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.axes.grid_axes import GridAxes
	>>> DrawnChart("day", "price", False, GridAxes.BOTH, None).grid_axes
	<GridAxes.BOTH: 1>
	"""

	x_label: str | None
	y_label: str | None
	x_on_vertical_axis: bool
	grid_axes: GridAxes
	legend_title: str | None
	title: str | None = None
	legend_outside: bool = False
	x_title_name: str | None = None
	y_title_name: str | None = None
