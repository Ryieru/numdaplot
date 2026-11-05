"""
Unit tests of the drawing of a ScatterChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
import pytest
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.point_values import read_point_values
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.scatter_drawing import choose_areas, draw_scatter_chart

SURFACES = ndp.Array.from_list([30.0, 45.0, 60.0])
PRICES = ndp.Array.from_list([150.0, 210.0, 260.0])
CITIES = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
ROOMS = ndp.Array.from_list([1, 2, 3])
FLATS = ndp.Table.from_arrays({"surface": SURFACES, "price": PRICES, "city": CITIES, "rooms": ROOMS})
VALUES = read_table_values(FLATS, "surface", ["price"], "ScatterChart")
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
GRID_VALUES = read_array_values(GRID, "ScatterChart")
SIZES = numpy.array([10.0, 20.0, numpy.nan, 30.0])
EXPECTED_AREAS = [16.0, 136.0, 0.0, 256.0]
SAME_SIZES = numpy.array([5.0, 5.0])
MIDDLE_AREA = 136.0
DEFAULT_AREA = 36.0


def build_table_layer(chart: ndp.ScatterChart) -> ChartLayer:
	"""
	Return a ScatterChart of the flats with its values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		A ScatterChart of surface and price.

	Returns
	-------
	ChartLayer
		The chart, its values and its point values.
	"""
	point_values = read_point_values(FLATS, chart.color_by, chart.size_by, VALUES.rows)
	layer = ChartLayer(chart, VALUES, point_values)

	return layer


def test_draw_scatter_chart_draws_one_point_per_row() -> None:
	"""
	Check that each row is a point at its x and y values.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	layer = build_table_layer(ndp.ScatterChart(x="surface", y="price"))

	draw_scatter_chart(axes, layer)

	offsets = numpy.asarray(axes.collections[0].get_offsets()).tolist()
	assert offsets == [[30.0, 150.0], [45.0, 210.0], [60.0, 260.0]]


def test_draw_scatter_chart_draws_one_group_per_color_text() -> None:
	"""
	Check that a text color_by gives one group of points per text, and its column as legend title.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	layer = build_table_layer(ndp.ScatterChart(x="surface", y="price", color_by="city"))

	drawn_chart = draw_scatter_chart(axes, layer)

	labels = [points.get_label() for points in axes.collections]
	assert labels == ["Paris", "Lyon"]
	assert drawn_chart.legend_title == "city"


def test_draw_scatter_chart_adds_a_color_bar_for_color_numbers() -> None:
	"""
	Check that a number color_by adds a color bar labeled with its column.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	layer = build_table_layer(ndp.ScatterChart(x="surface", y="price", color_by="rooms"))

	draw_scatter_chart(axes, layer)

	color_bar_label = figure.axes[1].get_ylabel()
	assert color_bar_label == "rooms"


def test_draw_scatter_chart_draws_each_array_column_in_its_color() -> None:
	"""
	Check that each column of an Array is a series of points.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_scatter_chart(axes, ChartLayer(ndp.ScatterChart(), GRID_VALUES))

	labels = [points.get_label() for points in axes.collections]
	assert labels == ["0", "1"]


def test_draw_scatter_chart_rejects_one_color_for_several_columns() -> None:
	"""
	Check that a single color for two series raises InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	layer = ChartLayer(ndp.ScatterChart(color=ndp.Color.RED), GRID_VALUES)

	with pytest.raises(InvalidColorCountError):
		draw_scatter_chart(axes, layer)


def test_choose_areas_scales_the_sizes_and_hides_missing_ones() -> None:
	"""
	Check the areas from 16 to 256, and 0 for a missing size.

	.. versionadded:: 0.1.0
	"""
	areas = choose_areas(SIZES, 4, None)

	assert areas.tolist() == EXPECTED_AREAS


def test_choose_areas_gives_the_middle_area_to_equal_sizes() -> None:
	"""
	Check that equal sizes all get the middle area.

	.. versionadded:: 0.1.0
	"""
	areas = choose_areas(SAME_SIZES, 2, None)

	assert areas.tolist() == [MIDDLE_AREA, MIDDLE_AREA]


def test_choose_areas_gives_the_default_area_without_sizes() -> None:
	"""
	Check that no size_by gives every point the default area.

	.. versionadded:: 0.1.0
	"""
	areas = choose_areas(None, 2, None)

	assert areas.tolist() == [DEFAULT_AREA, DEFAULT_AREA]


def test_choose_areas_squares_the_point_size() -> None:
	"""
	Check that a diameter of 3 gives an area of 9 square points.

	.. versionadded:: 0.1.0
	"""
	areas = choose_areas(None, 2, 3.0)

	assert areas.tolist() == [9.0, 9.0]
