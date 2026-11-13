"""
Unit tests of the drawing of a HistogramChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from datetime import time, timedelta

import numpy
import pytest
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import numdaplot as ndp
from numdaplot.errors.plots.invalid_color_count_error import InvalidColorCountError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.axes.grid_axes import GridAxes
from numdaplot.plots.drawing.charts.histogram_drawing import (
	OVERLAID_OPACITY,
	draw_histogram_chart,
	find_bin_edges,
	find_bin_weights,
	find_width_edges,
	read_width_hours,
	require_bins_on_values,
)
from numdaplot.plots.layers.chart_layer import ChartLayer

CHART_NAME = "HistogramChart"
PRICES = ndp.Array.from_list([12.0, 13.0, 17.0, None])
TWO_COLUMNS = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
FIVE_WIDTH = ndp.BinWidth(5.0)
FOUR_BINS = ndp.BinCount(4)
WIDE_NUMBERS = numpy.array([12.0, 21.0])
EXPECTED_COUNTS = [2.0, 1.0]
EXPECTED_RATIOS = [2 / 3, 1 / 3]
SPREAD_NUMBERS = numpy.array([12.0, 20.0])
EXPECTED_COUNT_EDGES = [12.0, 14.0, 16.0, 18.0, 20.0]
EXPECTED_WIDTH_EDGES = [10.0, 15.0, 20.0, 25.0]
NEGATIVE_NUMBERS = numpy.array([-7.0, -1.0])
EXPECTED_NEGATIVE_EDGES = [-10.0, -5.0, 0.0]
EQUAL_NUMBERS = numpy.array([10.0, 10.0])
EXPECTED_EQUAL_EDGES = [10.0, 15.0]
NO_NUMBERS = numpy.array([], dtype=numpy.float64)
EXPECTED_EMPTY_EDGES = [0.0, 5.0]
FOUR_NUMBERS = numpy.array([3.0, 5.0, 8.0, 9.0])
WIDTH = 5.0
HALF_HOUR_WIDTH = ndp.BinWidth(timedelta(minutes=30))
HALF_HOUR = 0.5
DAY_EDGE_COUNT = 25
DEFAULT_NUMBER_EDGE_COUNT = 11
MORNING_NUMBERS = numpy.array([8.25, 9.75])
EXPECTED_HALF_HOUR_EDGES = [8.0, 8.5, 9.0, 9.5, 10.0]
EXPECTED_MORNING_COUNT_EDGES = [8.25, 8.625, 9.0, 9.375, 9.75]
HISTOGRAM_HOURS = ndp.Array.from_list([time(8), time(9, 30)])
HISTOGRAM_HALF_PAST_EIGHT = 8.5
EXPECTED_HISTOGRAM_HOUR_LABEL = "08:30"


def build_layer(chart: ndp.HistogramChart, data: ndp.Array) -> ChartLayer:
	"""
	Return a HistogramChart with the values of an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart drawn.
	data
		The Array drawn.

	Returns
	-------
	ChartLayer
		The chart and its columns.
	"""
	samples = read_sample_values(data, None, None, CHART_NAME)
	layer = ChartLayer(chart, samples)

	return layer


def read_bar_heights(figure: Figure) -> list[float]:
	"""
	Return the height of each bar drawn on the first axes of a figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		A figure with a histogram.

	Returns
	-------
	list[float]
		The heights, in the order of the bars.
	"""
	bars = [patch for patch in figure.axes[0].patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]

	return heights


def test_draw_histogram_chart_counts_the_values_of_each_bin() -> None:
	"""
	Check that each bin is as high as its number of values, missing values left out.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	layer = build_layer(ndp.HistogramChart(bins=FIVE_WIDTH), PRICES)

	drawn_chart = draw_histogram_chart(axes, layer)

	heights = read_bar_heights(figure)
	assert heights == EXPECTED_COUNTS
	assert drawn_chart.y_label == "Count"
	assert drawn_chart.grid_axes == GridAxes.VALUES


def test_draw_histogram_chart_gives_the_share_of_each_bin_for_ratios() -> None:
	"""
	Check that the bins of a ratio histogram add up to 1.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	layer = build_layer(ndp.HistogramChart(bins=FIVE_WIDTH, measure=ndp.Measure.RATIO), PRICES)

	drawn_chart = draw_histogram_chart(axes, layer)

	heights = read_bar_heights(figure)
	assert heights == pytest.approx(EXPECTED_RATIOS)
	assert drawn_chart.y_label == "Ratio"


def test_draw_histogram_chart_overlays_several_columns_half_transparent() -> None:
	"""
	Check that two columns share the bins and are half transparent.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	layer = build_layer(ndp.HistogramChart(bins=ndp.BinCount(2)), TWO_COLUMNS)

	draw_histogram_chart(axes, layer)

	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	opacities = {bar.get_alpha() for bar in bars}
	assert opacities == {OVERLAID_OPACITY}
	assert len(bars) == 4


def test_draw_histogram_chart_rejects_colors_not_one_per_column() -> None:
	"""
	Check that one color for two columns raises InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	layer = build_layer(ndp.HistogramChart(colors=[ndp.Color.RED]), TWO_COLUMNS)

	with pytest.raises(InvalidColorCountError):
		draw_histogram_chart(axes, layer)


def test_find_bin_edges_spreads_a_bin_count_over_the_values() -> None:
	"""
	Check that a number of bins splits the range of the values evenly.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(SPREAD_NUMBERS, FOUR_BINS, ndp.Type.FLOAT64)

	edge_list = edges.tolist()
	assert edge_list == EXPECTED_COUNT_EDGES


def test_find_bin_edges_uses_the_width_of_bin_width() -> None:
	"""
	Check that a width gives edges on its multiples.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(WIDE_NUMBERS, FIVE_WIDTH, ndp.Type.FLOAT64)

	edge_list = edges.tolist()
	assert edge_list == EXPECTED_WIDTH_EDGES


def test_find_width_edges_starts_below_negative_numbers() -> None:
	"""
	Check that negative numbers start on the multiple below them.

	.. versionadded:: 0.1.0
	"""
	edges = find_width_edges(NEGATIVE_NUMBERS, WIDTH)

	assert edges.tolist() == EXPECTED_NEGATIVE_EDGES


def test_find_width_edges_gives_one_bin_to_equal_numbers() -> None:
	"""
	Check that numbers all equal still get one bin.

	.. versionadded:: 0.1.0
	"""
	edges = find_width_edges(EQUAL_NUMBERS, WIDTH)

	assert edges.tolist() == EXPECTED_EQUAL_EDGES


def test_find_width_edges_starts_at_zero_without_numbers() -> None:
	"""
	Check that a column without value gets a single bin from 0.

	.. versionadded:: 0.1.0
	"""
	edges = find_width_edges(NO_NUMBERS, WIDTH)

	assert edges.tolist() == EXPECTED_EMPTY_EDGES


def test_find_bin_weights_counts_each_number_once() -> None:
	"""
	Check that counts need no weight.

	.. versionadded:: 0.1.0
	"""
	weights = find_bin_weights(FOUR_NUMBERS, ndp.Measure.COUNT)

	assert weights is None


def test_find_bin_weights_shares_out_one_for_ratios() -> None:
	"""
	Check that each number weighs its share of the column.

	.. versionadded:: 0.1.0
	"""
	weights = find_bin_weights(FOUR_NUMBERS, ndp.Measure.RATIO)

	assert weights is not None
	assert weights.tolist() == [0.25, 0.25, 0.25, 0.25]


def test_find_bin_weights_needs_no_weight_without_numbers() -> None:
	"""
	Check that a column without value has no ratio to share out.

	.. versionadded:: 0.1.0
	"""
	weights = find_bin_weights(NO_NUMBERS, ndp.Measure.RATIO)

	assert weights is None


@pytest.mark.parametrize(
	("bins", "value_type"),
	[
		(None, ndp.Type.TIME),
		(FOUR_BINS, ndp.Type.TIME),
		(FIVE_WIDTH, ndp.Type.INT64),
		(HALF_HOUR_WIDTH, ndp.Type.TIME),
	],
)
def test_require_bins_on_values_accepts_a_width_of_the_kind_of_the_values(
	bins: ndp.BinCount | ndp.BinWidth | None, value_type: ndp.Type
) -> None:
	"""
	Check that default bins, a number of bins, a number for numbers and a duration for times are accepted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bins
		The bins of the chart.
	value_type
		The type of the values.
	"""
	require_bins_on_values(bins, value_type)


@pytest.mark.parametrize(("bins", "value_type"), [(FIVE_WIDTH, ndp.Type.TIME), (HALF_HOUR_WIDTH, ndp.Type.FLOAT64)])
def test_require_bins_on_values_rejects_a_width_of_another_kind(bins: ndp.BinWidth, value_type: ndp.Type) -> None:
	"""
	Check that a number for times of day and a duration for numbers raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bins
		The width of the bins.
	value_type
		The type of the values.
	"""
	with pytest.raises(IncompatibleTypesError):
		require_bins_on_values(bins, value_type)


def test_find_bin_edges_splits_the_day_in_hours_by_default_for_times() -> None:
	"""
	Check that times of day without bins give one bin per hour from 00:00 to 24:00.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(MORNING_NUMBERS, None, ndp.Type.TIME)

	edge_count = len(edges)
	first_edge = edges[0]
	last_edge = edges[-1]
	assert edge_count == DAY_EDGE_COUNT
	assert first_edge == 0.0
	assert last_edge == DAY_EDGE_COUNT - 1


def test_find_bin_edges_gives_ten_bins_by_default_for_numbers() -> None:
	"""
	Check that numbers without bins give ten bins.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(SPREAD_NUMBERS, None, ndp.Type.FLOAT64)

	edge_count = len(edges)
	assert edge_count == DEFAULT_NUMBER_EDGE_COUNT


def test_find_bin_edges_uses_a_duration_from_the_smallest_to_the_largest_time() -> None:
	"""
	Check that a duration gives edges on its multiples, from the smallest to the largest time.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(MORNING_NUMBERS, HALF_HOUR_WIDTH, ndp.Type.TIME)

	edge_list = edges.tolist()
	assert edge_list == EXPECTED_HALF_HOUR_EDGES


def test_find_bin_edges_spreads_a_bin_count_over_the_times() -> None:
	"""
	Check that a number of bins splits the span of the times evenly.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(MORNING_NUMBERS, FOUR_BINS, ndp.Type.TIME)

	edge_list = edges.tolist()
	assert edge_list == EXPECTED_MORNING_COUNT_EDGES


@pytest.mark.parametrize(("bins", "expected_width"), [(HALF_HOUR_WIDTH, HALF_HOUR), (FIVE_WIDTH, WIDTH)])
def test_read_width_hours_counts_a_duration_in_hours(bins: ndp.BinWidth, expected_width: float) -> None:
	"""
	Check that a duration gives its hours and a number stays as it is.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bins
		The width of the bins.
	expected_width
		The width as a number.
	"""
	width = read_width_hours(bins)

	assert width == expected_width


def test_draw_histogram_chart_labels_the_axis_of_times_hh_mm() -> None:
	"""
	Check that a histogram of times of day labels its horizontal axis HH:MM.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	samples = read_sample_values(HISTOGRAM_HOURS, None, None, CHART_NAME)
	layer = ChartLayer(ndp.HistogramChart(), samples)

	draw_histogram_chart(axes, layer)

	formatter = axes.xaxis.get_major_formatter()
	hour_label = formatter(HISTOGRAM_HALF_PAST_EIGHT)
	assert hour_label == EXPECTED_HISTOGRAM_HOUR_LABEL
