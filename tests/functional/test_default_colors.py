"""
Functional tests of the default colors of the series and groups of a chart.

.. versionadded:: 0.2.0
"""

import warnings
from typing import cast

import numpy
import pytest
from matplotlib.collections import PathCollection
from matplotlib.colors import to_hex

import numdaplot as ndp

CLUSTER_COUNT = 17
CROWDED_COUNT = 21
CLUSTER_NAME = "Cluster {number}"


def build_clusters(group_count: int) -> ndp.Table:
	"""
	Return one point per cluster, each cluster named by a text.

	.. versionadded:: 0.2.0

	Parameters
	----------
	group_count
		The number of clusters.

	Returns
	-------
	ndp.Table
		The columns ``x``, ``y`` and ``cluster``.
	"""
	numbers = list(range(group_count))
	names = [CLUSTER_NAME.format(number=number) for number in numbers]
	positions = [float(number) for number in numbers]
	x_values = ndp.Array.from_list(positions)
	y_values = ndp.Array.from_list(positions)
	cluster_names = ndp.Array.from_list(names)
	clusters = ndp.Table.from_arrays({"x": x_values, "y": y_values, "cluster": cluster_names})

	return clusters


def read_group_colors(clusters: ndp.Table) -> list[str]:
	"""
	Return the color of the points of each group of a scatter chart colored by cluster.

	.. versionadded:: 0.2.0

	Parameters
	----------
	clusters
		The points and their cluster.

	Returns
	-------
	list[str]
		One ``#rrggbb`` color per group, in the order of the legend.
	"""
	chart = ndp.ScatterChart(x="x", y="y", color_by="cluster")
	plot = ndp.Plot.scatter(clusters, chart)
	figure = plot.to_matplotlib()
	axes = figure.axes[0]
	point_groups = [cast(PathCollection, collection) for collection in axes.collections]
	face_colors = [points.get_facecolor() for points in point_groups]
	color_rows = [numpy.asarray(face_color, dtype=numpy.float64) for face_color in face_colors]
	group_colors = [to_hex(color_row[0]) for color_row in color_rows]

	return group_colors


def test_seventeen_groups_take_seventeen_different_colors() -> None:
	"""
	Check that every group of a 17 cluster chart has its own color, without warning.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters(CLUSTER_COUNT)

	with warnings.catch_warnings():
		warnings.simplefilter("error")
		group_colors = read_group_colors(clusters)

	distinct_colors = set(group_colors)
	distinct_count = len(distinct_colors)
	assert distinct_count == CLUSTER_COUNT


def test_more_groups_than_colors_warn_that_colors_are_shared() -> None:
	"""
	Check that 21 groups raise a ReadabilityWarning.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters(CROWDED_COUNT)

	with pytest.warns(ndp.ReadabilityWarning):
		read_group_colors(clusters)
