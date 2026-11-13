"""
Drawing of the missing values of a Table: bars per column and a map of every value.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

import numpy
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.container import BarContainer
from matplotlib.patches import Rectangle

from numdaplot.measures.measure import Measure
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.missing_cells import MissingCounts
from numdaplot.plots.drawing.bar_drawing import draw_bar_chart
from numdaplot.plots.drawing.bar_value_labels import BAR_LABEL_FONT_SIZE, BAR_LABEL_PADDING
from numdaplot.plots.drawing.cell_merging import find_cell_limits, fit_cells_to_axes, merge_cells
from numdaplot.plots.drawing.default_labels import COLUMN_LABEL, ROW_LABEL
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

MISSING_COLOR = "#33415c"
PRESENT_COLOR = GRID_COLOR
MISSING_TOTAL_LABEL = "Missing ({missing_total})"
PRESENT_LABEL = "Present"
MAP_TITLE = "Map of missing values"
LOWEST_RATIO = 0.0
HIGHEST_RATIO = 1.0
RATIO_TICK_COUNT = 6
# A patch placed nowhere draws nothing, yet the legend shows its colors.
LEGEND_SWATCH_CORNER = (numpy.nan, numpy.nan)
LEGEND_SWATCH_SIZE = 0.0
LEGEND_SWATCH_EDGE_WIDTH = 0.5
PERCENT_FACTOR = 100.0
STACKED_BAR_LABEL = "{count}\n{percent:.1f} %"
ONE_LINE_BAR_LABEL = "{count} ({percent:.1f} %)"
STACKED_LABEL_MINIMUM_WIDTH = 34.0
ONE_LINE_LABEL_MINIMUM_WIDTH = 13.0
# Heights in pixels, kept high enough for the layout narrowing the axes afterwards.
STACKED_LABEL_HEIGHT = 40.0
ONE_LINE_LABEL_HEIGHT = 90.0
UPWARD_ROTATION = 90
HIGHEST_HEADROOM_SHARE = 0.5
EMPTY_BAR_TOP = 1.0


def draw_missing_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw one bar per column of a Table, as high as its missing values.

	Ratios have ticks from 0 to 1, and counts have ticks on whole numbers. Each bar is labeled with its number of
	missing values and their share of the rows, when the bars leave room for it.

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
		``"Missing count"`` or ``"Missing ratio"`` as label of the values, and grid lines across their axis only.

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
	>>> chart = ndp.MissingChart(measure=ndp.Measure.RATIO)
	>>> drawn_chart = draw_missing_chart(axes, ChartLayer(chart, read_missing_counts(flats, chart.measure)))
	>>> [float(tick) for tick in axes.get_yticks()][-1]
	1.0
	"""
	chart = cast(MissingChart, layer.chart)
	values = cast(MissingCounts, layer.values)
	bar_layer = ChartLayer(BarChart(), values)
	drawn_chart = draw_bar_chart(axes, bar_layer)
	label_height = write_bar_labels(axes, values)
	shown_values = values.series[0].values
	highest_bar = float(numpy.max(shown_values, initial=0.0))
	if chart.measure == Measure.RATIO:
		highest_bar = HIGHEST_RATIO

	bar_top = highest_bar
	if bar_top == 0:
		bar_top = EMPTY_BAR_TOP

	axis_top = find_axis_top(bar_top, label_height, axes.bbox.height)
	axes.set_ylim(LOWEST_RATIO, axis_top)
	if chart.measure == Measure.RATIO:
		ratio_ticks = numpy.linspace(LOWEST_RATIO, HIGHEST_RATIO, RATIO_TICK_COUNT)
		axes.set_yticks(ratio_ticks)
		return drawn_chart

	place_whole_ticks(axes.yaxis, shown_values)

	return drawn_chart


def write_bar_labels(axes: Axes, values: MissingCounts) -> float:
	"""
	Write the number of missing values and their share of the rows above each bar, with the room the bars leave.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes holding the bars.
	values
		The counts of each column and the number of rows.

	Returns
	-------
	float
		The height in pixels the labels need above the bars, 0 when the bars are too narrow for them.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.missing_cells import read_missing_counts
	>>> from numdaplot.plots.drawing.bar_drawing import draw_bar_chart
	>>> from numdaplot.plots.drawing.missing_drawing import write_bar_labels
	>>> flats = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.0, None])})
	>>> values = read_missing_counts(flats, ndp.Measure.COUNT)
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = draw_bar_chart(axes, ChartLayer(ndp.BarChart(), values))
	>>> write_bar_labels(axes, values)
	40.0
	>>> axes.texts[0].get_text().splitlines()
	['1', '50.0 %']
	"""
	column_count = len(values.counts)
	if column_count == 0:
		return 0.0

	column_width = axes.bbox.width / column_count
	if column_width < ONE_LINE_LABEL_MINIMUM_WIDTH:
		return 0.0

	is_stacked = column_width >= STACKED_LABEL_MINIMUM_WIDTH
	label_format = ONE_LINE_BAR_LABEL
	rotation = UPWARD_ROTATION
	label_height = ONE_LINE_LABEL_HEIGHT
	if is_stacked:
		label_format = STACKED_BAR_LABEL
		rotation = 0
		label_height = STACKED_LABEL_HEIGHT

	labels = format_bar_labels(values, label_format)
	bars = cast(BarContainer, axes.containers[0])
	axes.bar_label(
		bars,
		labels=labels,
		padding=BAR_LABEL_PADDING,
		fontsize=BAR_LABEL_FONT_SIZE,
		rotation=rotation,
	)

	return label_height


def format_bar_labels(values: MissingCounts, label_format: str) -> list[str]:
	"""
	Return the label of each bar, with its number of missing values and their percentage of the rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The counts of each column and the number of rows.
	label_format
		The text of a label, with the fields ``count`` and ``percent``.

	Returns
	-------
	list[str]
		One label per bar. The percentages of a Table without rows are 0.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.missing_cells import read_missing_counts
	>>> from numdaplot.plots.drawing.missing_drawing import ONE_LINE_BAR_LABEL, format_bar_labels
	>>> flats = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.0, None])})
	>>> format_bar_labels(read_missing_counts(flats, ndp.Measure.COUNT), ONE_LINE_BAR_LABEL)
	['1 (50.0 %)']
	"""
	row_count = max(values.row_count, 1)
	labels = list[str]()

	for count in values.counts:
		whole_count = int(count)
		percent = whole_count * PERCENT_FACTOR / row_count
		label = label_format.format(count=whole_count, percent=percent)
		labels.append(label)

	return labels


def find_axis_top(bar_top: float, label_height: float, axes_height: float) -> float:
	"""
	Return the top of the axis of the values, high enough to leave the labels room above the highest bar.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bar_top
		The highest value the axis must show, above 0.
	label_height
		The height in pixels the labels need.
	axes_height
		The height of the axes in pixels.

	Returns
	-------
	float
		The top of the axis, at most twice the highest value.

	Examples
	--------
	>>> from numdaplot.plots.drawing.missing_drawing import find_axis_top
	>>> find_axis_top(30.0, 40.0, 400.0)
	33.333333333333336
	"""
	headroom_share = min(label_height / axes_height, HIGHEST_HEADROOM_SHARE)
	axis_top = bar_top / (1 - headroom_share)

	return axis_top


def draw_missing_map(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each value of a Table as a cell, light gray when present and dark when missing.

	The columns are side by side and the rows go down from the first one. When the axes have too few pixels for the
	cells, a dark band marks at least one missing value among the cells it covers. A legend names the two colors and
	gives the total of missing values, past the axes with ``LegendPosition.BEST``.

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
		``Column`` and ``Row`` as labels, the title of the map, no grid lines, and the legend past the axes.

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
	shown_cells = fit_cells_to_axes(grid, axes, merge_cells)
	cell_colors = ListedColormap([PRESENT_COLOR, MISSING_COLOR])
	cell_limits = find_cell_limits(grid)
	axes.imshow(
		shown_cells,
		cmap=cell_colors,
		vmin=LOWEST_RATIO,
		vmax=HIGHEST_RATIO,
		aspect=CELL_ASPECT,
		interpolation=CELL_INTERPOLATION,
		extent=cell_limits,
	)
	place_column_names(axes, values.series)
	place_whole_ticks(axes.yaxis, values.positions.values)
	hide_frame(axes)
	missing_total = int(grid.sum())
	missing_label = MISSING_TOTAL_LABEL.format(missing_total=missing_total)
	add_legend_swatch(axes, MISSING_COLOR, missing_label)
	add_legend_swatch(axes, PRESENT_COLOR, PRESENT_LABEL)
	drawn_chart = DrawnChart(COLUMN_LABEL, ROW_LABEL, False, GridAxes.NONE, None, title=MAP_TITLE, legend_outside=True)

	return drawn_chart


def add_legend_swatch(axes: Axes, color_code: str, label: str) -> None:
	"""
	Add an invisible patch of a color, which the legend shows with a thin border and its label.

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
	>>> add_legend_swatch(axes, "#33415c", "Missing (3)")
	>>> axes.get_legend_handles_labels()[1]
	['Missing (3)']
	"""
	swatch = Rectangle(
		LEGEND_SWATCH_CORNER,
		LEGEND_SWATCH_SIZE,
		LEGEND_SWATCH_SIZE,
		facecolor=color_code,
		edgecolor=MISSING_COLOR,
		linewidth=LEGEND_SWATCH_EDGE_WIDTH,
		label=label,
	)
	axes.add_patch(swatch)
