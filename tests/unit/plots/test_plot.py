"""
Unit tests of Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false
# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from pathlib import Path

import numpy
import pytest
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots import plot as plot_module
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.drawing.plot_drawing import FigureDrawing, build_figure
from numdaplot.plots.output import image_saving
from numdaplot.plots.plot import Plot

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
LAYER = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
STYLE = ndp.Style(title="Prices")
PNG_NAME = "prices.png"
SVG_NAME = "prices.svg"
DEFAULT_RESOLUTION = 100
SHARP_RESOLUTION = 200
SAVE_FUNCTION_NAME = "save_figure"
SHARP_OPTIONS = ndp.ImageOptions(dpi=200)
SHOW_FUNCTION_NAME = "show_drawing"
DEFAULT_INCHES = (6.4, 4.8)
MONTHS = ndp.Array.from_list(["Jan", "Feb", "Mar"])
SHOP = ndp.Table.from_arrays(
	{
		"month": MONTHS,
		"sales": ndp.Array.from_list([120.0, 150.0, 90.0]),
		"price": ndp.Array.from_list([12.5, 11.0, 14.0]),
	}
)
SALES_BARS = ndp.BarChart(x="month", y=["sales"])
PRICE_LINE = ndp.LineChart(x="month", y=["price"])
PRICE_POINTS = ndp.ScatterChart(x="month", y="price")
BOX_PLOT = ndp.plot_box(PRICES, ndp.BoxChart())
OLD_CONTENT = "old"


def build_plot() -> Plot:
	"""
	Return a Plot of three prices.

	.. versionadded:: 0.1.0

	Returns
	-------
	Plot
		A line Plot titled Prices.
	"""
	plot = Plot._create([LAYER], STYLE)

	return plot


def test_plot_refuses_its_constructor() -> None:
	"""
	Check that creating a Plot by its constructor raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedOperationError):
		Plot()


def test_plot_keeps_its_own_copy_of_the_layers() -> None:
	"""
	Check that changing the given list changes nothing in the Plot.

	.. versionadded:: 0.1.0
	"""
	layers = [LAYER]
	plot = Plot._create(layers, STYLE)

	layers.clear()

	figure = plot.to_matplotlib()
	line_count = len(figure.axes[0].lines)
	assert line_count == 1


def test_to_matplotlib_gives_a_new_figure_each_time() -> None:
	"""
	Check that changing a returned figure never changes the Plot.

	.. versionadded:: 0.1.0
	"""
	plot = build_plot()
	first_figure = plot.to_matplotlib()
	first_figure.axes[0].set_title(OLD_CONTENT)

	second_figure = plot.to_matplotlib()

	assert second_figure.axes[0].get_title() == "Prices"


class SaveRecorder:
	"""
	Fake image saving keeping the format and the resolution of each saved image.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without saved image.

		.. versionadded:: 0.1.0
		"""
		self.saved_images = list[tuple[str, int]]()

	def __call__(self, figure: Figure, path: Path, image_format: str, resolution: int) -> None:
		"""
		Keep the format and the resolution of a saved image.

		.. versionadded:: 0.1.0

		Parameters
		----------
		figure
			The saved figure, ignored.
		path
			The path of the image, ignored.
		image_format
			The format of the image.
		resolution
			The number of dots per inch.
		"""
		self.saved_images.append((image_format, resolution))


@pytest.mark.parametrize(
	("options", "expected_resolution"),
	[(None, DEFAULT_RESOLUTION), (SHARP_OPTIONS, SHARP_RESOLUTION)],
)
def test_save_saves_a_png_image_at_the_resolution_of_its_options(
	monkeypatch: pytest.MonkeyPatch, options: ndp.ImageOptions | None, expected_resolution: int
) -> None:
	"""
	Check that a PNG image is saved at 100 dots per inch, or at the resolution of its options.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the image saving with a fake.
	options
		The options given, or None.
	expected_resolution
		The resolution of the saved image.
	"""
	save_recorder = SaveRecorder()
	monkeypatch.setattr(image_saving, SAVE_FUNCTION_NAME, save_recorder)

	build_plot().save(PNG_NAME, options)

	assert save_recorder.saved_images == [("png", expected_resolution)]


def test_save_refuses_to_overwrite_a_file_by_default(tmp_path: Path) -> None:
	"""
	Check that an existing file raises FileExistsError and keeps its content.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / SVG_NAME
	path.write_text(OLD_CONTENT)

	with pytest.raises(ndp.FileExistsError):
		build_plot().save(path)

	assert path.read_text() == OLD_CONTENT


def test_save_replaces_a_file_when_asked(tmp_path: Path) -> None:
	"""
	Check that Conflict.REPLACE overwrites an existing file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / SVG_NAME
	path.write_text(OLD_CONTENT)

	build_plot().save(path, on_conflict=ndp.Conflict.REPLACE)

	assert path.read_text() != OLD_CONTENT


def test_save_checks_the_extension_before_the_existing_file(tmp_path: Path) -> None:
	"""
	Check that a wrong extension is reported even when the file exists.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / "prices.jpg"
	path.write_text(OLD_CONTENT)

	with pytest.raises(ndp.UnsupportedImageFormatError):
		build_plot().save(path)


def test_show_hands_the_drawing_of_the_plot_to_the_display(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that show displays what the Plot draws, at the size of its style.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the display with a fake.
	"""
	shown_drawings = list[FigureDrawing]()
	monkeypatch.setattr(plot_module, SHOW_FUNCTION_NAME, shown_drawings.append)

	build_plot().show()

	shown_drawing = shown_drawings[0]
	shown_figure = build_figure(shown_drawing)
	assert shown_drawing.size_inches == DEFAULT_INCHES
	assert shown_figure.axes[0].get_title() == "Prices"


def build_sales_plot() -> Plot:
	"""
	Return a Plot of the sales of each month as bars.

	.. versionadded:: 0.1.0

	Returns
	-------
	Plot
		A bar Plot of three months.
	"""
	plot = ndp.plot_bar(SHOP, SALES_BARS)

	return plot


def test_add_line_draws_a_line_over_the_bars_and_leaves_the_plot_unchanged() -> None:
	"""
	Check that the new Plot has the bars and the line, and the first one only the bars.

	.. versionadded:: 0.1.0
	"""
	plot = build_sales_plot()

	both = plot.add_line(SHOP, PRICE_LINE)

	plot_axes = plot.to_matplotlib().axes[0]
	both_axes = both.to_matplotlib().axes[0]
	assert len(plot_axes.lines) == 0
	assert len(both_axes.lines) == 1
	assert len(both_axes.patches) == 3


def test_add_line_on_the_right_draws_a_second_axis() -> None:
	"""
	Check that a line on the right gets axes of its own, labeled with its column.

	.. versionadded:: 0.1.0
	"""
	plot = build_sales_plot()

	both = plot.add_line(SHOP, PRICE_LINE, axis=ndp.ValueAxis.RIGHT)

	figure = both.to_matplotlib()
	axes_count = len(figure.axes)
	assert axes_count == 2
	assert figure.axes[1].get_ylabel() == "price"


def test_add_bar_rejects_horizontal_bars() -> None:
	"""
	Check that added bars must be vertical.

	.. versionadded:: 0.1.0
	"""
	horizontal_bars = ndp.BarChart(x="month", y=["price"], orientation=ndp.Orientation.HORIZONTAL)

	with pytest.raises(ndp.RefusedSettingError):
		build_sales_plot().add_bar(SHOP, horizontal_bars)


def test_add_bar_draws_bars_over_the_bars() -> None:
	"""
	Check that added bars are drawn after the first ones.

	.. versionadded:: 0.1.0
	"""
	both = build_sales_plot().add_bar(SHOP, ndp.BarChart(x="month", y=["price"]))

	both_axes = both.to_matplotlib().axes[0]
	assert len(both_axes.patches) == 6


def test_add_scatter_draws_points_over_the_bars() -> None:
	"""
	Check that added points are drawn on the labels of the bars.

	.. versionadded:: 0.1.0
	"""
	both = build_sales_plot().add_scatter(SHOP, PRICE_POINTS)

	both_axes = both.to_matplotlib().axes[0]
	point_offsets = both_axes.collections[0].get_offsets()
	offsets = numpy.asarray(point_offsets).tolist()
	assert offsets == [[0.0, 12.5], [1.0, 11.0], [2.0, 14.0]]


def test_add_line_rejects_a_plot_of_boxes() -> None:
	"""
	Check that a Plot of boxes refuses added charts.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError, match="BoxChart"):
		BOX_PLOT.add_line(PRICES, ndp.LineChart())


def test_add_line_rejects_numbers_over_texts() -> None:
	"""
	Check that a line of numbers cannot be added over bars of texts.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.IncompatibleChartsError):
		build_sales_plot().add_line(PRICES, ndp.LineChart())


def test_add_line_keeps_the_style_of_the_plot() -> None:
	"""
	Check that the new Plot has the title of the first one.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_bar(SHOP, SALES_BARS, ndp.Style(title="Shop"))

	both = plot.add_line(SHOP, PRICE_LINE)

	both_axes = both.to_matplotlib().axes[0]
	assert both_axes.get_title() == "Shop"


def test_add_line_without_chart_draws_the_lines_of_an_array() -> None:
	"""
	Check that add_line without chart draws a line over the bars.

	.. versionadded:: 0.1.0
	"""
	bar_plot = ndp.plot_bar(PRICES)

	both = bar_plot.add_line(PRICES)

	figure = both.to_matplotlib()
	line_count = len(figure.axes[0].lines)
	assert line_count == 1
