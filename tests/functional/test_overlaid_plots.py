"""
Functional tests of the charts added over a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from datetime import date
from pathlib import Path

import numpy
import pytest
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle

import numdaplot as ndp

SHOP = ndp.Table.from_arrays(
	{
		"month": ndp.Array.from_list(["Jan", "Feb", "Mar"]),
		"sales": ndp.Array.from_list([120.0, 150.0, 90.0]),
		"price": ndp.Array.from_list([12.5, 11.0, 14.0]),
	}
)
TARGETS = ndp.Table.from_arrays(
	{
		"month": ndp.Array.from_list(["Feb", "Apr"]),
		"target": ndp.Array.from_list([160.0, 170.0]),
	}
)
DAILY = ndp.Table.from_arrays(
	{
		"day": ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 2)]),
		"sales": ndp.Array.from_list([10.0, 12.0]),
	}
)
SALES_BARS = ndp.BarChart(x="month", y=["sales"])
EXPECTED_MONTHS = ["Jan", "Feb", "Mar", "Apr"]
BLUE_CODE = "#1f77b4"
ORANGE_CODE = "#ff7f0e"


def test_a_line_over_bars_shares_their_labels_and_adds_its_own() -> None:
	"""
	Check merged labels, the target placed on its month, and the next color of the cycle.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_bar(SHOP, SALES_BARS)
	line = ndp.LineChart(x="month", y=["target"])

	both = plot.add_line(TARGETS, line)

	axes = both.to_matplotlib().axes[0]
	month_labels = [label.get_text() for label in axes.get_xticklabels()]
	target_line = axes.lines[0]
	target_values = numpy.asarray(target_line.get_ydata(), dtype=numpy.float64)
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	assert month_labels == EXPECTED_MONTHS
	assert numpy.isnan(target_values[0])
	assert target_values[1] == 160.0
	assert target_values[3] == 170.0
	assert target_line.get_color() == ORANGE_CODE
	assert len(bars) == 3


def test_a_line_on_the_right_axis_has_its_own_scale_and_label() -> None:
	"""
	Check two vertical axes, the right label of the style, and one legend naming both charts.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(y_label="Sales", right_label="Price (euros)")
	plot = ndp.plot_bar(SHOP, SALES_BARS, style)
	line = ndp.LineChart(x="month", y=["price"])

	both = plot.add_line(SHOP, line, axis=ndp.ValueAxis.RIGHT)

	figure = both.to_matplotlib()
	left_axes, right_axes = figure.axes
	legend = right_axes.get_legend()
	assert left_axes.get_ylabel() == "Sales"
	assert right_axes.get_ylabel() == "Price (euros)"
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	assert legend_texts == ["sales", "price"]


def test_charts_can_be_added_one_after_the_other() -> None:
	"""
	Check that bars, a line and points are drawn together, each in the next color.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_bar(SHOP, SALES_BARS)
	with_line = plot.add_line(SHOP, ndp.LineChart(x="month", y=["price"]), axis=ndp.ValueAxis.RIGHT)

	with_points = with_line.add_scatter(SHOP, ndp.ScatterChart(x="month", y="price"), axis=ndp.ValueAxis.RIGHT)

	right_axes = with_points.to_matplotlib().axes[1]
	bar_color = with_points.to_matplotlib().axes[0].patches[0].get_facecolor()
	assert len(right_axes.lines) == 1
	assert len(right_axes.collections) == 1
	assert bar_color == to_rgba(BLUE_CODE)


def test_a_chart_of_dates_cannot_be_added_over_months() -> None:
	"""
	Check that dates over texts raise IncompatibleChartsError, caught as a NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_bar(SHOP, SALES_BARS)
	line = ndp.LineChart(x="day", y=["sales"])

	with pytest.raises(ndp.NumdaplotError, match="dates"):
		plot.add_line(DAILY, line)


def test_an_overlaid_plot_is_saved_as_an_image(tmp_path: Path) -> None:
	"""
	Check that a Plot with an added line is written as a PNG file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / "shop.png"
	plot = ndp.plot_bar(SHOP, SALES_BARS)
	both = plot.add_line(SHOP, ndp.LineChart(x="month", y=["price"]), axis=ndp.ValueAxis.RIGHT)

	both.save(image_path)

	image_start = image_path.read_bytes()[:4]
	assert image_start == b"\x89PNG"


def test_a_date_axis_labels_the_period_of_the_charts_on_both_sides() -> None:
	"""
	Check that the corner label of a date axis covers the dates of a chart on the right.

	.. versionadded:: 0.1.0
	"""
	march_sales = ndp.Table.from_arrays(
		{
			"day": ndp.Array.from_list([date(2019, 3, 1), date(2019, 3, 31)]),
			"sales": ndp.Array.from_list([10.0, 12.0]),
		}
	)
	may_prices = ndp.Table.from_arrays(
		{
			"day": ndp.Array.from_list([date(2019, 4, 1), date(2019, 5, 20)]),
			"price": ndp.Array.from_list([3.0, 4.0]),
		}
	)
	plot = ndp.plot_line(march_sales, ndp.LineChart(x="day", y=["sales"]))
	both = plot.add_line(may_prices, ndp.LineChart(x="day", y=["price"]), axis=ndp.ValueAxis.RIGHT)

	figure = both.to_matplotlib()
	figure.draw_without_rendering()

	left_axes = figure.axes[0]
	corner_label = left_axes.xaxis.get_offset_text()
	corner_text = corner_label.get_text()
	assert corner_text == "2019-Mar to 2019-May"
