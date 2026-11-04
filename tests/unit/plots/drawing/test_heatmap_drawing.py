"""
Unit tests of the drawing of a HeatmapChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Any, cast

import numpy
import pandas
from matplotlib.colors import to_rgba
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.chart_values import Series
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.heatmap_drawing import (
	draw_heatmap_chart,
	find_scale_limits,
	format_cell_value,
	hide_frame,
	place_column_names,
	stack_columns,
	write_cell_values,
)
from numdaplot.plots.drawing.plot_theme import GRID_COLOR

CHART_NAME = "HeatmapChart"
TEMPERATURES_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", "Lyon"],
		"jan": [5.5, -2.0],
		"feb": [6.0, None],
	}
)
TEMPERATURES = ndp.Table.from_pandas(TEMPERATURES_FRAME)
COLUMNS = ["jan", "feb"]
EXPECTED_CITIES = ["Paris", "Lyon"]
EXPECTED_MASK = [[False, False], [False, True]]
JANUARY = Series("jan", numpy.array([1.0, 2.0]))
FEBRUARY = Series("feb", numpy.array([3.0, 4.0]))
EXPECTED_GRID = [[1.0, 3.0], [2.0, 4.0]]
CHANGES = numpy.array([[-1.0, 4.0], [numpy.nan, 2.0]])
RISES = numpy.array([[1.0, 4.0]])
NO_VALUES = numpy.array([[numpy.nan]])
NO_LIMITS = (None, None)
CELL_GRID = numpy.array([[1.25, numpy.nan, 3.0]])
EXPECTED_CELL_TEXTS = ["1.25", "3"]


def build_layer(chart: ndp.HeatmapChart) -> ChartLayer:
	"""
	Return a HeatmapChart of the city temperatures with its values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart drawn.

	Returns
	-------
	ChartLayer
		The chart, its row labels and its columns.
	"""
	values = read_table_values(TEMPERATURES, "city", COLUMNS, CHART_NAME)
	layer = ChartLayer(chart, values)

	return layer


def test_draw_heatmap_chart_draws_a_cell_per_value_with_the_first_row_on_top() -> None:
	"""
	Check the cells, the masked missing value, the labels and the absence of grid lines.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	drawn_chart = draw_heatmap_chart(axes, build_layer(ndp.HeatmapChart(columns=COLUMNS, labels="city")))

	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	row_labels = [label.get_text() for label in axes.get_yticklabels()]
	bottom, top = axes.get_ylim()
	assert numpy.ma.getmaskarray(cells).tolist() == EXPECTED_MASK
	assert row_labels == EXPECTED_CITIES
	assert top < bottom
	assert drawn_chart.y_label == "city"
	assert drawn_chart.grid_axes == GridAxes.NONE


def test_draw_heatmap_chart_fills_a_missing_cell_with_light_gray() -> None:
	"""
	Check that the color scale paints missing values with the grid color.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_heatmap_chart(axes, build_layer(ndp.HeatmapChart(columns=COLUMNS, labels="city")))

	color_scale = axes.images[0].get_cmap()
	missing_color = color_scale.get_bad().tolist()
	expected_color = list(to_rgba(GRID_COLOR))
	assert missing_color == expected_color


def test_draw_heatmap_chart_adds_a_color_bar() -> None:
	"""
	Check that a color bar is drawn next to the cells.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	draw_heatmap_chart(axes, build_layer(ndp.HeatmapChart(columns=COLUMNS, labels="city")))

	axes_count = len(figure.axes)
	assert axes_count == 2


def test_draw_heatmap_chart_writes_the_values_when_shown() -> None:
	"""
	Check that each present value is written in its cell.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	chart = ndp.HeatmapChart(columns=COLUMNS, labels="city", values=ndp.CellValues.SHOWN)

	draw_heatmap_chart(axes, build_layer(chart))

	cell_texts = [text.get_text() for text in axes.texts]
	assert cell_texts == ["5.5", "6", "-2"]


def test_draw_heatmap_chart_centers_red_blue_on_zero() -> None:
	"""
	Check that RED_BLUE around 0 gets opposite limits.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	chart = ndp.HeatmapChart(columns=COLUMNS, labels="city", scale=ndp.ColorScale.RED_BLUE)

	draw_heatmap_chart(axes, build_layer(chart))

	limits = list(axes.images[0].get_clim())
	assert limits == [-6.0, 6.0]


def test_stack_columns_places_the_columns_side_by_side() -> None:
	"""
	Check that each series becomes a column of the grid.

	.. versionadded:: 0.1.0
	"""
	grid = stack_columns([JANUARY, FEBRUARY])

	assert grid.tolist() == EXPECTED_GRID


def test_find_scale_limits_centers_red_blue_around_zero() -> None:
	"""
	Check that values on both sides of 0 get limits as far from 0 as the furthest value.

	.. versionadded:: 0.1.0
	"""
	limits = find_scale_limits(CHANGES, ndp.ColorScale.RED_BLUE)

	assert limits == (-4.0, 4.0)


def test_find_scale_limits_keeps_red_blue_on_one_side_of_zero() -> None:
	"""
	Check that values all above 0 keep the default limits.

	.. versionadded:: 0.1.0
	"""
	limits = find_scale_limits(RISES, ndp.ColorScale.RED_BLUE)

	assert limits == NO_LIMITS


def test_find_scale_limits_keeps_the_other_scales() -> None:
	"""
	Check that other scales keep the default limits, even around 0.

	.. versionadded:: 0.1.0
	"""
	limits = find_scale_limits(CHANGES, ndp.ColorScale.BLUES)

	assert limits == NO_LIMITS


def test_find_scale_limits_keeps_red_blue_without_values() -> None:
	"""
	Check that a grid without value keeps the default limits.

	.. versionadded:: 0.1.0
	"""
	limits = find_scale_limits(NO_VALUES, ndp.ColorScale.RED_BLUE)

	assert limits == NO_LIMITS


def test_place_column_names_labels_each_column() -> None:
	"""
	Check that each column of cells is labeled with its name.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	place_column_names(axes, [JANUARY, FEBRUARY])

	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert column_labels == COLUMNS


def test_hide_frame_hides_every_border() -> None:
	"""
	Check that no border of the axes stays visible.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	hide_frame(axes)

	visible_borders = [spine for spine in axes.spines.values() if spine.get_visible()]
	assert visible_borders == []


def test_write_cell_values_skips_the_missing_values() -> None:
	"""
	Check that only present values are written.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	image = axes.imshow(CELL_GRID)

	write_cell_values(axes, image, CELL_GRID)

	cell_texts = [text.get_text() for text in axes.texts]
	assert cell_texts == EXPECTED_CELL_TEXTS


def test_format_cell_value_rounds_to_two_decimals() -> None:
	"""
	Check that a value keeps at most two decimals.

	.. versionadded:: 0.1.0
	"""
	cell_text = format_cell_value(12.3456)

	assert cell_text == "12.35"


def test_format_cell_value_drops_trailing_zeros() -> None:
	"""
	Check that a whole value is written without decimals.

	.. versionadded:: 0.1.0
	"""
	cell_text = format_cell_value(4.0)

	assert cell_text == "4"
