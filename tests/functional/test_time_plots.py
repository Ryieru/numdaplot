"""
Functional tests of the Plots of Tables holding times of day.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from datetime import time

import numpy
from matplotlib.axes import Axes
from matplotlib.text import Text

import numdaplot as ndp

HOURS = ndp.Array.from_list([time(8), time(12, 30), time(18, 15), time(23)])
COUNTS = ndp.Array.from_list([3.0, 5.0, 2.0, 4.0])
ACCIDENTS = ndp.Table.from_arrays({"hour": HOURS, "count": COUNTS})
COUNT_COLUMNS = ["count"]
EXPECTED_HOURS = [8.0, 12.5, 18.25, 23.0]
EXPECTED_HOUR_LABELS = ["08:00", "12:30", "18:15", "23:00"]
EXPECTED_DAY_LABELS = ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00", "24:00"]
DATE_LABEL_ROTATION = 45.0
SINGLE_LINE_COUNT = 1


def draw_axes(plot: ndp.Plot) -> Axes:
	"""
	Return the drawn axes of a Plot, its tick labels placed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		A Plot of one chart.

	Returns
	-------
	Axes
		The matplotlib axes of the chart.
	"""
	figure = plot.to_matplotlib()
	figure.draw_without_rendering()
	axes = figure.axes[0]

	return axes


def read_texts(text_objects: Sequence[Text]) -> list[str]:
	"""
	Return the texts of matplotlib text objects: tick labels, legend entries or slice names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text_objects
		The matplotlib text objects.

	Returns
	-------
	list[str]
		The texts, in the same order.
	"""
	texts = [text_object.get_text() for text_object in text_objects]

	return texts


def test_a_plot_of_a_table_holding_an_unused_time_column_is_drawn() -> None:
	"""
	Check that a column of times of day left out of the chart does not stop the Plot.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.LineChart(y=COUNT_COLUMNS)
	plot = ndp.Plot.line(ACCIDENTS, chart)

	axes = draw_axes(plot)

	line_count = len(axes.lines)
	assert line_count == SINGLE_LINE_COUNT


def test_a_line_plot_places_times_of_day_at_their_hours() -> None:
	"""
	Check that times of day are placed at their hours, under labels every three hours.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.LineChart(x="hour", y=COUNT_COLUMNS)
	plot = ndp.Plot.line(ACCIDENTS, chart)

	axes = draw_axes(plot)

	first_line = axes.lines[0]
	line_positions = first_line.get_xdata()
	positions = numpy.asarray(line_positions, dtype=numpy.float64)
	position_list = positions.tolist()
	tick_labels = axes.get_xticklabels()
	labels = read_texts(tick_labels)
	assert position_list == EXPECTED_HOURS
	assert labels == EXPECTED_DAY_LABELS


def test_times_of_day_on_the_x_axis_are_rotated_like_dates() -> None:
	"""
	Check that the labels of times of day are rotated as the labels of dates.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.LineChart(x="hour", y=COUNT_COLUMNS)
	plot = ndp.Plot.line(ACCIDENTS, chart)

	axes = draw_axes(plot)

	tick_labels = axes.get_xticklabels()
	first_label = tick_labels[0]
	rotation = first_label.get_rotation()
	assert rotation == DATE_LABEL_ROTATION


def test_a_bar_plot_labels_each_bar_with_its_time_of_day() -> None:
	"""
	Check that each bar is placed at its hour and labeled with it.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BarChart(x="hour", y=COUNT_COLUMNS)
	plot = ndp.Plot.bar(ACCIDENTS, chart)

	axes = draw_axes(plot)

	tick_labels = axes.get_xticklabels()
	labels = read_texts(tick_labels)
	assert labels == EXPECTED_HOUR_LABELS


def test_a_scatter_plot_places_each_point_at_its_hour() -> None:
	"""
	Check that each point of a scatter Plot is placed at its hour.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="hour", y="count")
	plot = ndp.Plot.scatter(ACCIDENTS, chart)

	axes = draw_axes(plot)

	points = axes.collections[0]
	offsets = points.get_offsets()
	point_positions = numpy.asarray(offsets, dtype=numpy.float64)
	x_positions = point_positions[:, 0]
	x_position_list = x_positions.tolist()
	assert x_position_list == EXPECTED_HOURS


def test_a_heatmap_names_its_rows_with_times_of_day() -> None:
	"""
	Check that the rows of a heatmap are named with their times of day.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HeatmapChart(columns=COUNT_COLUMNS, labels="hour")
	plot = ndp.Plot.heatmap(ACCIDENTS, chart)

	axes = draw_axes(plot)

	tick_labels = axes.get_yticklabels()
	labels = read_texts(tick_labels)
	assert labels == EXPECTED_HOUR_LABELS


def test_a_pie_names_its_slices_with_times_of_day() -> None:
	"""
	Check that the slices of a pie are named with their times of day.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="hour", values="count")
	plot = ndp.Plot.pie(ACCIDENTS, chart)

	axes = draw_axes(plot)

	slice_count = len(EXPECTED_HOUR_LABELS)
	slice_texts = axes.texts[:slice_count]
	labels = read_texts(slice_texts)
	assert labels == EXPECTED_HOUR_LABELS


def test_a_scatter_plot_colored_by_time_of_day_names_each_time_in_the_legend() -> None:
	"""
	Check that each time of day of color_by is named in the legend.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="count", y="count", color_by="hour")
	plot = ndp.Plot.scatter(ACCIDENTS, chart)

	axes = draw_axes(plot)

	legend = axes.get_legend()
	assert legend is not None
	legend_texts = legend.get_texts()
	labels = read_texts(legend_texts)
	assert labels == EXPECTED_HOUR_LABELS


def test_a_box_plot_grouped_by_time_of_day_names_each_box_with_its_time() -> None:
	"""
	Check that each box of group_by is named with its time of day.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BoxChart(columns=COUNT_COLUMNS, group_by="hour")
	plot = ndp.Plot.box(ACCIDENTS, chart)

	axes = draw_axes(plot)

	tick_labels = axes.get_xticklabels()
	labels = read_texts(tick_labels)
	assert labels == EXPECTED_HOUR_LABELS
