"""
Functional tests of the order of the color_by groups of a scatter Plot.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

import numpy
from matplotlib.axes import Axes

import numdaplot as ndp

CLUSTER_NAMES = ["Noise", "Cluster 3", "Cluster 0", "Cluster 10", "Cluster 2", "Noise", "Cluster 1"]
EXPECTED_CLUSTER_ORDER = ["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 10", "Noise"]
AGES = [25, 5, 70, 8]
AGE_BRACKETS = ndp.Brackets(limits=[0, 10, 20, 100])
EXPECTED_AGE_ORDER = ["0 to 9", "20 to 99"]
FLAGS = [True, False, True]
EXPECTED_FLAG_ORDER = ["False", "True"]


def build_points(colors: list[str] | list[int] | list[bool]) -> ndp.Table:
	"""
	Return a Table of points with one color_by value each.

	.. versionadded:: 0.2.0

	Parameters
	----------
	colors
		The color_by value of each point.

	Returns
	-------
	ndp.Table
		The columns x, y and group.
	"""
	point_count = len(colors)
	positions = [float(position) for position in range(point_count)]
	x_values = ndp.Array.from_list(positions)
	y_values = ndp.Array.from_list(positions)
	groups = ndp.Array.from_list(colors)
	points = ndp.Table.from_arrays({"x": x_values, "y": y_values, "group": groups})

	return points


def draw_groups(points: ndp.Table) -> Axes:
	"""
	Return the matplotlib axes of a scatter Plot colored by the group column.

	.. versionadded:: 0.2.0

	Parameters
	----------
	points
		A Table with the columns x, y and group.

	Returns
	-------
	Axes
		The axes of the drawn Plot.
	"""
	chart = ndp.ScatterChart(x="x", y="y", color_by="group")
	plot = ndp.Plot.scatter(points, chart)
	figure = plot.to_matplotlib()
	axes = figure.axes[0]

	return axes


def read_legend_texts(axes: Axes) -> list[str]:
	"""
	Return the texts of the legend of an axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		A matplotlib axes with a legend.

	Returns
	-------
	list[str]
		The texts, from the top of the legend.
	"""
	legend = axes.get_legend()
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]

	return legend_texts


def read_group_colors(axes: Axes) -> dict[str, list[float]]:
	"""
	Return the color of the points of each group of an axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		A matplotlib axes with one collection of points per group.

	Returns
	-------
	dict[str, list[float]]
		The red, green, blue and opacity parts of each group.
	"""
	group_colors = dict[str, list[float]]()

	for points in axes.collections:
		raw_face_colors = points.get_facecolor()
		face_colors = numpy.asarray(raw_face_colors, dtype=numpy.float64)
		first_color = face_colors[0]
		raw_color_parts = first_color.tolist()
		color_parts = cast(list[float], raw_color_parts)
		group_label = points.get_label()
		group_name = str(group_label)
		group_colors[group_name] = color_parts

	return group_colors


def test_cluster_names_are_in_natural_order() -> None:
	"""
	Check that the legend lists Cluster 2 before Cluster 10, whatever the order of the rows.

	.. versionadded:: 0.2.0
	"""
	points = build_points(CLUSTER_NAMES)

	axes = draw_groups(points)

	legend_texts = read_legend_texts(axes)
	assert legend_texts == EXPECTED_CLUSTER_ORDER


def test_a_group_keeps_its_color_when_the_rows_are_reversed() -> None:
	"""
	Check that each group takes the same color whatever the order of the rows.

	.. versionadded:: 0.2.0
	"""
	reversed_names = CLUSTER_NAMES[::-1]
	points = build_points(CLUSTER_NAMES)
	reversed_points = build_points(reversed_names)

	axes = draw_groups(points)
	reversed_axes = draw_groups(reversed_points)

	group_colors = read_group_colors(axes)
	reversed_group_colors = read_group_colors(reversed_axes)
	assert group_colors == reversed_group_colors


def test_categories_keep_their_order() -> None:
	"""
	Check that a color_by column of categories follows the order of its categories, without the empty ones.

	.. versionadded:: 0.2.0
	"""
	points = build_points(AGES)
	conversion = ndp.TableConversion(columns=["group"], dtype=ndp.Type.CATEGORY, format=AGE_BRACKETS)
	age_points = points.convert(conversion)

	axes = draw_groups(age_points)

	legend_texts = read_legend_texts(axes)
	assert legend_texts == EXPECTED_AGE_ORDER


def test_false_comes_before_true() -> None:
	"""
	Check that the groups of a boolean color_by column list False first.

	.. versionadded:: 0.2.0
	"""
	points = build_points(FLAGS)

	axes = draw_groups(points)

	legend_texts = read_legend_texts(axes)
	assert legend_texts == EXPECTED_FLAG_ORDER
