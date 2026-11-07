"""
Drawing of a HeatmapChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings
from typing import cast

import matplotlib
import numpy
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from numpy.typing import NDArray

from numdaplot.arrays.operations.float_errors import INTERNAL_FILES
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.cell_values import CellValues
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.data.chart_values import ChartValues, Series
from numdaplot.plots.drawing.cell_merging import average_cells, find_cell_limits, fit_cells_to_axes
from numdaplot.plots.drawing.color_bar import add_color_bar
from numdaplot.plots.drawing.color_scale_values import SCALE_NAMES, find_scale_limits
from numdaplot.plots.drawing.default_labels import COLUMN_LABEL, find_position_label
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.plot_theme import GRID_COLOR
from numdaplot.plots.drawing.position_axis import TRIMMED_ZEROS, place_categories, set_fixed_labels
from numdaplot.plots.drawing.text_contrast import choose_text_color

CELL_DECIMALS = 2
CELL_ASPECT = "auto"
CELL_INTERPOLATION = "nearest"
CENTERED = "center"
MERGED_CELLS_MESSAGE = (
	"A HeatmapChart with {row_count} rows and {column_count} columns does not fit in the image, so each band shows the "
	"mean of its cells. Give a larger ndp.Size, or group the values with Table.aggregate first."
)
UNWRITTEN_VALUES_MESSAGE = " The values of the cells are not written."


def draw_heatmap_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each value as a cell colored along a color scale, the columns side by side and the first row on top.

	When the axes have too few pixels for the cells, each band shows the mean of its cells, missing values left out,
	the color scale follows these means, and the values of the cells are not written.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A HeatmapChart, its row labels and its columns.

	Returns
	-------
	DrawnChart
		The ``labels`` column as default label of the vertical axis, and no grid lines.

	Warns
	-----
	ReadabilityWarning
		When the cells are merged into bands.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.heatmap_drawing import draw_heatmap_chart
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, None]])
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = draw_heatmap_chart(axes, ChartLayer(ndp.HeatmapChart(), read_array_values(grid, "HeatmapChart")))
	>>> axes.images[0].get_array().mask.tolist()
	[[False, False], [False, True]]
	"""
	chart = cast(HeatmapChart, layer.chart)
	values = cast(ChartValues, layer.values)
	grid = stack_columns(values.series)
	shown_cells = fit_cells_to_axes(grid, axes, average_cells)
	cells_are_merged = shown_cells is not grid
	scale_name = SCALE_NAMES[chart.scale]
	base_scale = matplotlib.colormaps[scale_name]
	color_scale = base_scale.with_extremes(bad=GRID_COLOR)
	lowest_color, highest_color = find_scale_limits(shown_cells, chart.scale)
	cell_limits = find_cell_limits(grid)
	# matplotlib paints the NaN cells with the color for missing values of the scale.
	image = axes.imshow(
		shown_cells,
		cmap=color_scale,
		vmin=lowest_color,
		vmax=highest_color,
		aspect=CELL_ASPECT,
		interpolation=CELL_INTERPOLATION,
		extent=cell_limits,
	)
	place_column_names(axes, values.series)
	place_categories(axes, values.positions, True)
	hide_frame(axes)
	scale_label = ""
	if values.value_name is not None:
		scale_label = values.value_name

	add_color_bar(axes, image, scale_label, shown_cells)
	values_are_asked = chart.values == CellValues.SHOWN
	if cells_are_merged:
		warn_merged_cells(grid, values_are_asked)
	elif values_are_asked:
		write_cell_values(axes, image, grid)

	y_label = find_position_label(values.positions)
	drawn_chart = DrawnChart(COLUMN_LABEL, y_label, False, GridAxes.NONE, None)

	return drawn_chart


def warn_merged_cells(grid: NDArray[numpy.float64], values_are_asked: bool) -> None:
	"""
	Warn that a heatmap shows the mean of its cells, and that their values are not written when they were asked for.

	.. versionadded:: 0.1.0

	Parameters
	----------
	grid
		The cells before they are merged.
	values_are_asked
		True when the chart asks for the values of the cells to be written.

	Warns
	-----
	ReadabilityWarning
		Always.

	Examples
	--------
	>>> import numpy
	>>> import warnings
	>>> from numdaplot.plots.drawing.heatmap_drawing import warn_merged_cells
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_merged_cells(numpy.zeros((3000, 2)), False)
	>>> str(caught_warnings[0].message).startswith("A HeatmapChart with 3000 rows and 2 columns")
	True
	"""
	row_count, column_count = grid.shape
	message = MERGED_CELLS_MESSAGE.format(row_count=row_count, column_count=column_count)
	if values_are_asked:
		message = message + UNWRITTEN_VALUES_MESSAGE

	warnings.warn(message, ReadabilityWarning, skip_file_prefixes=INTERNAL_FILES)


def stack_columns(series_list: list[Series]) -> NDArray[numpy.float64]:
	"""
	Return the columns of a chart side by side, as a grid of one row per row and one column per column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	series_list
		The columns, each with one number per row.

	Returns
	-------
	NDArray[numpy.float64]
		The grid of numbers, NaN where a value is missing.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.heatmap_drawing import stack_columns
	>>> stack_columns([Series("jan", numpy.array([1.0, 2.0])), Series("feb", numpy.array([3.0, 4.0]))]).tolist()
	[[1.0, 3.0], [2.0, 4.0]]
	"""
	columns = [series.values for series in series_list]
	grid = numpy.column_stack(columns)

	return grid


def place_column_names(axes: Axes, series_list: list[Series]) -> None:
	"""
	Label each column of cells with its name along the horizontal axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	series_list
		The columns, in the order of the cells.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.drawing.heatmap_drawing import place_column_names
	>>> axes = Figure().add_subplot()
	>>> place_column_names(axes, [Series("jan", numpy.array([1.0])), Series("feb", numpy.array([2.0]))])
	>>> [label.get_text() for label in axes.get_xticklabels()]
	['jan', 'feb']
	"""
	column_names = [series.name for series in series_list]
	column_count = len(column_names)
	coordinates = numpy.arange(column_count, dtype=numpy.float64)
	set_fixed_labels(axes.xaxis, coordinates, column_names)


def hide_frame(axes: Axes) -> None:
	"""
	Hide the lines framing the axes and their tick marks, the cells drawing their own edges.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.heatmap_drawing import hide_frame
	>>> axes = Figure().add_subplot()
	>>> hide_frame(axes)
	>>> axes.spines["left"].get_visible()
	False
	"""
	for spine in axes.spines.values():
		spine.set_visible(False)

	axes.tick_params(length=0)


def write_cell_values(axes: Axes, image: AxesImage, grid: NDArray[numpy.float64]) -> None:
	"""
	Write the value of each cell inside it, in black or white to stay readable over its color.

	A missing value writes nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	image
		The colored cells.
	grid
		The numbers of the cells, NaN where a value is missing.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.heatmap_drawing import write_cell_values
	>>> axes = Figure().add_subplot()
	>>> grid = numpy.array([[1.25, numpy.nan, 3.0]])
	>>> write_cell_values(axes, axes.imshow(grid), grid)
	>>> [text.get_text() for text in axes.texts]
	['1.25', '3']
	"""
	# Some versions of the matplotlib stubs leave the colors given by to_rgba untyped.
	cell_colors = cast(NDArray[numpy.float64], image.to_rgba(grid))

	for (row, column), number in numpy.ndenumerate(grid):
		if numpy.isnan(number):
			continue

		cell_color = cell_colors[row, column].tolist()
		text_color = choose_text_color(cell_color)
		cell_text = format_cell_value(number)
		axes.text(column, row, cell_text, color=text_color, horizontalalignment=CENTERED, verticalalignment=CENTERED)


def format_cell_value(number: float) -> str:
	"""
	Return the text of a cell value, with at most two decimals and no trailing zero.

	.. versionadded:: 0.1.0

	Parameters
	----------
	number
		The value of the cell.

	Returns
	-------
	str
		The value rounded to two decimals.

	Examples
	--------
	>>> from numdaplot.plots.drawing.heatmap_drawing import format_cell_value
	>>> format_cell_value(12.3456), format_cell_value(4.0)
	('12.35', '4')
	"""
	cell_text = numpy.format_float_positional(number, precision=CELL_DECIMALS, trim=TRIMMED_ZEROS)

	return cell_text
