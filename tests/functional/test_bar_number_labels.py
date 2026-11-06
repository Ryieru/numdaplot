"""
Functional tests of the labels of numbers below the bars of a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import pytest

import numdaplot as ndp

ROTATED = 45.0
HORIZONTAL = 0.0
FEW_VALUES = list(range(10))
HOURS = list(range(24))
SIX_YEARS = list(range(2000, 2006))
YEARS = list(range(2000, 2024))
UNEVEN_VALUES = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
WIDE_SIZE = ndp.Size(width=14.0, height=4.0)
NARROW_SIZE = ndp.Size(width=2.5, height=4.0)


def build_bars(values: list[int]) -> ndp.Table:
	"""
	Return a Table with a number per bar.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values below the bars.

	Returns
	-------
	Table
		The columns ``x`` and ``y``.
	"""
	heights = [1.0] * len(values)
	table = ndp.Table.from_arrays({"x": ndp.Array.from_list(values), "y": ndp.Array.from_list(heights)})

	return table


def read_rotation(plot: ndp.Plot) -> float:
	"""
	Return the angle of the labels of the horizontal axis of a Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		The Plot.

	Returns
	-------
	float
		The angle in degrees.
	"""
	figure = plot.to_matplotlib()
	labels = figure.axes[0].get_xticklabels()
	rotation = labels[0].get_rotation()

	return rotation


@pytest.mark.parametrize("values", [HOURS, YEARS, UNEVEN_VALUES])
def test_numbers_without_room_are_rotated(values: list[int]) -> None:
	"""
	Check that numbers that would touch are rotated.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values below the bars.
	"""
	table = build_bars(values)

	plot = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]))

	rotation = read_rotation(plot)
	assert rotation == ROTATED


def test_numbers_with_room_stay_horizontal() -> None:
	"""
	Check that few numbers keep their horizontal labels.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(FEW_VALUES)

	plot = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]))

	rotation = read_rotation(plot)
	assert rotation == HORIZONTAL


def test_a_wider_plot_leaves_room_for_the_same_numbers() -> None:
	"""
	Check that the room follows the size of the Plot.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(HOURS)

	plot = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]), ndp.PlotStyle(size=WIDE_SIZE))

	rotation = read_rotation(plot)
	assert rotation == HORIZONTAL


def test_a_narrower_plot_rotates_the_same_numbers() -> None:
	"""
	Check that numbers fitting at the default size are rotated in a narrow Plot.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(SIX_YEARS)
	plot_at_default_size = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]))
	default_rotation = read_rotation(plot_at_default_size)

	plot = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]), ndp.PlotStyle(size=NARROW_SIZE))

	rotation = read_rotation(plot)
	assert default_rotation == HORIZONTAL
	assert rotation == ROTATED


def test_a_chosen_rotation_wins_over_the_room() -> None:
	"""
	Check that ``x_tick_rotation`` keeps numbers horizontal, even without room.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(YEARS)

	plot = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]), ndp.PlotStyle(x_tick_rotation=0.0))

	rotation = read_rotation(plot)
	assert rotation == HORIZONTAL


def test_a_line_chart_keeps_horizontal_numbers() -> None:
	"""
	Check that matplotlib, which chooses the labels of a line chart, keeps them horizontal.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(YEARS)

	plot = ndp.Plot.line(table, ndp.LineChart(x="x", y=["y"]))

	rotation = read_rotation(plot)
	assert rotation == HORIZONTAL


def test_a_line_on_the_right_of_bars_rotates_their_numbers() -> None:
	"""
	Check the chart of the hours with a line on a second axis.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(HOURS)
	bars = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]))

	both = bars.add_line(table, ndp.LineChart(x="x", y=["y"]), ndp.ValueAxis.RIGHT)

	rotation = read_rotation(both)
	assert rotation == ROTATED


def test_a_plot_in_a_small_figure_cell_rotates_its_numbers() -> None:
	"""
	Check that the room follows the cell of a Figure.

	.. versionadded:: 0.1.0
	"""
	table = build_bars(FEW_VALUES)
	plot = ndp.Plot.bar(table, ndp.BarChart(x="x", y=["y"]))
	figure = ndp.Figure(ndp.Layout(rows=1, columns=4), ndp.FigureStyle(size=ndp.Size(width=6.4, height=4.8)))
	figure = figure.place(plot, ndp.Cell(row=0, column=0))

	matplotlib_figure = figure.to_matplotlib()

	labels = matplotlib_figure.axes[0].get_xticklabels()
	rotation = labels[0].get_rotation()
	assert rotation == ROTATED
