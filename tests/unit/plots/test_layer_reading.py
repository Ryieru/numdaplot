"""
Unit tests of the reading of the charts a Plot draws on its axes.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.layer_reading import build_series_layer, read_bar_layer, read_line_layer, read_scatter_layer

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "city": CITIES})
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
TWO_COLORS = [ndp.Color.RED, ndp.Color.BLUE]
HISTOGRAM_NAME = "HistogramChart"


def test_read_line_layer_reads_the_columns_of_a_table() -> None:
	"""
	Check that each y column is a series at the x values.

	.. versionadded:: 0.1.0
	"""
	layer = read_line_layer(SALES, ndp.LineChart(x="day", y=["price"]))

	assert layer.values.series[0].name == "price"
	assert layer.value_axis == ndp.ValueAxis.LEFT


def test_read_line_layer_rejects_colors_not_one_per_line() -> None:
	"""
	Check that two colors for one line raise InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		read_line_layer(SALES, ndp.LineChart(x="day", y=["price"], colors=TWO_COLORS))


def test_read_bar_layer_reads_each_column_of_an_array() -> None:
	"""
	Check that each column of an Array is a series of bars.

	.. versionadded:: 0.1.0
	"""
	layer = read_bar_layer(GRID, ndp.BarChart())

	series_count = len(layer.values.series)
	assert series_count == 2


def test_read_bar_layer_rejects_a_table_without_y() -> None:
	"""
	Check that a Table needs y.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		read_bar_layer(SALES, ndp.BarChart(x="city"))


def test_read_scatter_layer_reads_the_color_values_of_a_table() -> None:
	"""
	Check that a ScatterChart of a Table keeps the values of its color_by column.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="day", y="price", color_by="city")

	layer = read_scatter_layer(SALES, chart)

	assert layer.points is not None
	assert layer.points.color_name == "city"


def test_read_scatter_layer_accepts_one_color_for_a_single_array_column() -> None:
	"""
	Check that one color for a one-dimensional Array is accepted, without point values.

	.. versionadded:: 0.1.0
	"""
	layer = read_scatter_layer(PRICES, ndp.ScatterChart(color=ndp.Color.RED))

	assert layer.points is None


def test_build_series_layer_keeps_the_chart_and_its_values() -> None:
	"""
	Check that the layer holds the chart and the series it was given.

	.. versionadded:: 0.2.0
	"""
	chart = ndp.HistogramChart(columns=["price"])
	values = read_sample_values(SALES, chart.columns, None, HISTOGRAM_NAME)

	layer = build_series_layer(chart, values)

	assert layer.chart is chart
	assert layer.values is values


def test_build_series_layer_rejects_colors_not_one_per_series() -> None:
	"""
	Check that two colors for one column raise InvalidColorCountError.

	.. versionadded:: 0.2.0
	"""
	chart = ndp.HistogramChart(columns=["price"], colors=TWO_COLORS)
	values = read_sample_values(SALES, chart.columns, None, HISTOGRAM_NAME)

	with pytest.raises(ndp.InvalidColorCountError):
		build_series_layer(chart, values)
