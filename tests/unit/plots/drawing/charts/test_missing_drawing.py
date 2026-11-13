"""
Unit tests of the drawing of the missing values of a Table.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Any, cast

import numpy
import pandas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import numdaplot as ndp
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.data.missing_cells import read_missing_cells, read_missing_counts
from numdaplot.plots.drawing.axes.grid_axes import GridAxes
from numdaplot.plots.drawing.charts.missing_drawing import (
	ONE_LINE_BAR_LABEL,
	PRESENT_LABEL,
	add_legend_swatch,
	draw_missing_chart,
	draw_missing_map,
	find_axis_top,
	format_bar_labels,
)
from numdaplot.plots.layers.chart_layer import ChartLayer

FLATS_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", None, "Pau"],
		"price": [12.0, None, None],
		"rooms": [2.0, 3.0, 1.0],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
EXPECTED_COLUMNS = ["city", "price", "rooms"]
EXPECTED_COUNTS = [1.0, 2.0, 0.0]
EXPECTED_MAP = [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
SWATCH_COLOR = "#33415c"
EXPECTED_STACKED_LABELS = ["1\n33.3 %", "2\n66.7 %", "0\n0.0 %"]
EXPECTED_MISSING_TOTAL_LABEL = "Missing (3)"
EXPECTED_UPWARD_LABEL = "1 (50.0 %)"
UPWARD_ROTATION = 90.0
NARROW_COLUMN_COUNT = 30
EXPECTED_EMPTY_TABLE_LABELS = ["0 (0.0 %)"]
EXPECTED_RATIO_TOP_TICK = 1.0
MANY_COLUMN_NAMES = [f"column_{i}" for i in range(50)]
TOO_MANY_COLUMN_NAMES = [f"column_{i}" for i in range(200)]
AXES_HEIGHT = 400.0
COMPLETE_PRICES = [1.0, 2.0]
BAR_TOP = 30.0
LABEL_HEIGHT = 40.0
EXPECTED_AXIS_TOP = 33.333333333333336
HIGHEST_AXIS_TOP = 60.0
TALLER_THAN_AXES_LABEL = 900.0


def draw_counts(measure: ndp.Measure) -> Figure:
	"""
	Return a figure with the missing values of each column of the flats drawn as bars.

	.. versionadded:: 0.1.0

	Parameters
	----------
	measure
		Counts or ratios.

	Returns
	-------
	Figure
		The figure drawn.
	"""
	figure = Figure()
	axes = figure.add_subplot()
	chart = ndp.MissingChart(measure=measure)
	values = read_missing_counts(FLATS, measure)
	draw_missing_chart(axes, ChartLayer(chart, values))

	return figure


def test_draw_missing_chart_draws_one_bar_per_column() -> None:
	"""
	Check that each column gets a bar labeled with its name, even without missing value.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.COUNT)

	axes = figure.axes[0]
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert heights == EXPECTED_COUNTS
	assert column_labels == EXPECTED_COLUMNS


def test_draw_missing_chart_places_ratio_ticks_up_to_one() -> None:
	"""
	Check that the ticks of the ratios stop at 1, the axis leaving room for the labels above.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.RATIO)

	axes = figure.axes[0]
	# Some versions of the matplotlib stubs leave the ticks untyped.
	ticks = cast(NDArray[numpy.float64], axes.get_yticks())
	_, axis_top = axes.get_ylim()
	assert float(ticks[-1]) == EXPECTED_RATIO_TOP_TICK
	assert axis_top > EXPECTED_RATIO_TOP_TICK


def test_draw_missing_chart_labels_each_bar_with_its_count_and_percentage() -> None:
	"""
	Check two lines above each bar, even without missing value.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.COUNT)

	labels = [text.get_text() for text in figure.axes[0].texts]
	assert labels == EXPECTED_STACKED_LABELS


def test_draw_missing_chart_shows_both_numbers_on_ratio_bars() -> None:
	"""
	Check that the labels stay the same when the bars show ratios.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.RATIO)

	labels = [text.get_text() for text in figure.axes[0].texts]
	assert labels == EXPECTED_STACKED_LABELS


def draw_named_columns(column_names: list[str]) -> Figure:
	"""
	Return a figure with the bars of a Table holding the given columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The names of the columns.

	Returns
	-------
	Figure
		The figure drawn.
	"""
	figure = Figure()
	axes = figure.add_subplot()
	columns = {column_name: [1.0, None] for column_name in column_names}
	frame = pandas.DataFrame(columns)
	table = ndp.Table.from_pandas(frame)
	values = read_missing_counts(table, ndp.Measure.COUNT)
	draw_missing_chart(axes, ChartLayer(ndp.MissingChart(), values))

	return figure


def test_draw_missing_chart_writes_labels_upwards_on_narrow_bars() -> None:
	"""
	Check that narrow bars get one line rotated upwards.

	.. versionadded:: 0.1.0
	"""
	figure = draw_named_columns(MANY_COLUMN_NAMES[:NARROW_COLUMN_COUNT])

	first_label = figure.axes[0].texts[0]
	assert first_label.get_text() == EXPECTED_UPWARD_LABEL
	assert first_label.get_rotation() == UPWARD_ROTATION


def test_draw_missing_chart_leaves_out_labels_on_too_narrow_bars() -> None:
	"""
	Check that bars without room for a line get no label.

	.. versionadded:: 0.1.0
	"""
	figure = draw_named_columns(TOO_MANY_COLUMN_NAMES)

	label_count = len(figure.axes[0].texts)
	assert label_count == 0


def test_format_bar_labels_gives_zero_percent_without_rows() -> None:
	"""
	Check that a Table without rows does not divide by zero.

	.. versionadded:: 0.1.0
	"""
	empty_frame = pandas.DataFrame({"price": pandas.Series([], dtype="float64")})
	table = ndp.Table.from_pandas(empty_frame)
	values = read_missing_counts(table, ndp.Measure.COUNT)

	labels = format_bar_labels(values, ONE_LINE_BAR_LABEL)

	assert labels == EXPECTED_EMPTY_TABLE_LABELS


def test_find_axis_top_leaves_the_room_of_the_labels() -> None:
	"""
	Check that the labels take their share of the axes above the highest bar.

	.. versionadded:: 0.1.0
	"""
	axis_top = find_axis_top(BAR_TOP, LABEL_HEIGHT, AXES_HEIGHT)

	assert axis_top == EXPECTED_AXIS_TOP


def test_find_axis_top_keeps_half_of_the_axes_for_the_bars() -> None:
	"""
	Check that labels taller than the axes leave the bars half of them.

	.. versionadded:: 0.1.0
	"""
	axis_top = find_axis_top(BAR_TOP, TALLER_THAN_AXES_LABEL, AXES_HEIGHT)

	assert axis_top == HIGHEST_AXIS_TOP


def test_draw_missing_chart_places_counts_on_whole_ticks() -> None:
	"""
	Check that every tick of the counts is a whole number.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.COUNT)

	# Some versions of the matplotlib stubs leave the ticks untyped.
	ticks = cast(NDArray[numpy.float64], figure.axes[0].get_yticks())
	whole_ticks = [float(tick).is_integer() for tick in ticks]
	assert all(whole_ticks)


def test_draw_missing_map_draws_a_cell_per_value() -> None:
	"""
	Check that each value is a cell, 1 where missing, without grid lines.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_missing_map(axes, ChartLayer(MissingMapChart(), read_missing_cells(FLATS)))

	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert cells.tolist() == EXPECTED_MAP
	assert column_labels == EXPECTED_COLUMNS
	assert drawn_chart.y_label == "Row"
	assert drawn_chart.grid_axes == GridAxes.NONE


def test_draw_missing_map_names_both_colors_in_the_legend() -> None:
	"""
	Check that the legend names both colors and gives the total of missing values.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_missing_map(axes, ChartLayer(MissingMapChart(), read_missing_cells(FLATS)))

	_, legend_labels = axes.get_legend_handles_labels()
	assert legend_labels == [EXPECTED_MISSING_TOTAL_LABEL, PRESENT_LABEL]


def test_add_legend_swatch_draws_nothing_visible() -> None:
	"""
	Check that the swatch has no size, so it draws nothing on the axes.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	add_legend_swatch(axes, SWATCH_COLOR, EXPECTED_MISSING_TOTAL_LABEL)

	swatch = axes.patches[0]
	assert isinstance(swatch, Rectangle)
	assert swatch.get_width() == 0
	assert swatch.get_height() == 0
	assert numpy.isnan(swatch.get_x())


def test_draw_missing_chart_keeps_room_above_bars_of_zero() -> None:
	"""
	Check that a Table without missing value still gets a count axis above zero.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(COMPLETE_PRICES)
	complete_flats = ndp.Table.from_arrays({"price": prices})
	axes = Figure().add_subplot()
	values = read_missing_counts(complete_flats, ndp.Measure.COUNT)

	draw_missing_chart(axes, ChartLayer(ndp.MissingChart(), values))

	axis_top = axes.get_ylim()[1]
	assert axis_top > 0
