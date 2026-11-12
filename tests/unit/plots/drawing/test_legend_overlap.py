"""
Unit tests of the legends placed with BEST that hide values.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Any, cast

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.transforms import Bbox

from numdaplot.plots.drawing.legend_overlap import covers_values, move_hiding_legends, move_past_axes
from numdaplot.plots.drawing.style_drawing import BEST_LEGEND_ID

GRID_SIZE = 10
GRID_NUMBERS = [float(number) for number in range(GRID_SIZE)]
GRID_X = GRID_NUMBERS * GRID_SIZE
GRID_Y = sorted(GRID_X)
BEST_LOCATION = "best"
UPPER_LEFT_LOCATION = "upper left"
BOX_HALF_SIDE = 5.0
BOX_SIDE = 10.0
ORIGIN = (0.0, 0.0)
FAR_POINT = (100.0, 100.0)
CROSSING_LINE_X = [-1.0, 1.0]
CROSSING_LINE_Y = [0.0, 0.0]
FIRST_SERIES = "first"
SECOND_SERIES = "second"


def build_axes() -> tuple[Figure, Axes]:
	"""
	Return a figure and its axes, to draw values on.

	.. versionadded:: 0.2.0

	Returns
	-------
	tuple[Figure, Axes]
		The figure and its only axes.
	"""
	figure = Figure()
	axes = figure.add_subplot()

	return figure, axes


def build_box_around(axes: Axes, data_point: tuple[float, float]) -> Bbox:
	"""
	Return a small box of the page centered on a point of the values.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The axes of the values, already laid out.
	data_point
		The point, in the coordinates of the values.

	Returns
	-------
	Bbox
		A square box around the point.
	"""
	# Some versions of the matplotlib stubs leave the type of the transformed point unknown.
	data_transform = cast(Any, axes.transData)
	page_point = data_transform.transform(data_point)
	left = page_point[0] - BOX_HALF_SIDE
	bottom = page_point[1] - BOX_HALF_SIDE
	box = Bbox.from_bounds(left, bottom, BOX_SIDE, BOX_SIDE)

	return box


def is_past_axes(axes: Axes, legend: Legend) -> bool:
	"""
	Return whether a legend is anchored past the right edge of its axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The axes of the legend.
	legend
		The legend.

	Returns
	-------
	bool
		True when the anchor of the legend starts on the right of the axes.
	"""
	anchor_box = legend.get_bbox_to_anchor()
	is_past = bool(anchor_box.x0 > axes.bbox.x1)

	return is_past


def draw_full_grid(axes: Axes) -> None:
	"""
	Draw points filling the whole axes, and a second series so that the legend has two names.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The axes drawn on.
	"""
	axes.scatter(GRID_X, GRID_Y, label=FIRST_SERIES)
	axes.scatter(GRID_X, GRID_Y, label=SECOND_SERIES)


def test_covers_values_finds_a_point_under_the_box() -> None:
	"""
	Check that a box around a point covers a value.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	axes.scatter([ORIGIN[0]], [ORIGIN[1]])
	figure.draw_without_rendering()
	box = build_box_around(axes, ORIGIN)

	is_covered = covers_values(axes, box)

	assert is_covered


def test_covers_values_finds_a_line_crossing_the_box() -> None:
	"""
	Check that a line crossing a box covers a value, although none of its points is inside.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	axes.plot(CROSSING_LINE_X, CROSSING_LINE_Y)
	figure.draw_without_rendering()
	box = build_box_around(axes, ORIGIN)

	is_covered = covers_values(axes, box)

	assert is_covered


def test_covers_values_finds_a_bar_under_the_box() -> None:
	"""
	Check that a box on a bar covers a value.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	axes.bar([ORIGIN[0]], [FAR_POINT[1]])
	figure.draw_without_rendering()
	box = build_box_around(axes, ORIGIN)

	is_covered = covers_values(axes, box)

	assert is_covered


def test_covers_values_finds_nothing_away_from_the_values() -> None:
	"""
	Check that a box far from every value covers nothing.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	axes.scatter([ORIGIN[0]], [ORIGIN[1]])
	axes.scatter([FAR_POINT[0]], [FAR_POINT[1]])
	figure.draw_without_rendering()
	middle_point = (FAR_POINT[0] / 2, FAR_POINT[1] / 2)
	box = build_box_around(axes, middle_point)

	is_covered = covers_values(axes, box)

	assert not is_covered


def test_move_hiding_legends_moves_a_best_legend_hiding_values() -> None:
	"""
	Check that a marked legend over a grid of points is moved past the axes.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	draw_full_grid(axes)
	legend = axes.legend(loc=BEST_LOCATION)
	legend.set_gid(BEST_LEGEND_ID)

	move_hiding_legends(figure)

	is_past = is_past_axes(axes, legend)
	assert is_past


def test_move_hiding_legends_keeps_a_legend_placed_by_the_user() -> None:
	"""
	Check that a legend placed at a chosen corner stays there, even over values.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	draw_full_grid(axes)
	legend = axes.legend(loc=UPPER_LEFT_LOCATION)

	move_hiding_legends(figure)

	is_past = is_past_axes(axes, legend)
	assert not is_past


def test_move_hiding_legends_keeps_a_best_legend_in_a_free_corner() -> None:
	"""
	Check that a marked legend hiding no value stays inside the axes.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_axes()
	axes.scatter([ORIGIN[0]], [ORIGIN[1]], label=FIRST_SERIES)
	axes.scatter([FAR_POINT[0]], [ORIGIN[1]], label=SECOND_SERIES)
	legend = axes.legend(loc=BEST_LOCATION)
	legend.set_gid(BEST_LEGEND_ID)

	move_hiding_legends(figure)

	is_past = is_past_axes(axes, legend)
	assert not is_past


def test_move_past_axes_anchors_the_legend_on_the_right() -> None:
	"""
	Check that a moved legend is anchored past the right edge of its axes.

	.. versionadded:: 0.2.0
	"""
	_, axes = build_axes()
	axes.plot(CROSSING_LINE_X, CROSSING_LINE_Y, label=FIRST_SERIES)
	legend = axes.legend(loc=BEST_LOCATION)

	move_past_axes(axes, legend)

	is_past = is_past_axes(axes, legend)
	assert is_past
