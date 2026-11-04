"""
Unit tests of the griffe extension showing the image of each plot example.

.. versionadded:: 0.1.0
"""

import base64
import doctest

import griffe
import pytest
from figure_images import (
	FigureImages,
	ShownImages,
	insert_plot_images,
	run_examples,
	write_image_line,
	write_svg_image,
)
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values

MODULE_NAME = "plots"
PLOT_LINES = [
	"Prices of the week.",
	"",
	">>> import numdaplot as ndp",
	">>> prices = ndp.Array.from_list([12.0, 15.5])",
	">>> plot = ndp.plot_line(prices, ndp.LineChart())",
	">>> plot.show()",
	">>> print('done')",
	"done",
]
PLOT_TEXT = "\n".join(PLOT_LINES)
IMAGE_START = "![Plot drawn by the example](data:image/svg+xml;base64,"
SHOW_LINE_NUMBER = 5
TEXT_WITHOUT_SHOW = "Prices.\n\n>>> 1 / 0"
BROKEN_PLOT_TEXT = ">>> plot.show()"
SVG_START = "<?xml"
PRINTING_EXAMPLE = ">>> print('hidden')\nhidden\n"
SVG_TEXT = "<svg/>"
PRICES = ndp.Array.from_list([12.0, 15.5])
LAYERS = [ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))]


def test_shown_images_record_each_shown_plot_as_svg() -> None:
	"""
	Check that a recorded Plot becomes an SVG image.

	.. versionadded:: 0.1.0
	"""
	shown_images = ShownImages()

	shown_images.record(LAYERS, ndp.Style())

	image_count = len(shown_images.images)
	assert image_count == 1
	assert shown_images.images[0].startswith(SVG_START)


def test_write_svg_image_writes_an_svg_text() -> None:
	"""
	Check that a figure is written as SVG.

	.. versionadded:: 0.1.0
	"""
	svg_image = write_svg_image(Figure())

	assert svg_image.startswith(SVG_START)


def test_write_image_line_embeds_the_image_in_base64() -> None:
	"""
	Check that the image line holds the image encoded in base64, with the plot-image class.

	.. versionadded:: 0.1.0
	"""
	image_line = write_image_line(SVG_TEXT)

	encoded_part = image_line.removeprefix(IMAGE_START).split(")")[0]
	decoded_text = base64.b64decode(encoded_part).decode()
	assert decoded_text == SVG_TEXT
	assert image_line.endswith("{ .plot-image }")


def test_run_examples_records_the_images_of_each_example() -> None:
	"""
	Check that only the example calling show records an image.

	.. versionadded:: 0.1.0
	"""
	examples = doctest.DocTestParser().get_examples(PLOT_TEXT)

	example_images = run_examples(examples)

	image_counts = [len(images) for images in example_images]
	assert image_counts == [0, 0, 0, 1, 0]


def test_run_examples_hides_the_printed_output(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that the examples print nothing while the documentation builds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed text.
	"""
	examples = doctest.DocTestParser().get_examples(PRINTING_EXAMPLE)

	run_examples(examples)

	captured = capsys.readouterr()
	assert captured.out == ""


def test_run_examples_stops_at_a_broken_example() -> None:
	"""
	Check that an example raising an error stops the build.

	.. versionadded:: 0.1.0
	"""
	examples = doctest.DocTestParser().get_examples(BROKEN_PLOT_TEXT)

	with pytest.raises(NameError):
		run_examples(examples)


def test_insert_plot_images_places_the_image_under_its_example() -> None:
	"""
	Check that the image follows the example calling show, after an empty line, before the next example.

	.. versionadded:: 0.1.0
	"""
	shown_text = insert_plot_images(PLOT_TEXT)

	lines = shown_text.split("\n")
	assert lines[SHOW_LINE_NUMBER] == ">>> plot.show()"
	assert lines[SHOW_LINE_NUMBER + 1] == ""
	assert lines[SHOW_LINE_NUMBER + 2].startswith(IMAGE_START)
	assert lines[SHOW_LINE_NUMBER + 3] == ""
	assert lines[SHOW_LINE_NUMBER + 4] == ">>> print('done')"


def test_insert_plot_images_does_not_run_a_docstring_without_show() -> None:
	"""
	Check that a docstring without show is returned unchanged, its examples not run.

	.. versionadded:: 0.1.0
	"""
	shown_text = insert_plot_images(TEXT_WITHOUT_SHOW)

	assert shown_text == TEXT_WITHOUT_SHOW


def test_figure_images_insert_the_images_of_a_docstring() -> None:
	"""
	Check that the extension rewrites the docstring of a module.

	.. versionadded:: 0.1.0
	"""
	docstring = griffe.Docstring(PLOT_TEXT)
	module = griffe.Module(MODULE_NAME, docstring=docstring)
	extension = FigureImages()

	extension.on_object(obj=module)

	assert IMAGE_START in docstring.value


def test_figure_images_skip_an_object_without_docstring() -> None:
	"""
	Check that an object without docstring is left without docstring.

	.. versionadded:: 0.1.0
	"""
	module = griffe.Module(MODULE_NAME)
	extension = FigureImages()

	extension.on_object(obj=module)

	assert module.docstring is None
