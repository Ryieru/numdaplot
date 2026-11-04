"""
Functional tests of the heatmaps of Tables and Arrays.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from datetime import date
from typing import Any, cast

import numpy
import pandas

import numdaplot as ndp

ORDERS_FRAME = pandas.DataFrame(
	{
		"day": ["Mon", "Tue", None],
		"morning": [12.0, -3.0, 5.0],
		"noon": [30.0, None, 7.0],
	}
)
ORDERS = ndp.Table.from_pandas(ORDERS_FRAME)
SLOTS = ["morning", "noon"]
EXPECTED_DAYS = ["Mon", "Tue"]
EXPECTED_SLOTS = ["morning", "noon"]
EXPECTED_MASK = [[False, False], [False, True]]
EXPECTED_TEXTS = ["12", "30", "-3"]
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
DATES = ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 2)])
TEMPERATURES = ndp.Array.from_list([3.5, 4.0])
WEATHER = ndp.Table.from_arrays({"day": DATES, "temperature": TEMPERATURES})


def test_a_heatmap_colors_each_value_with_the_row_labels_and_column_names() -> None:
	"""
	Check the labels, the missing day left out, the missing value masked and the written values.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HeatmapChart(columns=SLOTS, labels="day", values=ndp.CellValues.SHOWN)

	plot = ndp.plot_heatmap(ORDERS, chart)

	figure = plot.to_matplotlib()
	axes = figure.axes[0]
	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	day_labels = [label.get_text() for label in axes.get_yticklabels()]
	slot_labels = [label.get_text() for label in axes.get_xticklabels()]
	cell_texts = [text.get_text() for text in axes.texts]
	assert numpy.ma.getmaskarray(cells).tolist() == EXPECTED_MASK
	assert day_labels == EXPECTED_DAYS
	assert slot_labels == EXPECTED_SLOTS
	assert cell_texts == EXPECTED_TEXTS
	assert axes.get_ylabel() == "day"
	assert len(figure.axes) == 2


def test_a_red_blue_heatmap_is_centered_on_zero() -> None:
	"""
	Check that values on both sides of 0 put 0 in the middle of the scale.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HeatmapChart(columns=SLOTS, labels="day", scale=ndp.ColorScale.RED_BLUE)

	plot = ndp.plot_heatmap(ORDERS, chart)

	axes = plot.to_matplotlib().axes[0]
	lowest, highest = axes.images[0].get_clim()
	assert lowest == -highest


def test_a_heatmap_of_an_array_numbers_its_rows_and_columns() -> None:
	"""
	Check that an Array labels its rows and columns with their numbers.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_heatmap(GRID, ndp.HeatmapChart())

	axes = plot.to_matplotlib().axes[0]
	row_labels = [label.get_text() for label in axes.get_yticklabels()]
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert row_labels == ["0", "1", "2"]
	assert column_labels == ["0", "1"]


def test_a_heatmap_labels_its_rows_with_dates() -> None:
	"""
	Check that a column of dates labels the rows with their dates.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HeatmapChart(columns=["temperature"], labels="day")

	plot = ndp.plot_heatmap(WEATHER, chart)

	axes = plot.to_matplotlib().axes[0]
	row_labels = [label.get_text() for label in axes.get_yticklabels()]
	assert row_labels == ["2026-01-01", "2026-01-02"]
