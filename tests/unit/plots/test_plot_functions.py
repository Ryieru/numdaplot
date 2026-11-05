"""
Unit tests of the plot_* functions.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings
from collections.abc import Callable
from typing import Any, cast

import pytest

import numdaplot as ndp
from numdaplot.plots.plot_bar import plot_bar
from numdaplot.plots.plot_box import plot_box
from numdaplot.plots.plot_heatmap import plot_heatmap, read_heatmap_values
from numdaplot.plots.plot_histogram import plot_histogram
from numdaplot.plots.plot_line import plot_line
from numdaplot.plots.plot_missing_by_column import plot_missing_by_column
from numdaplot.plots.plot_missing_map import plot_missing_map
from numdaplot.plots.plot_pie import plot_pie, require_no_axis_settings
from numdaplot.plots.plot_scatter import plot_scatter

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
MISSING_PRICES = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.0, None])})
FRUITS = ndp.Array.from_list(["apple", "pear", "plum", "fig", "kiwi", "lime"])
FRUIT_SALES = ndp.Array.from_list([30.0, 25.0, 15.0, 12.0, 10.0, 8.0])
FRUIT_SHARES = ndp.Table.from_arrays({"fruit": FRUITS, "sales": FRUIT_SALES})


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


def test_plot_histogram_rejects_a_table_without_columns() -> None:
	"""
	Check that a Table needs columns.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		plot_histogram(SALES, ndp.HistogramChart())


def test_plot_histogram_rejects_colors_not_one_per_column_when_created() -> None:
	"""
	Check that two colors for one column raise InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		plot_histogram(PRICES, ndp.HistogramChart(colors=TWO_COLORS))


def test_plot_histogram_draws_with_the_default_style() -> None:
	"""
	Check that a histogram without style has no title.

	.. versionadded:: 0.1.0
	"""
	plot = plot_histogram(SALES, ndp.HistogramChart(columns=["price"]))

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == ""


def test_plot_box_rejects_group_by_for_an_array() -> None:
	"""
	Check that an Array takes no group_by.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		plot_box(GRID, ndp.BoxChart(group_by="city"))


def test_plot_box_rejects_colors_not_one_per_column_when_created() -> None:
	"""
	Check that one color for two Array columns raises InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidColorCountError):
		plot_box(GRID, ndp.BoxChart(colors=[ndp.Color.RED]))


def test_plot_pie_rejects_an_array() -> None:
	"""
	Check that an Array raises UnsupportedDataError, even untyped.

	.. versionadded:: 0.1.0
	"""
	untyped_plot_pie = cast(Any, plot_pie)

	with pytest.raises(ndp.UnsupportedDataError):
		untyped_plot_pie(PRICES, ndp.PieChart(labels="city", values="price"))


def test_plot_pie_rejects_colors_not_one_per_slice_when_created() -> None:
	"""
	Check that one color for two slices raises InvalidColorCountError at once.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="city", values="sales", colors=[ndp.Color.RED])

	with pytest.raises(ndp.InvalidColorCountError):
		plot_pie(CITY_TOTALS, chart)


def test_plot_pie_rejects_an_axis_label() -> None:
	"""
	Check that a style with a y_label raises RefusedSettingError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="y_label"):
		plot_pie(CITY_TOTALS, PIE_CHART, ndp.PlotStyle(y_label="Sales"))


def test_plot_pie_warns_beyond_five_slices() -> None:
	"""
	Check that 6 slices emit a ReadabilityWarning pointing at the caller.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="fruit", values="sales")

	with pytest.warns(ndp.ReadabilityWarning) as caught_warnings:
		plot_pie(FRUIT_SHARES, chart)

	warned_file = caught_warnings[0].filename
	assert warned_file == __file__


def test_plot_pie_is_silent_up_to_five_slices() -> None:
	"""
	Check that 2 slices emit no warning.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		plot_pie(CITY_TOTALS, PIE_CHART)

	assert caught_warnings == []


def test_require_no_axis_settings_accepts_a_title() -> None:
	"""
	Check that a pie style may have a title.

	.. versionadded:: 0.1.0
	"""
	require_no_axis_settings(ndp.PlotStyle(title="Sales"))


def test_require_no_axis_settings_accepts_no_style() -> None:
	"""
	Check that the default style passes.

	.. versionadded:: 0.1.0
	"""
	require_no_axis_settings(None)


def test_read_heatmap_values_reads_the_labels_and_columns_of_a_table() -> None:
	"""
	Check that labels gives the row positions and columns the series.

	.. versionadded:: 0.1.0
	"""
	values = read_heatmap_values(SALES, ndp.HeatmapChart(columns=["price"], labels="city"))

	assert values.positions.name == "city"
	assert values.series[0].name == "price"


def test_read_heatmap_values_rejects_a_table_without_columns() -> None:
	"""
	Check that a Table needs columns, named as the HeatmapChart names them.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError, match="needs columns"):
		read_heatmap_values(SALES, ndp.HeatmapChart(labels="city"))


def test_read_heatmap_values_reads_each_column_of_an_array() -> None:
	"""
	Check that an Array gives one series per column.

	.. versionadded:: 0.1.0
	"""
	values = read_heatmap_values(GRID, ndp.HeatmapChart())

	series_count = len(values.series)
	assert series_count == 2


def test_plot_heatmap_draws_with_the_default_style() -> None:
	"""
	Check that a heatmap without style has no title.

	.. versionadded:: 0.1.0
	"""
	plot = plot_heatmap(GRID, ndp.HeatmapChart())

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == ""


def test_plot_missing_by_column_rejects_an_array() -> None:
	"""
	Check that an Array raises UnsupportedDataError naming the function.

	.. versionadded:: 0.1.0
	"""
	untyped_plot = cast(Any, plot_missing_by_column)

	with pytest.raises(ndp.UnsupportedDataError, match="plot_missing_by_column"):
		untyped_plot(PRICES, ndp.MissingChart())


def test_plot_missing_map_rejects_an_array() -> None:
	"""
	Check that an Array raises UnsupportedDataError naming the function.

	.. versionadded:: 0.1.0
	"""
	untyped_plot = cast(Any, plot_missing_map)

	with pytest.raises(ndp.UnsupportedDataError, match="plot_missing_map"):
		untyped_plot(PRICES)


@pytest.mark.parametrize(
	("plot_function", "data"),
	[
		(plot_line, PRICES),
		(plot_bar, PRICES),
		(plot_scatter, PRICES),
		(plot_box, PRICES),
		(plot_histogram, PRICES),
		(plot_heatmap, GRID),
		(plot_missing_by_column, MISSING_PRICES),
	],
)
def test_plot_function_without_chart_draws_with_the_default_chart(
	plot_function: Callable[..., ndp.Plot],
	data: ndp.Table | ndp.Array,
) -> None:
	"""
	Check that a plot function called without chart draws one chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot_function
		The plot function.
	data
		Data the default chart draws.
	"""
	plot = plot_function(data)

	figure = plot.to_matplotlib()
	axes_count = len(figure.axes)
	assert axes_count >= 1


def test_plot_function_without_chart_still_needs_the_columns_of_a_table() -> None:
	"""
	Check that a Table without chart raises InvalidChartDataError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidChartDataError):
		plot_bar(SALES)


@pytest.mark.parametrize(
	"style",
	[
		ndp.PlotStyle(y_label="Sales"),
		ndp.PlotStyle(right_label="Price"),
		ndp.PlotStyle(x_tick_rotation=45),
		ndp.PlotStyle(y_tick_rotation=45),
	],
)
def test_require_no_axis_settings_rejects_every_axis_setting(style: ndp.PlotStyle) -> None:
	"""
	Check that each axis setting raises RefusedSettingError for a pie.

	.. versionadded:: 0.1.0

	Parameters
	----------
	style
		A style with one axis setting.
	"""
	with pytest.raises(ndp.RefusedSettingError):
		require_no_axis_settings(style)
