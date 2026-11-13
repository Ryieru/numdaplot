"""
Unit tests of the colors of the charts overlaid on a Plot.

.. versionadded:: 0.1.0
"""

import warnings

import pytest

import numdaplot as ndp
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.drawing.layer_colors import continue_color_cycle, give_cycle_colors

PRICES = ndp.Array.from_list([12.0, 15.5])
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
BARS = ChartLayer(ndp.BarChart(), read_array_values(GRID, "BarChart"))
LINE = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
RED_LINE = ChartLayer(ndp.LineChart(colors=[ndp.Color.RED]), read_array_values(PRICES, "LineChart"))
POINTS = ChartLayer(ndp.ScatterChart(), read_array_values(PRICES, "ScatterChart"))
GRID_POINTS = ChartLayer(ndp.ScatterChart(), read_array_values(GRID, "ScatterChart"))
WIDE_GRID = ndp.Array.filled(ndp.Shape([2, 20]), 1.0)
WIDE_GRID_VALUES = read_array_values(WIDE_GRID, "BarChart")
WIDE_BARS = ChartLayer(ndp.BarChart(), WIDE_GRID_VALUES)


def test_continue_color_cycle_gives_the_next_colors_to_each_chart() -> None:
	"""
	Check that two series of bars, then a line, then points take the next colors of the cycle.

	.. versionadded:: 0.1.0
	"""
	bars, line, points = continue_color_cycle([BARS, LINE, POINTS])

	assert isinstance(bars.chart, BarChart)
	assert isinstance(line.chart, LineChart)
	assert isinstance(points.chart, ScatterChart)
	assert bars.chart.colors is None
	assert line.chart.colors == [ndp.Color.GREEN]
	assert points.chart.color == ndp.Color.RED


def test_continue_color_cycle_keeps_chosen_colors() -> None:
	"""
	Check that a chart with chosen colors keeps them, and still uses its place in the cycle.

	.. versionadded:: 0.1.0
	"""
	_, red_line, line = continue_color_cycle([LINE, RED_LINE, LINE])

	assert isinstance(red_line.chart, LineChart)
	assert isinstance(line.chart, LineChart)
	assert red_line.chart.colors == [ndp.Color.RED]
	assert line.chart.colors == [ndp.Color.GREEN]


def test_give_cycle_colors_keeps_the_first_chart() -> None:
	"""
	Check that a chart starting the cycle keeps the default colors.

	.. versionadded:: 0.1.0
	"""
	colored_layer = give_cycle_colors(LINE, 0, 1)

	assert colored_layer is LINE


def test_give_cycle_colors_keeps_several_series_of_points() -> None:
	"""
	Check that points of several series, which take no single color, keep the default ones.

	.. versionadded:: 0.1.0
	"""
	colored_layer = give_cycle_colors(GRID_POINTS, 1, 2)

	assert colored_layer is GRID_POINTS


def test_continue_color_cycle_warns_when_the_charts_share_colors() -> None:
	"""
	Check that 20 bars and a line, 21 series in all, raise a ReadabilityWarning.

	.. versionadded:: 0.2.0
	"""
	with pytest.warns(ReadabilityWarning):
		continue_color_cycle([WIDE_BARS, LINE])


def test_continue_color_cycle_leaves_the_warning_of_a_single_chart_to_its_drawing() -> None:
	"""
	Check that a single chart of 20 series gives no warning here.

	.. versionadded:: 0.2.0
	"""
	with warnings.catch_warnings():
		warnings.simplefilter("error")
		continue_color_cycle([WIDE_BARS])
