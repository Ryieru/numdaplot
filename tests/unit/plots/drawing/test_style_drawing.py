"""
Unit tests of the drawing of the PlotStyle of a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import pytest
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.plot_axes import PlotAxes
from numdaplot.plots.drawing.style_drawing import (
	BEST_LEGEND_ID,
	LEGEND_POINT_AREA,
	apply_style,
	draw_grid_lines,
	find_first_shape_id,
	find_transform_past_right_axis,
	list_legend_entries,
	place_legend,
	write_axis_labels,
	write_right_label,
)

LINE_CHART = DrawnChart("day", "price", False, GridAxes.BOTH, None)
HORIZONTAL_BARS = DrawnChart("city", None, True, GridAxes.VALUES, None)
GROUPS = DrawnChart("surface", "price", False, GridAxes.BOTH, "city")
HEATMAP = DrawnChart(None, "city", False, GridAxes.NONE, None)


def test_apply_style_writes_the_y_label_by_the_x_label_by_default() -> None:
	"""
	Check that a default PlotStyle draws the title built from the labels.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	apply_style(PlotAxes(axes, None, None), LINE_CHART, ndp.PlotStyle())

	assert axes.get_title() == "price by day"


def test_write_axis_labels_puts_the_x_label_on_the_vertical_axis_for_horizontal_bars() -> None:
	"""
	Check that x_label names the axis of the x values, whatever its direction.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	write_axis_labels(axes, HORIZONTAL_BARS, ndp.PlotStyle(x_label="City"))

	assert axes.get_ylabel() == "City"
	assert axes.get_xlabel() == ""


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


def test_draw_grid_lines_draws_none_for_a_heatmap() -> None:
	"""
	Check that a chart asking for no grid lines gets none across either axis.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_grid_lines(axes, HEATMAP)

	x_visible = axes.xaxis.get_gridlines()[0].get_visible()
	y_visible = axes.yaxis.get_gridlines()[0].get_visible()
	assert not x_visible
	assert not y_visible


def test_place_legend_draws_no_legend_for_a_single_series() -> None:
	"""
	Check that one series gives no legend.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([1.0, 2.0], label="price")

	place_legend(PlotAxes(axes, None, None), LINE_CHART, ndp.LegendPosition.BEST)

	assert axes.get_legend() is None


def test_place_legend_draws_points_of_the_same_size_with_the_legend_title() -> None:
	"""
	Check that the legend of point groups has its title and points of one size.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.scatter([1.0], [2.0], s=[200.0], label="Paris")
	axes.scatter([2.0], [3.0], s=[16.0], label="Lyon")

	place_legend(PlotAxes(axes, None, None), GROUPS, ndp.LegendPosition.OUTSIDE_RIGHT)

	legend = axes.get_legend()
	assert legend is not None
	handle_areas = [
		float(handle.get_sizes()[0]) for handle in legend.legend_handles if isinstance(handle, PathCollection)
	]
	assert legend.get_title().get_text() == "city"
	assert handle_areas == [LEGEND_POINT_AREA, LEGEND_POINT_AREA]


def test_write_right_label_names_the_right_axis_by_default() -> None:
	"""
	Check that the axis on the right gets the default label of its first chart.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	right_axes = axes.twinx()

	write_right_label(PlotAxes(axes, right_axes, "price"), ndp.PlotStyle())

	assert right_axes.get_ylabel() == "price"


def test_write_right_label_writes_the_label_of_the_style() -> None:
	"""
	Check that the right_label of the style wins over the default one.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	right_axes = axes.twinx()

	write_right_label(PlotAxes(axes, right_axes, "price"), ndp.PlotStyle(right_label="Euros"))

	assert right_axes.get_ylabel() == "Euros"


def test_write_right_label_does_nothing_without_right_axis() -> None:
	"""
	Check that a Plot without axis on the right gets no right label.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	write_right_label(PlotAxes(axes, None, "price"), ndp.PlotStyle(right_label="Euros"))

	axes_count = len(axes.figure.axes)
	assert axes_count == 1


def test_place_legend_names_the_series_of_both_axes_over_the_right_one() -> None:
	"""
	Check that the legend gathers the series of both axes and is drawn over the right axes.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([1.0, 2.0], label="sales")
	right_axes = axes.twinx()
	right_axes.plot([3.0, 1.0], label="price")

	place_legend(PlotAxes(axes, right_axes, None), LINE_CHART, ndp.LegendPosition.BEST)

	legend = right_axes.get_legend()
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	assert legend_texts == ["sales", "price"]
	assert axes.get_legend() is None


def test_list_legend_entries_follows_the_drawing_order() -> None:
	"""
	Check that bars drawn before a line are named first, unlike matplotlib does.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.bar([0.0, 1.0], [3.0, 4.0], label="sales")
	axes.plot([0.0, 1.0], [2.0, 5.0], label="target")

	_, labels = list_legend_entries(axes)

	assert labels == ["sales", "target"]


def test_find_first_shape_id_gives_the_first_bar_of_a_container() -> None:
	"""
	Check that bars are placed at their first bar.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	bars = axes.bar([0.0, 1.0], [3.0, 4.0])

	shape_id = find_first_shape_id(bars)

	first_bar = bars.patches[0]
	assert shape_id == id(first_bar)


def test_find_first_shape_id_gives_an_empty_container_itself() -> None:
	"""
	Check that a container without shape is identified by itself.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	bars = axes.bar([], [])

	shape_id = find_first_shape_id(bars)

	assert shape_id == id(bars)


def test_find_transform_past_right_axis_shifts_past_the_axis() -> None:
	"""
	Check that the shift covers the width of the values and the label on the right.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	right_axes = axes.twinx()
	right_axes.set_ylabel("Mean price")

	transform = find_transform_past_right_axis(right_axes)

	shifted_edge = transform.transform((1.0, 0.0))[0]
	axis_box = right_axes.yaxis.get_tightbbox()
	assert axis_box is not None
	assert shifted_edge == pytest.approx(axis_box.x1)


def test_place_legend_moves_best_outside_with_axes_on_the_right() -> None:
	"""
	Check that ``BEST`` uses the location of ``OUTSIDE_RIGHT`` with axes on the right.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([1.0, 2.0], label="price")
	right_axes = axes.twinx()
	right_axes.plot([3.0, 1.0], label="cost")

	place_legend(PlotAxes(axes, right_axes, None), LINE_CHART, ndp.LegendPosition.BEST)

	legend = right_axes.get_legend()
	assert legend is not None
	legend_anchor = legend.get_bbox_to_anchor()
	axes_box = right_axes.get_window_extent()
	assert legend_anchor.x0 > axes_box.x1


def test_find_transform_past_right_axis_stays_on_the_edge_of_a_hidden_axis() -> None:
	"""
	Check that a right axis hidden from view adds no shift past the edge of the axes.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	right_axes = axes.twinx()
	right_axes.yaxis.set_visible(False)

	transform = find_transform_past_right_axis(right_axes)

	shifted_edge = transform.transform((1.0, 0.0))[0]
	axes_box = right_axes.get_window_extent()
	assert shifted_edge == pytest.approx(axes_box.x1)


@pytest.mark.parametrize(
	("legend_position", "expected_id"),
	[
		(ndp.LegendPosition.BEST, BEST_LEGEND_ID),
		(ndp.LegendPosition.UPPER_LEFT, None),
		(ndp.LegendPosition.OUTSIDE_RIGHT, None),
	],
)
def test_place_legend_marks_only_a_best_legend_inside_the_axes(
	legend_position: ndp.LegendPosition,
	expected_id: str | None,
) -> None:
	"""
	Check that only a ``BEST`` legend placed inside the axes is marked to be checked once laid out.

	.. versionadded:: 0.2.0

	Parameters
	----------
	legend_position
		The position asked for.
	expected_id
		The mark of the legend, None when it is not checked.
	"""
	axes = Figure().add_subplot()
	axes.plot([1.0, 2.0], label="price")
	axes.plot([2.0, 1.0], label="cost")

	place_legend(PlotAxes(axes, None, None), LINE_CHART, legend_position)

	legend = axes.get_legend()
	assert legend is not None
	legend_id = legend.get_gid()
	assert legend_id == expected_id
