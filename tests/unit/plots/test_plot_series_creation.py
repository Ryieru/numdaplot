"""
Unit tests of the creation of a Plot of lines, bars or points.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import pytest

import numdaplot as ndp

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "city": CITIES})
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
TWO_COLORS = [ndp.Color.RED, ndp.Color.BLUE]


def test_plot_line_uses_the_default_style_when_omitted() -> None:
	"""
	Check that a Plot without style has its default title and size.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.line(SALES, ndp.LineChart(x="day", y=["price"]))

	figure = plot.to_matplotlib()
	inches = figure.get_size_inches().tolist()
	assert figure.axes[0].get_title() == "price by day"
	assert inches == [6.4, 4.8]


def test_plot_line_rejects_colors_not_one_per_series_when_created() -> None:
	"""
	Check that two colors for one line raise InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.LineChart(x="day", y=["price"], colors=TWO_COLORS)

	with pytest.raises(ndp.InvalidColorCountError):
		ndp.Plot.line(SALES, chart)


def test_plot_bar_rejects_a_table_without_y() -> None:
	"""
	Check that a Table needs y.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		ndp.Plot.bar(SALES, ndp.BarChart(x="city"))


def test_plot_bar_rejects_colors_not_one_per_series_when_created() -> None:
	"""
	Check that two colors for one series of bars raise InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		ndp.Plot.bar(PRICES, ndp.BarChart(colors=TWO_COLORS))


def test_plot_scatter_rejects_a_table_without_y() -> None:
	"""
	Check that a Table needs y.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		ndp.Plot.scatter(SALES, ndp.ScatterChart(x="day"))


def test_plot_scatter_rejects_color_by_for_an_array() -> None:
	"""
	Check that an Array takes no color_by.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		ndp.Plot.scatter(PRICES, ndp.ScatterChart(color_by="city"))


def test_plot_scatter_rejects_one_color_for_several_array_columns() -> None:
	"""
	Check that one color for an Array of two columns raises InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		ndp.Plot.scatter(GRID, ndp.ScatterChart(color=ndp.Color.RED))
