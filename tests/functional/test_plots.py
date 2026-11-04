"""
Functional tests of the line, bar and scatter Plots of Tables and Arrays.

.. versionadded:: 0.1.0
"""

import struct
from datetime import date
from pathlib import Path

import numpy
import pandas
import pytest

import numdaplot as ndp

DAYS = ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3)])
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
COSTS = ndp.Array.from_list([8.0, None, 9.0])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "cost": COSTS})
CITY_FRAME = pandas.DataFrame(
	{"city": ["Paris", "Lyon", None], "2025": [120.0, 80.0, 45.0], "2026": [150.0, 95.0, 40.0]}
)
CITY_SALES = ndp.Table.from_pandas(CITY_FRAME)
FLATS = ndp.Table.from_arrays(
	{
		"surface": ndp.Array.from_list([30.0, 45.0, 60.0, 80.0]),
		"price": ndp.Array.from_list([150.0, 210.0, 260.0, 330.0]),
		"city": ndp.Array.from_list(["Paris", "Lyon", "Paris", "Pau"]),
	}
)
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
STYLE = ndp.Style(title="Sales", x_label="Day", y_label="Euros", legend=ndp.LegendPosition.UPPER_LEFT)
IMAGE_NAMES = ["sales.png", "sales.svg", "sales.pdf"]
IMAGE_STARTS = {"sales.png": b"\x89PNG", "sales.svg": b"<?xml", "sales.pdf": b"%PDF"}
EXPECTED_PIXEL_SIZE = (600, 300)
EXPECTED_SHARP_SIZE = (1280, 960)
PNG_SIZE_START = 16
PNG_SIZE_END = 24
PNG_SIZE_LAYOUT = ">II"


def read_png_size(path: Path) -> tuple[int, int]:
	"""
	Return the width and the height in pixels of a PNG image, written at the start of its file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of a PNG image.

	Returns
	-------
	tuple[int, int]
		The width and the height.
	"""
	image_bytes = path.read_bytes()
	size_bytes = image_bytes[PNG_SIZE_START:PNG_SIZE_END]
	width, height = struct.unpack(PNG_SIZE_LAYOUT, size_bytes)
	image_size = (int(width), int(height))

	return image_size


def test_a_line_plot_of_a_table_draws_each_column_with_the_style() -> None:
	"""
	Check a line Plot of dated prices and costs: lines, labels, title and legend.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.LineChart(x="day", y=["price", "cost"])
	plot = ndp.plot_line(SALES, chart, STYLE)

	axes = plot.to_matplotlib().axes[0]

	legend = axes.get_legend()
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	line_labels = [line.get_label() for line in axes.lines]
	assert line_labels == ["price", "cost"]
	assert legend_texts == ["price", "cost"]
	assert (axes.get_title(), axes.get_xlabel(), axes.get_ylabel()) == ("Sales", "Day", "Euros")


def test_a_line_plot_breaks_its_line_at_a_missing_value() -> None:
	"""
	Check that the missing cost of the second day is not drawn.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_line(SALES, ndp.LineChart(x="day", y=["cost"]))

	axes = plot.to_matplotlib().axes[0]

	costs = numpy.asarray(axes.lines[0].get_ydata(), dtype=numpy.float64)
	missing = numpy.isnan(costs).tolist()
	assert missing == [False, True, False]
	assert axes.get_ylabel() == "cost"


def test_a_line_plot_of_an_array_draws_each_column_at_the_row_numbers() -> None:
	"""
	Check that each column of an Array is a line placed at the row numbers.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_line(GRID, ndp.LineChart())

	axes = plot.to_matplotlib().axes[0]

	line_count = len(axes.lines)
	positions = numpy.asarray(axes.lines[0].get_xdata(), dtype=numpy.float64).tolist()
	assert line_count == 2
	assert positions == [0.0, 1.0, 2.0]


def test_a_bar_plot_labels_each_bar_with_its_city_and_leaves_out_a_missing_city() -> None:
	"""
	Check that each city labels a position, the row without city being left out.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BarChart(x="city", y=["2025", "2026"])
	plot = ndp.plot_bar(CITY_SALES, chart)

	axes = plot.to_matplotlib().axes[0]

	labels = [label.get_text() for label in axes.get_xticklabels()]
	bar_count = len(axes.patches)
	assert labels == ["Paris", "Lyon"]
	assert bar_count == 4


def test_a_scatter_plot_colors_each_city_and_names_it_in_the_legend() -> None:
	"""
	Check that the points of each city share a color named in the legend.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.ScatterChart(x="surface", y="price", color_by="city")
	plot = ndp.plot_scatter(FLATS, chart)

	axes = plot.to_matplotlib().axes[0]

	legend = axes.get_legend()
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	assert legend_texts == ["Paris", "Lyon", "Pau"]
	assert legend.get_title().get_text() == "city"


def test_a_hidden_legend_and_hidden_grid_lines_are_not_drawn() -> None:
	"""
	Check that LegendPosition.HIDDEN and GridLines.HIDDEN draw nothing.

	.. versionadded:: 0.1.0
	"""
	style = ndp.Style(legend=ndp.LegendPosition.HIDDEN, grid_lines=ndp.GridLines.HIDDEN)
	plot = ndp.plot_line(GRID, ndp.LineChart(), style)

	axes = plot.to_matplotlib().axes[0]

	grid_visible = axes.yaxis.get_gridlines()[0].get_visible()
	assert axes.get_legend() is None
	assert not grid_visible


@pytest.mark.parametrize("image_name", IMAGE_NAMES)
def test_a_plot_is_saved_in_the_format_of_its_extension(tmp_path: Path, image_name: str) -> None:
	"""
	Check that PNG, SVG and PDF images start with the signature of their format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	image_name
		The name of the image.
	"""
	path = tmp_path / image_name
	plot = ndp.plot_bar(PRICES, ndp.BarChart())

	plot.save(path)

	expected_start = IMAGE_STARTS[image_name]
	image_start = path.read_bytes()[: len(expected_start)]
	assert image_start == expected_start


def test_a_plot_sized_in_pixels_gives_an_image_of_that_size(tmp_path: Path) -> None:
	"""
	Check that a Plot of 600 by 300 pixels gives a PNG image of 600 by 300 pixels.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / IMAGE_NAMES[0]
	size = ndp.Size(width=600, height=300, unit=ndp.SizeUnit.PIXEL)
	plot = ndp.plot_line(PRICES, ndp.LineChart(), ndp.Style(size=size))

	plot.save(path)

	image_size = read_png_size(path)
	assert image_size == EXPECTED_PIXEL_SIZE


def test_a_plot_saved_with_more_dots_per_inch_has_more_pixels(tmp_path: Path) -> None:
	"""
	Check that 200 dots per inch give a PNG image of 1280 by 960 pixels for the default size.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / IMAGE_NAMES[0]
	plot = ndp.plot_line(PRICES, ndp.LineChart())

	plot.save(path, ndp.ImageOptions(dpi=200))

	image_size = read_png_size(path)
	assert image_size == EXPECTED_SHARP_SIZE


def test_a_plot_keeps_its_values_when_the_data_changes_afterwards() -> None:
	"""
	Check that a Plot keeps the values of the Table it was made from.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"price": [12.0, 15.5]})
	table = ndp.Table.from_pandas(frame)
	plot = ndp.plot_line(table, ndp.LineChart(y=["price"]))

	frame.loc[0, "price"] = 99.0

	prices = numpy.asarray(plot.to_matplotlib().axes[0].lines[0].get_ydata(), dtype=numpy.float64).tolist()
	assert prices == [12.0, 15.5]


def test_a_plot_rejects_durations_on_its_x_axis() -> None:
	"""
	Check that a duration x column raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([1, 2]).apply(ndp.ToDuration(unit=ndp.DurationUnit.HOUR))
	table = ndp.Table.from_arrays({"wait": durations, "price": ndp.Array.from_list([1.0, 2.0])})

	with pytest.raises(ndp.IncompatibleTypesError):
		ndp.plot_line(table, ndp.LineChart(x="wait", y=["price"]))
