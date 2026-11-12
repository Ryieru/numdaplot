"""
Unit tests of the creation of a Plot showing how values are spread or shared out.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings
from typing import Any, cast

import pytest

import numdaplot as ndp

DAYS = ndp.Array.from_list([1, 2, 3])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "city": CITIES})
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
TWO_COLORS = [ndp.Color.RED, ndp.Color.BLUE]
CITY_TOTALS = ndp.Table.from_arrays(
	{"city": ndp.Array.from_list(["Paris", "Lyon"]), "sales": ndp.Array.from_list([120.0, 80.0])}
)
PIE_CHART = ndp.PieChart(labels="city", values="sales")
FRUITS = ndp.Array.from_list(["apple", "pear", "plum", "fig", "kiwi", "lime"])
FRUIT_SALES = ndp.Array.from_list([30.0, 25.0, 15.0, 12.0, 10.0, 8.0])
FRUIT_SHARES = ndp.Table.from_arrays({"fruit": FRUITS, "sales": FRUIT_SALES})


def test_plot_histogram_rejects_a_table_without_columns() -> None:
	"""
	Check that a Table needs columns.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		ndp.Plot.histogram(SALES, ndp.HistogramChart())


def test_plot_histogram_rejects_colors_not_one_per_column_when_created() -> None:
	"""
	Check that two colors for one column raise InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		ndp.Plot.histogram(PRICES, ndp.HistogramChart(colors=TWO_COLORS))


def test_plot_histogram_draws_with_the_default_style() -> None:
	"""
	Check that a histogram without style has its default title.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.histogram(SALES, ndp.HistogramChart(columns=["price"]))

	figure = plot.to_matplotlib()
	plot_title = figure.get_suptitle()
	assert plot_title == "Count by price"


def test_plot_box_rejects_group_by_for_an_array() -> None:
	"""
	Check that an Array takes no group_by.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		ndp.Plot.box(GRID, ndp.BoxChart(group_by="city"))


def test_plot_box_rejects_colors_not_one_per_column_when_created() -> None:
	"""
	Check that one color for two Array columns raises InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		ndp.Plot.box(GRID, ndp.BoxChart(colors=[ndp.Color.RED]))


def test_plot_pie_rejects_an_array() -> None:
	"""
	Check that an Array raises InvalidTypeError, even untyped.

	.. versionadded:: 0.1.0
	"""
	untyped_plot_pie = cast(Any, ndp.Plot.pie)

	with pytest.raises(ndp.InvalidTypeError):
		untyped_plot_pie(PRICES, ndp.PieChart(labels="city", values="price"))


def test_plot_pie_rejects_colors_not_one_per_slice_when_created() -> None:
	"""
	Check that one color for two slices raises InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="city", values="sales", colors=[ndp.Color.RED])

	with pytest.raises(ndp.InvalidColorCountError):
		ndp.Plot.pie(CITY_TOTALS, chart)


def test_plot_pie_rejects_an_axis_label() -> None:
	"""
	Check that a style with a y_label raises RefusedSettingError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="y_label"):
		ndp.Plot.pie(CITY_TOTALS, PIE_CHART, ndp.PlotStyle(y_label="Sales"))


def test_plot_pie_warns_beyond_five_slices() -> None:
	"""
	Check that 6 slices emit a ReadabilityWarning pointing at the caller.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="fruit", values="sales")

	with pytest.warns(ndp.ReadabilityWarning) as caught_warnings:
		ndp.Plot.pie(FRUIT_SHARES, chart)

	warned_file = caught_warnings[0].filename
	assert warned_file == __file__


def test_plot_pie_is_silent_up_to_five_slices() -> None:
	"""
	Check that 2 slices emit no warning.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		ndp.Plot.pie(CITY_TOTALS, PIE_CHART)

	assert caught_warnings == []
