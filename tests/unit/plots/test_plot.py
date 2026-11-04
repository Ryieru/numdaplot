"""
Unit tests of Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path
from typing import Any

import pytest
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots import plot as plot_module
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
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
SHOW_FUNCTION_NAME = "show_plot"
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
	plot = Plot([LAYER], STYLE)

	return plot


def test_plot_keeps_its_own_copy_of_the_layers() -> None:
	"""
	Check that changing the given list changes nothing in the Plot.

	.. versionadded:: 0.1.0
	"""
	layers = [LAYER]
	plot = Plot(layers, STYLE)

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
	monkeypatch.setattr(plot_module, SAVE_FUNCTION_NAME, save_recorder)

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


def test_show_hands_the_charts_and_the_style_to_the_display(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that show displays the layers with the style of the Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the display with a fake.
	"""
	shown_calls = list[tuple[Any, Any]]()

	def record_show(layers: list[ChartLayer], style: ndp.Style) -> None:
		"""
		Keep the shown layers and style.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layers
			The shown layers.
		style
			The shown style.
		"""
		shown_calls.append((layers, style))

	monkeypatch.setattr(plot_module, SHOW_FUNCTION_NAME, record_show)

	build_plot().show()

	shown_layers, shown_style = shown_calls[0]
	assert shown_layers == [LAYER]
	assert shown_style is STYLE
