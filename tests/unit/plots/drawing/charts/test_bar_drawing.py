"""
Unit tests of the drawing of a BarChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.axes.grid_axes import GridAxes
from numdaplot.plots.drawing.charts.bar_drawing import StackTops, draw_bar_chart, find_group_coordinates, stack_bars

CITIES = ndp.Array.from_list(["Paris", "Lyon"])
SALES_2025 = ndp.Array.from_list([120.0, -10.0])
SALES_2026 = ndp.Array.from_list([150.0, None])
SALES = ndp.Table.from_arrays({"city": CITIES, "2025": SALES_2025, "2026": SALES_2026})
VALUES = read_table_values(SALES, "city", ["2025", "2026"], "BarChart")
GROUPED_LAYER = ChartLayer(ndp.BarChart(x="city", y=["2025", "2026"]), VALUES)
STACKED_CHART = ndp.BarChart(x="city", y=["2025", "2026"], layout=ndp.BarLayout.STACKED)
STACKED_LAYER = ChartLayer(STACKED_CHART, VALUES)
HORIZONTAL_CHART = ndp.BarChart(x="city", y=["2025", "2026"], orientation=ndp.Orientation.HORIZONTAL)
HORIZONTAL_LAYER = ChartLayer(HORIZONTAL_CHART, VALUES)
EXPECTED_GROUPED_MIDDLES = [-0.2, 0.8, 0.2]
EXPECTED_STACKED_BASES = [0.0, 0.0, 120.0]
LABELED_CHART = ndp.BarChart(x="city", y=["2025", "2026"], value_labels=ndp.ValueLabels(decimals=1))
LABELED_LAYER = ChartLayer(LABELED_CHART, VALUES)
EXPECTED_LABEL_TEXTS = ["120.0", "-10.0", "150.0"]


def test_draw_bar_chart_draws_no_bar_at_a_missing_value() -> None:
	"""
	Check that three present values give three bars.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_bar_chart(axes, GROUPED_LAYER)

	bar_count = len(axes.patches)
	assert bar_count == 3


def test_draw_bar_chart_places_grouped_bars_side_by_side() -> None:
	"""
	Check the middles of grouped bars around each position: both bars of 2025, then the bar of 2026.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_bar_chart(axes, GROUPED_LAYER)

	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	middles = [round(bar.get_x() + bar.get_width() / 2, 6) for bar in bars]
	assert middles == EXPECTED_GROUPED_MIDDLES


def test_draw_bar_chart_stacks_bars_on_each_other() -> None:
	"""
	Check that a stacked bar starts at the top of the bar below it.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_bar_chart(axes, STACKED_LAYER)

	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	bases = [float(bar.get_y()) for bar in bars]
	assert bases == EXPECTED_STACKED_BASES


def test_draw_bar_chart_places_horizontal_bars_from_the_top() -> None:
	"""
	Check that horizontal bars put the x values on the vertical axis, the first row on top.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_bar_chart(axes, HORIZONTAL_LAYER)

	bottom_limit, top_limit = axes.get_ylim()
	assert drawn_chart.x_on_vertical_axis
	assert bottom_limit > top_limit


def test_draw_bar_chart_only_grids_the_values() -> None:
	"""
	Check that bars ask for grid lines across their values only.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_bar_chart(axes, GROUPED_LAYER)

	assert drawn_chart.grid_axes == GridAxes.VALUES


def test_draw_bar_chart_writes_the_value_of_each_present_bar() -> None:
	"""
	Check that a chart with value labels writes one rounded value per bar drawn.

	.. versionadded:: 0.2.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	draw_bar_chart(axes, LABELED_LAYER)

	label_texts = [text.get_text() for text in axes.texts]
	assert label_texts == EXPECTED_LABEL_TEXTS


def test_draw_bar_chart_writes_no_value_by_default() -> None:
	"""
	Check that a chart without value labels writes no text.

	.. versionadded:: 0.2.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	draw_bar_chart(axes, GROUPED_LAYER)

	text_count = len(axes.texts)
	assert text_count == 0


def test_find_group_coordinates_centers_the_group_on_the_position() -> None:
	"""
	Check that the middle series of three stays on the position.

	.. versionadded:: 0.1.0
	"""
	coordinates = numpy.array([0.0, 1.0])

	group_coordinates = find_group_coordinates(coordinates, 1, 3)

	rounded_coordinates = numpy.round(group_coordinates, 6).tolist()
	assert rounded_coordinates == [0.0, 1.0]


def test_stack_bars_stacks_negative_values_below_zero() -> None:
	"""
	Check that a negative value starts at the bottom of the negative stack.

	.. versionadded:: 0.1.0
	"""
	stack_tops = StackTops(numpy.array([5.0]), numpy.array([-2.0]))

	bases, new_tops = stack_bars(numpy.array([-3.0]), stack_tops)

	assert bases.tolist() == [-2.0]
	assert new_tops.negative.tolist() == [-5.0]
	assert new_tops.positive.tolist() == [5.0]


def test_stack_bars_adds_nothing_for_a_missing_value() -> None:
	"""
	Check that a missing value leaves the stacks unchanged.

	.. versionadded:: 0.1.0
	"""
	stack_tops = StackTops(numpy.array([5.0]), numpy.array([0.0]))

	_, new_tops = stack_bars(numpy.array([numpy.nan]), stack_tops)

	assert new_tops.positive.tolist() == [5.0]
