"""
Unit tests of the drawing of a PieChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
import pytest
from matplotlib.figure import Figure
from matplotlib.patches import Wedge

import numdaplot as ndp
from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.pie_values import read_pie_values
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.pie_drawing import draw_pie_chart, find_percentage_place, write_percentages
from numdaplot.plots.drawing.text_contrast import DARK_TEXT_COLOR, LIGHT_TEXT_COLOR

CITIES = ndp.Array.from_list(["Paris", "Lyon"])
SALES = ndp.Array.from_list([150.0, 50.0])
SHARES = ndp.Table.from_arrays({"city": CITIES, "sales": SALES})
EXPECTED_TEXTS = ["Paris", "Lyon", "75.0%", "25.0%"]
EXPECTED_LABELS = ["Paris", "Lyon"]
TOP_ANGLE = 90.0
FULL_TURN = 360.0
UPPER_HALF = Wedge((0.0, 0.0), 1.0, 0.0, 180.0)
EXPECTED_UPPER_PLACE = (0.0, 0.65)
WHITE_SLICE = Wedge((0.0, 0.0), 1.0, 0.0, 360.0, facecolor="#ffffff")
DARK_SLICE = Wedge((0.0, 0.0), 1.0, 0.0, 360.0, facecolor="#000033")
SINGLE_VALUE = numpy.array([4.0])


def build_layer(chart: ndp.PieChart) -> ChartLayer:
	"""
	Return a PieChart of the city sales with its values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart drawn.

	Returns
	-------
	ChartLayer
		The chart, its labels and its values.
	"""
	pie_values = read_pie_values(SHARES, chart)
	layer = ChartLayer(chart, pie_values)

	return layer


def test_draw_pie_chart_labels_each_slice_with_its_share() -> None:
	"""
	Check that each slice is labeled with its text and its percentage, without grid lines.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_pie_chart(axes, build_layer(ndp.PieChart(labels="city", values="sales")))

	texts = [text.get_text() for text in axes.texts]
	assert texts == EXPECTED_TEXTS
	assert drawn_chart.grid_axes == GridAxes.NONE


def test_draw_pie_chart_starts_at_the_top_and_turns_clockwise() -> None:
	"""
	Check that the first slice starts at the top and the second one follows it clockwise.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_pie_chart(axes, build_layer(ndp.PieChart(labels="city", values="sales")))

	slices = [patch for patch in axes.patches if isinstance(patch, Wedge)]
	first_end = slices[0].theta2 % FULL_TURN
	second_end = slices[1].theta2 % FULL_TURN
	assert first_end == pytest.approx(TOP_ANGLE)
	assert second_end == pytest.approx(slices[0].theta1 % FULL_TURN)


def test_draw_pie_chart_hides_the_percentages_when_hidden() -> None:
	"""
	Check that only the labels are written when the percentages are hidden.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	chart = ndp.PieChart(labels="city", values="sales", percentages=ndp.Percentages.HIDDEN)

	draw_pie_chart(axes, build_layer(chart))

	texts = [text.get_text() for text in axes.texts]
	assert texts == EXPECTED_LABELS


def test_draw_pie_chart_leaves_the_slices_out_of_the_legend() -> None:
	"""
	Check that the slices, already labeled, give no legend entry.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_pie_chart(axes, build_layer(ndp.PieChart(labels="city", values="sales")))

	_, legend_labels = axes.get_legend_handles_labels()
	assert legend_labels == []


def test_draw_pie_chart_rejects_colors_not_one_per_slice() -> None:
	"""
	Check that one color for two slices raises InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	chart = ndp.PieChart(labels="city", values="sales", colors=[ndp.Color.RED])

	with pytest.raises(InvalidColorCountError):
		draw_pie_chart(axes, build_layer(chart))


def test_write_percentages_writes_black_over_a_light_slice() -> None:
	"""
	Check that a light slice gets a black percentage.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	write_percentages(axes, [WHITE_SLICE], SINGLE_VALUE)

	text_color = axes.texts[0].get_color()
	assert text_color == DARK_TEXT_COLOR


def test_write_percentages_writes_white_over_a_dark_slice() -> None:
	"""
	Check that a dark slice gets a white percentage.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	write_percentages(axes, [DARK_SLICE], SINGLE_VALUE)

	text_color = axes.texts[0].get_color()
	assert text_color == LIGHT_TEXT_COLOR


def test_find_percentage_place_is_on_the_middle_angle_of_the_slice() -> None:
	"""
	Check that the upper half of a disc has its percentage straight above the center.

	.. versionadded:: 0.1.0
	"""
	text_place = find_percentage_place(UPPER_HALF)

	assert text_place == pytest.approx(EXPECTED_UPPER_PLACE)
