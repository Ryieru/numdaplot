"""
Unit tests of the drawing of a HistogramChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
import pytest
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import numdaplot as ndp
from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.histogram_drawing import (
	OVERLAID_OPACITY,
	draw_histogram_chart,
	find_bin_edges,
	find_bin_weights,
	find_width_edges,
)

CHART_NAME = "HistogramChart"
PRICES = ndp.Array.from_list([12.0, 13.0, 17.0, None])
TWO_COLUMNS = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
FIVE_WIDTH = ndp.BinWidth(5.0)
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
	edges = find_bin_edges(SPREAD_NUMBERS, ndp.BinCount(4))

	assert edges.tolist() == EXPECTED_COUNT_EDGES


def test_find_bin_edges_uses_the_width_of_bin_width() -> None:
	"""
	Check that a width gives edges on its multiples.

	.. versionadded:: 0.1.0
	"""
	edges = find_bin_edges(numpy.array([12.0, 21.0]), FIVE_WIDTH)

	assert edges.tolist() == EXPECTED_WIDTH_EDGES


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
