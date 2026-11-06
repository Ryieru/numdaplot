"""
Functional tests of the labels of an axis without enough room.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings
from datetime import date, timedelta

import pytest

import numdaplot as ndp

MANY_VALUES = 60
FEW_VALUES = 20
SHOWN_AT_45 = 20
SHOWN_AT_90 = 30
SHOWN_FLAT = 10
WIDE_SIZE = ndp.Size(width=16.0, height=4.8)
TALL_SIZE = ndp.Size(width=6.4, height=16.0)
SMALL_FONT_ROOM = 2
TEXT_MESSAGE = (
	"The chart shows 20 of its 60 labels so that they stay readable. Give a wider ndp.Size to show more of them."
)
TALL_MESSAGE = (
	"The chart shows 20 of its 60 labels so that they stay readable. Give a taller ndp.Size to show more of them."
)
FIRST_DAY = date(2026, 1, 1)
FIRST_YEAR = 1000
HORIZONTAL_BARS = ndp.BarChart(x="x", y=["y"], orientation=ndp.Orientation.HORIZONTAL)
VERTICAL_BARS = ndp.BarChart(x="x", y=["y"])


def build_table(labels: list[str] | list[int] | list[date]) -> ndp.Table:
	"""
	Return a Table with a label and a height per row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	labels
		The ``x`` values.

	Returns
	-------
	ndp.Table
		The columns ``x`` and ``y``.
	"""
	heights = [1.0] * len(labels)
	table = ndp.Table.from_arrays({"x": ndp.Array.from_list(labels), "y": ndp.Array.from_list(heights)})

	return table


def build_texts(count: int) -> ndp.Table:
	"""
	Return a Table with a text per row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	count
		The number of rows.

	Returns
	-------
	ndp.Table
		The columns ``x`` and ``y``.
	"""
	labels = [f"Z{value:03d}" for value in range(count)]
	table = build_table(labels)

	return table


def count_shown_labels(plot: ndp.Plot, on_vertical_axis: bool = False) -> int:
	"""
	Return the number of labels the positions of a Plot show.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		The Plot.
	on_vertical_axis
		True to read the vertical axis.

	Returns
	-------
	int
		The number of labels.
	"""
	figure = plot.to_matplotlib()
	axes = figure.axes[0]
	labels = axes.get_yticklabels() if on_vertical_axis else axes.get_xticklabels()
	label_count = len(labels)

	return label_count


def test_many_texts_show_the_labels_that_fit_with_a_warning() -> None:
	"""
	Check the labels of 60 bars, and that each bar is still drawn.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	plot = ndp.plot_bar(table, VERTICAL_BARS)

	with pytest.warns(ndp.ReadabilityWarning) as caught_warnings:
		figure = plot.to_matplotlib()

	axes = figure.axes[0]
	labels = axes.get_xticklabels()
	bars = axes.patches
	warning_text = str(caught_warnings[0].message)
	assert len(labels) == SHOWN_AT_45
	assert len(bars) == MANY_VALUES
	assert warning_text == TEXT_MESSAGE


def test_a_warning_points_at_the_line_of_the_user() -> None:
	"""
	Check that the warning does not name a file of the library.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	plot = ndp.plot_bar(table, VERTICAL_BARS)

	with pytest.warns(ndp.ReadabilityWarning) as caught_warnings:
		plot.to_matplotlib()

	warning_file = caught_warnings[0].filename
	assert warning_file == __file__


def test_a_few_texts_show_each_label_without_warning() -> None:
	"""
	Check 20 labels at the default size.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(FEW_VALUES)
	plot = ndp.plot_bar(table, VERTICAL_BARS)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		shown_count = count_shown_labels(plot)

	assert shown_count == FEW_VALUES
	assert caught_warnings == []


def test_a_wider_size_shows_each_label() -> None:
	"""
	Check what the warning advises.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	style = ndp.PlotStyle(size=WIDE_SIZE)
	plot = ndp.plot_bar(table, VERTICAL_BARS, style)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		shown_count = count_shown_labels(plot)

	assert shown_count == MANY_VALUES
	assert caught_warnings == []


def test_many_numbers_show_the_labels_that_fit_without_warning() -> None:
	"""
	Check numbers, which a reader can find from their neighbors.

	.. versionadded:: 0.1.0
	"""
	values = [FIRST_YEAR + value for value in range(MANY_VALUES)]
	table = build_table(values)
	plot = ndp.plot_bar(table, VERTICAL_BARS)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		shown_count = count_shown_labels(plot)

	assert shown_count == SHOWN_AT_45
	assert caught_warnings == []


def test_many_dates_show_the_labels_that_fit_without_warning() -> None:
	"""
	Check dates, which a reader can find from their neighbors.

	.. versionadded:: 0.1.0
	"""
	days = [FIRST_DAY + timedelta(days=value) for value in range(MANY_VALUES)]
	table = build_table(days)
	plot = ndp.plot_bar(table, VERTICAL_BARS)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		shown_count = count_shown_labels(plot)

	assert shown_count == SHOWN_AT_45
	assert caught_warnings == []


@pytest.mark.parametrize(("rotation", "expected_count"), [(90.0, SHOWN_AT_90), (0.0, SHOWN_FLAT), (-45.0, SHOWN_AT_45)])
def test_a_chosen_angle_changes_the_labels_that_fit(rotation: float, expected_count: int) -> None:
	"""
	Check that upright labels need less room and flat labels more.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	style = ndp.PlotStyle(x_tick_rotation=rotation)
	plot = ndp.plot_bar(table, VERTICAL_BARS, style)

	with pytest.warns(ndp.ReadabilityWarning):
		shown_count = count_shown_labels(plot)

	assert shown_count == expected_count


def test_labels_kept_take_the_chosen_angle() -> None:
	"""
	Check that leaving labels out does not lose their rotation.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	plot = ndp.plot_bar(table, VERTICAL_BARS)

	with pytest.warns(ndp.ReadabilityWarning):
		figure = plot.to_matplotlib()

	labels = figure.axes[0].get_xticklabels()
	rotations = {label.get_rotation() for label in labels}
	assert rotations == {45.0}


def test_horizontal_bars_show_the_labels_that_fit_with_a_taller_advice() -> None:
	"""
	Check the labels on the vertical axis.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	plot = ndp.plot_bar(table, HORIZONTAL_BARS)

	with pytest.warns(ndp.ReadabilityWarning) as caught_warnings:
		shown_count = count_shown_labels(plot, True)

	warning_text = str(caught_warnings[0].message)
	assert shown_count == SHOWN_AT_45
	assert warning_text == TALL_MESSAGE


def test_a_taller_size_shows_each_label_of_horizontal_bars() -> None:
	"""
	Check what the warning advises on the vertical axis.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(MANY_VALUES)
	style = ndp.PlotStyle(size=TALL_SIZE)
	plot = ndp.plot_bar(table, HORIZONTAL_BARS, style)

	shown_count = count_shown_labels(plot, True)

	assert shown_count == MANY_VALUES


def build_heatmap(row_count: int, column_count: int) -> ndp.Plot:
	"""
	Return a heatmap of a number of rows and columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row_count
		The number of rows.
	column_count
		The number of columns.

	Returns
	-------
	ndp.Plot
		The heatmap.
	"""
	names = [f"row{value:03d}" for value in range(row_count)]
	column_names = [f"col{value:03d}" for value in range(column_count)]
	columns = {"name": ndp.Array.from_list(names)}
	values = ndp.Array.from_list([1.0] * row_count)
	for column_name in column_names:
		columns[column_name] = values

	table = ndp.Table.from_arrays(columns)
	chart = ndp.HeatmapChart(labels="name", columns=column_names)
	plot = ndp.plot_heatmap(table, chart)

	return plot


def test_a_heatmap_with_many_columns_shows_the_labels_that_fit() -> None:
	"""
	Check the names of the columns.

	.. versionadded:: 0.1.0
	"""
	plot = build_heatmap(SMALL_FONT_ROOM, MANY_VALUES)

	with pytest.warns(ndp.ReadabilityWarning):
		shown_count = count_shown_labels(plot)

	assert shown_count == SHOWN_AT_45


def test_a_heatmap_with_many_rows_shows_the_labels_that_fit() -> None:
	"""
	Check the names of the rows, read as ``y`` values.

	.. versionadded:: 0.1.0
	"""
	plot = build_heatmap(MANY_VALUES, SMALL_FONT_ROOM)

	with pytest.warns(ndp.ReadabilityWarning):
		shown_count = count_shown_labels(plot, True)

	assert shown_count == SHOWN_AT_45


def test_a_line_keeps_the_dates_chosen_by_matplotlib() -> None:
	"""
	Check that labels already chosen according to the room are left alone.

	.. versionadded:: 0.1.0
	"""
	days = [FIRST_DAY + timedelta(days=value) for value in range(MANY_VALUES)]
	table = build_table(days)
	plot = ndp.plot_line(table, ndp.LineChart(x="x", y=["y"]))

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		shown_count = count_shown_labels(plot)

	assert 0 < shown_count < MANY_VALUES
	assert caught_warnings == []


def test_a_plot_in_a_figure_shows_the_labels_that_fit_its_cell() -> None:
	"""
	Check that a Plot placed in a cell counts the room of its cell, not of the whole Figure.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(FEW_VALUES)
	plot = ndp.plot_bar(table, VERTICAL_BARS)
	layout = ndp.Layout(rows=1, columns=2)
	figure = ndp.Figure(layout)
	figure = figure.place(plot, ndp.Cell(row=0, column=0))

	with pytest.warns(ndp.ReadabilityWarning):
		matplotlib_figure = figure.to_matplotlib()

	labels = matplotlib_figure.axes[0].get_xticklabels()
	assert 0 < len(labels) < FEW_VALUES
