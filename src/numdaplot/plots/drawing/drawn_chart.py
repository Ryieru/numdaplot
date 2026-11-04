"""
What a drawn chart tells the style of its Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass


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
	grids_positions
		True when grid lines are also drawn across the axis of the ``x`` values, not only across the axis
		of the series.
	legend_title
		The title of the legend, such as the ``color_by`` column of a ScatterChart, or None.

	Examples
	--------
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> DrawnChart("day", "price", False, True, None).grids_positions
	True
	"""

	x_label: str | None
	y_label: str | None
	x_on_vertical_axis: bool
	grids_positions: bool
	legend_title: str | None
