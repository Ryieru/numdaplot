"""
Unit tests of the drawing of the Style of a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from matplotlib.collections import PathCollection
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.style_drawing import (
	LEGEND_POINT_AREA,
	apply_style,
	choose_label,
	draw_grid_lines,
	place_legend,
	write_axis_labels,
)

LINE_CHART = DrawnChart("day", "price", False, True, None)
HORIZONTAL_BARS = DrawnChart("city", None, True, False, None)
GROUPS = DrawnChart("surface", "price", False, True, "city")


def test_apply_style_writes_no_title_by_default() -> None:
	"""
	Check that a default Style draws no title.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	apply_style(axes, LINE_CHART, ndp.Style())

	assert axes.get_title() == ""


def test_write_axis_labels_puts_the_x_label_on_the_vertical_axis_for_horizontal_bars() -> None:
	"""
	Check that x_label names the axis of the x values, whatever its direction.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	write_axis_labels(axes, HORIZONTAL_BARS, ndp.Style(x_label="City"))

	assert axes.get_ylabel() == "City"
	assert axes.get_xlabel() == ""


def test_choose_label_prefers_an_empty_style_label_to_the_default() -> None:
	"""
	Check that an empty label in the style removes the default one.

	.. versionadded:: 0.1.0
	"""
	label = choose_label("", "price")

	assert label == ""


def test_draw_grid_lines_crosses_both_axes_for_lines() -> None:
	"""
	Check that a line chart gets grid lines across both axes.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_grid_lines(axes, LINE_CHART)

	x_visible = axes.xaxis.get_gridlines()[0].get_visible()
	y_visible = axes.yaxis.get_gridlines()[0].get_visible()
	assert x_visible
	assert y_visible


def test_draw_grid_lines_crosses_the_values_of_horizontal_bars_only() -> None:
	"""
	Check that horizontal bars get vertical grid lines only.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_grid_lines(axes, HORIZONTAL_BARS)

	x_visible = axes.xaxis.get_gridlines()[0].get_visible()
	y_visible = axes.yaxis.get_gridlines()[0].get_visible()
	assert x_visible
	assert not y_visible


def test_place_legend_draws_no_legend_for_a_single_series() -> None:
	"""
	Check that one series gives no legend.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([1.0, 2.0], label="price")

	place_legend(axes, LINE_CHART, ndp.LegendPosition.BEST)

	assert axes.get_legend() is None


def test_place_legend_draws_points_of_the_same_size_with_the_legend_title() -> None:
	"""
	Check that the legend of point groups has its title and points of one size.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.scatter([1.0], [2.0], s=[200.0], label="Paris")
	axes.scatter([2.0], [3.0], s=[16.0], label="Lyon")

	place_legend(axes, GROUPS, ndp.LegendPosition.OUTSIDE_RIGHT)

	legend = axes.get_legend()
	assert legend is not None
	handle_areas = [
		float(handle.get_sizes()[0]) for handle in legend.legend_handles if isinstance(handle, PathCollection)
	]
	assert legend.get_title().get_text() == "city"
	assert handle_areas == [LEGEND_POINT_AREA, LEGEND_POINT_AREA]
