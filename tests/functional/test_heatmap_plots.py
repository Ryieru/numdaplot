"""
Functional tests of the heatmaps of Tables and Arrays.

.. versionadded:: 0.1.0
"""

import warnings

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false
from datetime import date
from typing import Any, cast

import numpy
import pandas
import pytest

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
TALL_ROW_COUNT = 3000
TALL_COLUMN_COUNT = 2
TALL_VALUE = 100.0
SMALL_HEIGHT = 3.0
LARGE_HEIGHT = 8.0
MEAN_TOLERANCE = 1.0
SMALL_CELL_COUNT = 4


def test_a_heatmap_colors_each_value_with_the_row_labels_and_column_names() -> None:
	"""
	Check the labels, the missing day left out, the missing value masked and the written values.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HeatmapChart(columns=SLOTS, labels="day", values=ndp.CellValues.SHOWN)

	plot = ndp.Plot.heatmap(ORDERS, chart)

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

	plot = ndp.Plot.heatmap(ORDERS, chart)

	axes = plot.to_matplotlib().axes[0]
	lowest, highest = axes.images[0].get_clim()
	assert lowest == -highest


def test_a_heatmap_of_an_array_numbers_its_rows_and_columns() -> None:
	"""
	Check that an Array labels its rows and columns with their numbers.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.heatmap(GRID, ndp.HeatmapChart())

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

	plot = ndp.Plot.heatmap(WEATHER, chart)

	axes = plot.to_matplotlib().axes[0]
	row_labels = [label.get_text() for label in axes.get_yticklabels()]
	assert row_labels == ["2026-01-01", "2026-01-02"]


def build_tall_grid() -> ndp.Array:
	"""
	Return a grid with more rows than an image has pixels, half of it at the highest value.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Array
		The first half of the rows at 0, the second half at 100.
	"""
	numbers = numpy.zeros((TALL_ROW_COUNT, TALL_COLUMN_COUNT))
	numbers[TALL_ROW_COUNT // 2 :] = TALL_VALUE
	grid = ndp.Array.from_numpy(numbers)

	return grid


def test_a_tall_heatmap_shows_means_with_a_warning() -> None:
	"""
	Check that merged cells keep their place on the rows, and that a warning tells they are means.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.heatmap(build_tall_grid())

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		axes = plot.to_matplotlib().axes[0]

	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	message = str(caught_warnings[0].message)
	bottom, top = axes.get_ylim()
	assert caught_warnings[0].category is ndp.ReadabilityWarning
	assert "each band shows the mean" in message
	assert caught_warnings[0].filename == __file__
	assert cells.shape[0] < TALL_ROW_COUNT
	assert (bottom, top) == (TALL_ROW_COUNT - 0.5, -0.5)


def test_a_tall_heatmap_does_not_depend_on_the_size_of_the_image() -> None:
	"""
	Check that two heights show the same share of high values, up to a band.

	.. versionadded:: 0.1.0
	"""
	shares = list[float]()

	for height in (SMALL_HEIGHT, LARGE_HEIGHT):
		style = ndp.PlotStyle(size=ndp.Size(height=height))
		plot = ndp.Plot.heatmap(build_tall_grid(), style=style)

		with pytest.warns(ndp.ReadabilityWarning):
			image = plot.to_matplotlib().axes[0].images[0]

		# Some versions of the matplotlib stubs leave the cells of an image untyped.
		cells = cast(numpy.ma.MaskedArray[Any, Any], image.get_array())
		share = cast(float, cells.mean())
		shares.append(share)

	assert shares[0] == pytest.approx(TALL_VALUE / 2, abs=MEAN_TOLERANCE)
	assert shares[1] == pytest.approx(TALL_VALUE / 2, abs=MEAN_TOLERANCE)


def test_a_tall_heatmap_does_not_write_the_values_of_its_cells() -> None:
	"""
	Check that the warning says so when the values are asked for.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HeatmapChart(values=ndp.CellValues.SHOWN)
	plot = ndp.Plot.heatmap(build_tall_grid(), chart)

	with pytest.warns(ndp.ReadabilityWarning, match="values of the cells are not written"):
		axes = plot.to_matplotlib().axes[0]

	text_count = len(axes.texts)
	assert text_count == 0


def test_a_small_heatmap_still_writes_its_values_without_warning() -> None:
	"""
	Check that a heatmap that fits writes each value, and warns of nothing.

	.. versionadded:: 0.1.0
	"""
	numbers = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	plot = ndp.Plot.heatmap(numbers, ndp.HeatmapChart(values=ndp.CellValues.SHOWN))

	with warnings.catch_warnings():
		warnings.simplefilter("error")
		axes = plot.to_matplotlib().axes[0]

	text_count = len(axes.texts)
	assert text_count == SMALL_CELL_COUNT
