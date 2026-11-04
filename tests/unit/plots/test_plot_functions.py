"""
Unit tests of plot_line, plot_bar and plot_scatter.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import pytest

import numdaplot as ndp
from numdaplot.plots.plot_bar import plot_bar
from numdaplot.plots.plot_line import plot_line
from numdaplot.plots.plot_scatter import plot_scatter, read_scatter_layer

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "city": CITIES})
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
TWO_COLORS = [ndp.Color.RED, ndp.Color.BLUE]


def test_plot_line_uses_the_default_style_when_omitted() -> None:
	"""
	Check that a Plot without style has no title and the default size.

	.. versionadded:: 0.1.0
	"""
	plot = plot_line(SALES, ndp.LineChart(x="day", y=["price"]))

	figure = plot.to_matplotlib()
	inches = figure.get_size_inches().tolist()
	assert figure.axes[0].get_title() == ""
	assert inches == [6.4, 4.8]


def test_plot_line_rejects_colors_not_one_per_series_when_created() -> None:
	"""
	Check that two colors for one line raise InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.LineChart(x="day", y=["price"], colors=TWO_COLORS)

	with pytest.raises(ndp.InvalidColorCountError):
		plot_line(SALES, chart)


def test_plot_bar_rejects_a_table_without_y() -> None:
	"""
	Check that a Table needs y.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		plot_bar(SALES, ndp.BarChart(x="city"))


def test_plot_bar_rejects_colors_not_one_per_series_when_created() -> None:
	"""
	Check that two colors for one series of bars raise InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		plot_bar(PRICES, ndp.BarChart(colors=TWO_COLORS))


def test_plot_scatter_reads_the_color_values_of_a_table() -> None:
	"""
	Check that a ScatterChart of a Table keeps the values of its color_by column.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="day", y="price", color_by="city")

	layer = read_scatter_layer(SALES, chart)

	assert layer.points is not None
	assert layer.points.color_name == "city"


def test_plot_scatter_rejects_a_table_without_y() -> None:
	"""
	Check that a Table needs y.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		plot_scatter(SALES, ndp.ScatterChart(x="day"))


def test_plot_scatter_rejects_color_by_for_an_array() -> None:
	"""
	Check that an Array takes no color_by.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		plot_scatter(PRICES, ndp.ScatterChart(color_by="city"))


def test_plot_scatter_rejects_one_color_for_several_array_columns() -> None:
	"""
	Check that one color for an Array of two columns raises InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		plot_scatter(GRID, ndp.ScatterChart(color=ndp.Color.RED))


def test_plot_scatter_accepts_one_color_for_a_single_array_column() -> None:
	"""
	Check that one color for a one-dimensional Array is accepted.

	.. versionadded:: 0.1.0
	"""
	layer = read_scatter_layer(PRICES, ndp.ScatterChart(color=ndp.Color.RED))

	assert layer.points is None
