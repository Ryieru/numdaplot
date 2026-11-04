"""
Drawing of the missing values of a Table: bars per column and a map of every value.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.drawing.bar_drawing import draw_bar_chart
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.heatmap_drawing import (
	CELL_ASPECT,
	CELL_INTERPOLATION,
	hide_frame,
	place_column_names,
	stack_columns,
)
from numdaplot.plots.drawing.plot_theme import GRID_COLOR
from numdaplot.plots.drawing.whole_numbers import place_whole_ticks
from numdaplot.ratios.measure import Measure

MISSING_COLOR = "#33415c"
PRESENT_COLOR = GRID_COLOR
MISSING_LABEL = "Missing"
PRESENT_LABEL = "Present"
ROW_LABEL = "Row"
LOWEST_RATIO = 0.0
HIGHEST_RATIO = 1.0
LEGEND_SWATCH_CORNER = (0.0, 0.0)
LEGEND_SWATCH_SIZE = 0.0


def draw_missing_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw one bar per column of a Table, as high as its missing values.

	Ratios are on an axis from 0 to 1, and counts have ticks on whole numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A MissingChart and the missing values of each column.

	Returns
	-------
	DrawnChart
		``Missing count`` or ``Missing ratio`` as label of the values, and grid lines across their axis only.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.missing_cells import read_missing_counts
	>>> from numdaplot.plots.drawing.missing_drawing import draw_missing_chart
	>>> prices = ndp.Array.from_list([12.0, None])
	>>> flats = ndp.Table.from_arrays({"price": prices})
	>>> axes = Figure().add_subplot()
	>>> chart = ndp.MissingChart()
	>>> drawn_chart = draw_missing_chart(axes, ChartLayer(chart, read_missing_counts(flats, chart.measure)))
	>>> [float(limit) for limit in axes.get_ylim()]
	[0.0, 1.0]
	"""
	chart = cast(MissingChart, layer.chart)
	bar_layer = ChartLayer(BarChart(), layer.values)
	drawn_chart = draw_bar_chart(axes, bar_layer)
	if chart.measure == Measure.RATIO:
		axes.set_ylim(LOWEST_RATIO, HIGHEST_RATIO)
		return drawn_chart

	values = cast(ChartValues, layer.values)
	counts = values.series[0].values
	place_whole_ticks(axes.yaxis, counts)

	return drawn_chart


def draw_missing_map(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each value of a Table as a cell, light gray when present and dark when missing.

	The columns are side by side and the rows go down from the first one. A legend names the two colors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		The chart of the map and where each value is missing.

	Returns
	-------
	DrawnChart
		``Row`` as label of the vertical axis, and no grid lines.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.charts.missing_map_chart import MissingMapChart
	>>> from numdaplot.plots.data.missing_cells import read_missing_cells
	>>> from numdaplot.plots.drawing.missing_drawing import draw_missing_map
	>>> prices = ndp.Array.from_list([12.0, None])
	>>> flats = ndp.Table.from_arrays({"price": prices})
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = draw_missing_map(axes, ChartLayer(MissingMapChart(), read_missing_cells(flats)))
	>>> axes.images[0].get_array().tolist()
	[[0.0], [1.0]]
	"""
	values = cast(ChartValues, layer.values)
	grid = stack_columns(values.series)
	cell_colors = ListedColormap([PRESENT_COLOR, MISSING_COLOR])
	axes.imshow(
		grid,
		cmap=cell_colors,
		vmin=LOWEST_RATIO,
		vmax=HIGHEST_RATIO,
		aspect=CELL_ASPECT,
		interpolation=CELL_INTERPOLATION,
	)
	place_column_names(axes, values.series)
	place_whole_ticks(axes.yaxis, values.positions.values)
	hide_frame(axes)
	add_legend_swatch(axes, MISSING_COLOR, MISSING_LABEL)
	add_legend_swatch(axes, PRESENT_COLOR, PRESENT_LABEL)
	drawn_chart = DrawnChart(None, ROW_LABEL, False, GridAxes.NONE, None)

	return drawn_chart


def add_legend_swatch(axes: Axes, color_code: str, label: str) -> None:
	"""
	Add an invisible patch of a color, which the legend shows with its label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	color_code
		The ``#rrggbb`` code shown in the legend.
	label
		The name of the color in the legend.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.missing_drawing import add_legend_swatch
	>>> axes = Figure().add_subplot()
	>>> add_legend_swatch(axes, "#33415c", "Missing")
	>>> axes.get_legend_handles_labels()[1]
	['Missing']
	"""
	# A patch of size 0 draws nothing, yet the legend shows its color.
	swatch = Rectangle(LEGEND_SWATCH_CORNER, LEGEND_SWATCH_SIZE, LEGEND_SWATCH_SIZE, facecolor=color_code, label=label)
	axes.add_patch(swatch)
