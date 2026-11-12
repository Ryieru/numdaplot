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
STYLE = ndp.PlotStyle(title="Sales", x_label="Day", y_label="Euros", legend=ndp.LegendPosition.UPPER_LEFT)
IMAGE_NAMES = ["sales.png", "sales.svg", "sales.pdf"]
IMAGE_STARTS = {"sales.png": b"\x89PNG", "sales.svg": b"<?xml", "sales.pdf": b"%PDF"}
EXPECTED_PIXEL_SIZE = (600, 300)
EXPECTED_SHARP_SIZE = (1280, 960)
PNG_SIZE_START = 16
PNG_SIZE_END = 24
PNG_SIZE_LAYOUT = ">II"
DEFAULT_TEXT_ROTATION = 45.0
CHOSEN_ROTATION = 30.0
NO_ROTATION = 0.0


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
	plot = ndp.Plot.line(SALES, chart, STYLE)

	drawn_figure = plot.to_matplotlib()
	axes = drawn_figure.axes[0]

	legend = axes.get_legend()
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	line_labels = [line.get_label() for line in axes.lines]
	assert line_labels == ["price", "cost"]
	assert legend_texts == ["price", "cost"]
	plot_title = drawn_figure.get_suptitle()
	x_label = axes.get_xlabel()
	y_label = axes.get_ylabel()
	assert (plot_title, x_label, y_label) == ("Sales", "Day", "Euros")


def test_a_line_plot_breaks_its_line_at_a_missing_value() -> None:
	"""
	Check that the missing cost of the second day is not drawn.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.line(SALES, ndp.LineChart(x="day", y=["cost"]))

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
	plot = ndp.Plot.line(GRID, ndp.LineChart())

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
	plot = ndp.Plot.bar(CITY_SALES, chart)

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
	plot = ndp.Plot.scatter(FLATS, chart)

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
	style = ndp.PlotStyle(legend=ndp.LegendPosition.HIDDEN, grid_lines=ndp.GridLines.HIDDEN)
	plot = ndp.Plot.line(GRID, ndp.LineChart(), style)

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
	plot = ndp.Plot.bar(PRICES, ndp.BarChart())

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
	plot = ndp.Plot.line(PRICES, ndp.LineChart(), ndp.PlotStyle(size=size))

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
	plot = ndp.Plot.line(PRICES, ndp.LineChart())

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
	plot = ndp.Plot.line(table, ndp.LineChart(y=["price"]))

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
		ndp.Plot.line(table, ndp.LineChart(x="wait", y=["price"]))


def read_first_x_rotation(plot: ndp.Plot) -> float:
	"""
	Return the angle of the first label of the horizontal axis of a Plot.

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
	first_label = figure.axes[0].get_xticklabels()[0]
	first_rotation = first_label.get_rotation()

	return first_rotation


def build_city_sales() -> ndp.Table:
	"""
	Return a Table with a column of texts and a column of numbers holding a missing value.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The Table.
	"""
	cities = ndp.Array.from_list(["Paris", "Lyon"])
	totals = ndp.Array.from_list([120.0, None])
	city_sales = ndp.Table.from_arrays({"city": cities, "total": totals})

	return city_sales


def test_bar_plot_tilts_its_text_labels_by_default() -> None:
	"""
	Check that the cities below the bars are at 45 degrees.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BarChart(x="city", y=["total"])

	plot = ndp.Plot.bar(build_city_sales(), chart)

	assert read_first_x_rotation(plot) == DEFAULT_TEXT_ROTATION


def test_bar_plot_follows_the_rotation_of_the_style() -> None:
	"""
	Check that the PlotStyle changes the angle of the cities.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BarChart(x="city", y=["total"])
	style = ndp.PlotStyle(x_tick_rotation=CHOSEN_ROTATION)

	plot = ndp.Plot.bar(build_city_sales(), chart, style)

	assert read_first_x_rotation(plot) == CHOSEN_ROTATION


def test_missing_plot_tilts_the_column_names_by_default() -> None:
	"""
	Check the column names below the bars of the missing values.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.missing_by_column(build_city_sales(), ndp.MissingChart())

	assert read_first_x_rotation(plot) == DEFAULT_TEXT_ROTATION


def test_line_plot_keeps_its_numbers_flat_by_default() -> None:
	"""
	Check that numbers on the horizontal axis are not rotated.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list([12.0, 15.5])

	plot = ndp.Plot.line(prices, ndp.LineChart())

	assert read_first_x_rotation(plot) == NO_ROTATION


def test_array_bar_plot_keeps_its_row_numbers_flat_by_default() -> None:
	"""
	Check that the row numbers below the bars of an Array stay numbers.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list([12.0, 15.5])

	plot = ndp.Plot.bar(prices, ndp.BarChart())

	assert read_first_x_rotation(plot) == NO_ROTATION


def test_line_plot_follows_the_y_rotation_of_the_style() -> None:
	"""
	Check that the PlotStyle changes the angle of the values on the vertical axis.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list([12.0, 15.5])
	style = ndp.PlotStyle(y_tick_rotation=CHOSEN_ROTATION)

	plot = ndp.Plot.line(prices, ndp.LineChart(), style)

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_yticklabels()[0].get_rotation() == CHOSEN_ROTATION


def test_horizontal_bar_plot_applies_the_y_rotation_to_its_values() -> None:
	"""
	Check that the ``y`` rotation follows the values of horizontal bars, on the horizontal axis.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BarChart(x="city", y=["total"], orientation=ndp.Orientation.HORIZONTAL)
	style = ndp.PlotStyle(y_tick_rotation=CHOSEN_ROTATION)

	plot = ndp.Plot.bar(build_city_sales(), chart, style)

	assert read_first_x_rotation(plot) == CHOSEN_ROTATION


def test_a_date_axis_does_not_name_a_month_past_the_values() -> None:
	"""
	Check that days of March give March in the corner label, despite a last tick on April 1.

	.. versionadded:: 0.1.0
	"""
	march_table = ndp.Table.from_arrays(
		{
			"day": ndp.Array.from_list([date(2019, 3, 1), date(2019, 3, 31)]),
			"trips": ndp.Array.from_list([10.0, 12.0]),
		}
	)

	plot = ndp.Plot.line(march_table, ndp.LineChart(x="day", y=["trips"]))

	figure = plot.to_matplotlib()
	figure.draw_without_rendering()
	axes = figure.axes[0]
	tick_labels = axes.xaxis.get_ticklabels()
	last_tick_text = tick_labels[-1].get_text()
	corner_label = axes.xaxis.get_offset_text()
	corner_text = corner_label.get_text()
	assert last_tick_text == "Apr"
	assert corner_text == "2019-Mar"


def test_a_long_title_stays_whole_in_the_image() -> None:
	"""
	Check that a long title over a legend placed past the axes stays inside the image.

	.. versionadded:: 0.2.0
	"""
	days = ndp.Array.from_list([1, 2, 3])
	prices = ndp.Array.from_list([12.0, 15.5, 14.0])
	costs = ndp.Array.from_list([8.0, 9.5, 9.0])
	sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	title = "Missing ratio of the diabetics and of the non diabetics, for the ten largest columns"
	style = ndp.PlotStyle(title=title, legend=ndp.LegendPosition.OUTSIDE_RIGHT)
	plot = ndp.Plot.bar(sales, ndp.BarChart(x="day", y=["price", "cost"]), style)

	figure = plot.to_matplotlib()

	figure.draw_without_rendering()
	title_texts = [text for text in figure.texts if text.get_text() != ""]
	title_box = title_texts[0].get_window_extent()
	assert title_box.x0 >= 0
	assert title_box.x1 <= figure.bbox.width
