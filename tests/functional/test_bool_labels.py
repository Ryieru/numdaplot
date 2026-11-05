"""
Functional tests of the columns of booleans used as labels or groups by the charts.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from collections.abc import Callable
from typing import Any

import pandas
import pytest

import numdaplot as ndp

TRIPS = ndp.Table.from_arrays(
	{
		"weekend": ndp.Array.from_list([True, False, True, False]),
		"fare": ndp.Array.from_list([1.0, 2.0, 3.0, 4.0]),
	}
)
EXPECTED_LABELS = ["False", "True"]
MESSAGE_FORMAT = "Cannot apply {chart_name} to the BOOL column 'weekend'."


def read_x_labels(plot: ndp.Plot) -> list[str]:
	"""
	Return the labels of the horizontal axis of a Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		The Plot.

	Returns
	-------
	list[str]
		The texts of the labels.
	"""
	labels = plot.to_matplotlib().axes[0].get_xticklabels()
	label_texts = [label.get_text() for label in labels]

	return label_texts


def test_box_groups_are_named_after_booleans() -> None:
	"""
	Check one box per boolean, False first as in alphabetical order.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_box(TRIPS, ndp.BoxChart(columns=["fare"], group_by="weekend"))

	label_texts = read_x_labels(plot)

	assert label_texts == EXPECTED_LABELS


def test_points_are_colored_by_booleans_named_in_the_legend() -> None:
	"""
	Check one color per boolean, named in the legend.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_scatter(TRIPS, ndp.ScatterChart(x="fare", y="fare", color_by="weekend"))

	legend = plot.to_matplotlib().axes[0].get_legend()

	assert legend is not None
	legend_names = sorted(text.get_text() for text in legend.get_texts())
	assert legend_names == EXPECTED_LABELS


def test_bars_are_labeled_with_booleans() -> None:
	"""
	Check the labels of bars, one per row.

	.. versionadded:: 0.1.0
	"""
	totals = TRIPS.aggregate(
		ndp.Aggregation(calculations=[ndp.Calculation(column="fare", function=ndp.Sum())], group_by=["weekend"])
	)

	plot = ndp.plot_bar(totals, ndp.BarChart(x="weekend", y=["fare_sum"]))

	label_texts = read_x_labels(plot)
	assert label_texts == EXPECTED_LABELS


def test_slices_are_named_after_booleans() -> None:
	"""
	Check the names of the slices of a pie.

	.. versionadded:: 0.1.0
	"""
	totals = TRIPS.aggregate(
		ndp.Aggregation(calculations=[ndp.Calculation(column="fare", function=ndp.Sum())], group_by=["weekend"])
	)

	plot = ndp.plot_pie(totals, ndp.PieChart(labels="weekend", values="fare_sum"))

	slice_names = {text.get_text() for text in plot.to_matplotlib().axes[0].texts}
	assert set(EXPECTED_LABELS) <= slice_names


def test_heatmap_rows_are_labeled_with_booleans() -> None:
	"""
	Check the labels of the rows of a heatmap.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_heatmap(TRIPS, ndp.HeatmapChart(columns=["fare"], labels="weekend"))

	labels = plot.to_matplotlib().axes[0].get_yticklabels()
	label_texts = [label.get_text() for label in labels]
	assert label_texts == ["True", "False", "True", "False"]


@pytest.mark.parametrize(
	"draw",
	[
		lambda: ndp.plot_line(TRIPS, ndp.LineChart(x="weekend", y=["fare"])),
		lambda: ndp.plot_scatter(TRIPS, ndp.ScatterChart(x="weekend", y="fare")),
	],
)
def test_lines_and_points_are_placed_on_booleans(draw: Callable[[], ndp.Plot]) -> None:
	"""
	Check that ``x`` accepts booleans, like texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	draw
		The drawing.
	"""
	plot = draw()

	label_texts = read_x_labels(plot)
	assert set(label_texts) == set(EXPECTED_LABELS)


def test_a_row_with_a_missing_boolean_is_left_out_of_the_groups() -> None:
	"""
	Check that a missing boolean behaves like a missing text.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame(
		{
			"fare": pandas.Series([1.0, 2.0, 3.0]),
			"weekend": pandas.Series([True, None, False], dtype="boolean"),
		}
	)
	with_missing = ndp.Table.from_pandas(frame)

	plot = ndp.plot_box(with_missing, ndp.BoxChart(columns=["fare"], group_by="weekend"))

	label_texts = read_x_labels(plot)
	assert label_texts == EXPECTED_LABELS


@pytest.mark.parametrize(
	("draw", "chart_name"),
	[
		(lambda: ndp.plot_line(TRIPS, ndp.LineChart(x="fare", y=["weekend"])), "LineChart"),
		(lambda: ndp.plot_bar(TRIPS, ndp.BarChart(x="fare", y=["weekend"])), "BarChart"),
		(lambda: ndp.plot_scatter(TRIPS, ndp.ScatterChart(x="fare", y="weekend")), "ScatterChart"),
		(lambda: ndp.plot_scatter(TRIPS, ndp.ScatterChart(x="fare", y="fare", size_by="weekend")), "ScatterChart"),
		(lambda: ndp.plot_histogram(TRIPS, ndp.HistogramChart(columns=["weekend"])), "HistogramChart"),
		(lambda: ndp.plot_box(TRIPS, ndp.BoxChart(columns=["weekend"])), "BoxChart"),
		(lambda: ndp.plot_pie(TRIPS, ndp.PieChart(labels="weekend", values="weekend")), "PieChart"),
		(lambda: ndp.plot_heatmap(TRIPS, ndp.HeatmapChart(columns=["weekend"])), "HeatmapChart"),
	],
)
def test_booleans_stay_refused_as_measured_values(draw: Callable[[], Any], chart_name: str) -> None:
	"""
	Check the roles where a boolean has no clear meaning.

	.. versionadded:: 0.1.0

	Parameters
	----------
	draw
		The drawing.
	chart_name
		The chart named by the error.
	"""
	expected_message = MESSAGE_FORMAT.format(chart_name=chart_name)

	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		draw()

	error_text = str(error_info.value)
	assert error_text == expected_message


def test_integers_stay_refused_as_box_groups() -> None:
	"""
	Check that ``group_by`` of a BoxChart keeps refusing numbers.

	.. versionadded:: 0.1.0
	"""
	table = ndp.Table.from_arrays({"hour": ndp.Array.from_list([1, 2]), "fare": ndp.Array.from_list([1.0, 2.0])})

	with pytest.raises(ndp.IncompatibleTypesError):
		ndp.plot_box(table, ndp.BoxChart(columns=["fare"], group_by="hour"))
