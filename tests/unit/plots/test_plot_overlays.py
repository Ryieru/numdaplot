"""
Unit tests of the charts drawn over a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false
# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

import numpy
import pytest

import numdaplot as ndp
from numdaplot.plots.plot import Plot

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
MONTHS = ndp.Array.from_list(["Jan", "Feb", "Mar"])
SHOP = ndp.Table.from_arrays(
	{
		"month": MONTHS,
		"sales": ndp.Array.from_list([120.0, 150.0, 90.0]),
		"price": ndp.Array.from_list([12.5, 11.0, 14.0]),
	}
)
SALES_BARS = ndp.BarChart(x="month", y=["sales"])
PRICE_LINE = ndp.LineChart(x="month", y=["price"])
PRICE_POINTS = ndp.ScatterChart(x="month", y="price")
BOX_PLOT = ndp.Plot.box(PRICES, ndp.BoxChart())


def build_sales_plot() -> Plot:
	"""
	Return a Plot of the sales of each month as bars.

	.. versionadded:: 0.1.0

	Returns
	-------
	Plot
		A bar Plot of three months.
	"""
	plot = ndp.Plot.bar(SHOP, SALES_BARS)

	return plot


def test_add_line_draws_a_line_over_the_bars_and_leaves_the_plot_unchanged() -> None:
	"""
	Check that the new Plot has the bars and the line, and the first one only the bars.

	.. versionadded:: 0.1.0
	"""
	plot = build_sales_plot()

	both = plot.add_line(SHOP, PRICE_LINE)

	plot_axes = plot.to_matplotlib().axes[0]
	both_axes = both.to_matplotlib().axes[0]
	assert len(plot_axes.lines) == 0
	assert len(both_axes.lines) == 1
	assert len(both_axes.patches) == 3


def test_add_line_on_the_right_draws_a_second_axis() -> None:
	"""
	Check that a line on the right gets axes of its own, labeled with its column.

	.. versionadded:: 0.1.0
	"""
	plot = build_sales_plot()

	both = plot.add_line(SHOP, PRICE_LINE, axis=ndp.ValueAxis.RIGHT)

	figure = both.to_matplotlib()
	axes_count = len(figure.axes)
	assert axes_count == 2
	assert figure.axes[1].get_ylabel() == "price"


def test_add_bar_rejects_horizontal_bars() -> None:
	"""
	Check that added bars must be vertical.

	.. versionadded:: 0.1.0
	"""
	horizontal_bars = ndp.BarChart(x="month", y=["price"], orientation=ndp.Orientation.HORIZONTAL)

	with pytest.raises(ndp.RefusedSettingError):
		build_sales_plot().add_bar(SHOP, horizontal_bars)


def test_add_bar_draws_bars_over_the_bars() -> None:
	"""
	Check that added bars are drawn after the first ones.

	.. versionadded:: 0.1.0
	"""
	both = build_sales_plot().add_bar(SHOP, ndp.BarChart(x="month", y=["price"]))

	both_axes = both.to_matplotlib().axes[0]
	assert len(both_axes.patches) == 6


def test_add_scatter_draws_points_over_the_bars() -> None:
	"""
	Check that added points are drawn on the labels of the bars.

	.. versionadded:: 0.1.0
	"""
	both = build_sales_plot().add_scatter(SHOP, PRICE_POINTS)

	both_axes = both.to_matplotlib().axes[0]
	point_offsets = both_axes.collections[0].get_offsets()
	offsets = numpy.asarray(point_offsets).tolist()
	assert offsets == [[0.0, 12.5], [1.0, 11.0], [2.0, 14.0]]


def test_add_line_rejects_a_plot_of_boxes() -> None:
	"""
	Check that a Plot of boxes refuses added charts.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="BoxChart"):
		BOX_PLOT.add_line(PRICES, ndp.LineChart())


def test_add_line_rejects_numbers_over_texts() -> None:
	"""
	Check that a line of numbers cannot be added over bars of texts.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.IncompatibleChartsError):
		build_sales_plot().add_line(PRICES, ndp.LineChart())


def test_add_line_keeps_the_style_of_the_plot() -> None:
	"""
	Check that the new Plot has the title of the first one.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.bar(SHOP, SALES_BARS, ndp.PlotStyle(title="Shop"))

	both = plot.add_line(SHOP, PRICE_LINE)

	both_axes = both.to_matplotlib().axes[0]
	assert both_axes.get_title() == "Shop"


def test_add_line_without_chart_draws_the_lines_of_an_array() -> None:
	"""
	Check that add_line without chart draws a line over the bars.

	.. versionadded:: 0.1.0
	"""
	bar_plot = ndp.Plot.bar(PRICES)

	both = bar_plot.add_line(PRICES)

	figure = both.to_matplotlib()
	line_count = len(figure.axes[0].lines)
	assert line_count == 1


def test_add_scatter_without_chart_draws_the_points_of_an_array() -> None:
	"""
	Check that add_scatter without chart draws points over the bars.

	.. versionadded:: 0.1.0
	"""
	bar_plot = ndp.Plot.bar(PRICES)

	both = bar_plot.add_scatter(PRICES)

	figure = both.to_matplotlib()
	point_group_count = len(figure.axes[0].collections)
	assert point_group_count == 1
