"""
Functional tests of the place of the legend of a Plot.

.. versionadded:: 0.2.0
"""

from matplotlib.figure import Figure

import numdaplot as ndp

GRID_SIZE = 6
GROUP_NAME = "group {number}"
DAYS = ndp.Array.from_list([1, 2, 3, 4])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
COSTS = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "cost": COSTS})


def build_crowded_points() -> ndp.Table:
	"""
	Return a grid of points filling the whole chart, each column of the grid a group of its own.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The columns ``x``, ``y`` and ``group``.
	"""
	x_list = list[float]()
	y_list = list[float]()
	group_list = list[str]()

	for i in range(GRID_SIZE):
		for j in range(GRID_SIZE):
			group_name = GROUP_NAME.format(number=i)
			x_value = float(i)
			y_value = float(j)
			x_list.append(x_value)
			y_list.append(y_value)
			group_list.append(group_name)

	x_values = ndp.Array.from_list(x_list)
	y_values = ndp.Array.from_list(y_list)
	groups = ndp.Array.from_list(group_list)
	points = ndp.Table.from_arrays({"x": x_values, "y": y_values, "group": groups})

	return points


def is_legend_past_axes(figure: Figure) -> bool:
	"""
	Return whether the legend of a laid out figure starts on the right of its axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	figure
		The figure of a Plot with a legend.

	Returns
	-------
	bool
		True when the legend is past the axes.
	"""
	figure.draw_without_rendering()
	axes = figure.axes[0]
	legend = axes.get_legend()
	assert legend is not None
	legend_box = legend.get_window_extent()
	is_past = bool(legend_box.x0 > axes.bbox.x1)

	return is_past


def test_best_legend_goes_past_the_axes_when_it_would_hide_points() -> None:
	"""
	Check that the default legend leaves a chart full of points.

	.. versionadded:: 0.2.0
	"""
	points = build_crowded_points()
	plot = ndp.Plot.scatter(points, ndp.ScatterChart(x="x", y="y", color_by="group"))

	figure = plot.to_matplotlib()

	is_past = is_legend_past_axes(figure)
	assert is_past


def test_best_legend_stays_inside_in_a_free_corner() -> None:
	"""
	Check that the default legend of two lines stays inside, where it hides nothing.

	.. versionadded:: 0.2.0
	"""
	plot = ndp.Plot.line(SALES, ndp.LineChart(x="day", y=["price", "cost"]))

	figure = plot.to_matplotlib()

	is_past = is_legend_past_axes(figure)
	assert not is_past


def test_a_chosen_corner_keeps_the_legend_over_the_points() -> None:
	"""
	Check that a legend placed at a chosen corner stays there, even over points.

	.. versionadded:: 0.2.0
	"""
	points = build_crowded_points()
	style = ndp.PlotStyle(legend=ndp.LegendPosition.UPPER_LEFT)
	plot = ndp.Plot.scatter(points, ndp.ScatterChart(x="x", y="y", color_by="group"), style)

	figure = plot.to_matplotlib()

	is_past = is_legend_past_axes(figure)
	assert not is_past
