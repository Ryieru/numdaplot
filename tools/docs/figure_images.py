"""
Griffe extension showing the image of each plot example under its code in the documentation site.

The examples of the plots end with ``plot.show()`` or ``figure.show()``. When ``mkdocs`` reads a docstring
holding such an example, this extension runs its examples in order, as doctest does, while ``Plot.show`` and
``Figure.show`` draw an SVG image instead of opening a window. Each image is written in the docstring right
under the example that showed it, so the documentation shows exactly what the code draws.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of savefig untyped.
# pyright: reportUnknownMemberType=false

import base64
import contextlib
import doctest
import io
from typing import Any
from unittest import mock

import griffe
from matplotlib.figure import Figure

from numdaplot.plots.drawing.plot_drawing import FigureDrawing, build_figure

SHOW_CALL = ".show()"
SHOWN_FUNCTION_PATHS = ("numdaplot.plots.plot_output.show_drawing", "numdaplot.plots.figure.figure.show_drawing")
SVG_FORMAT = "svg"
TEXT_ENCODING = "utf-8"
EXAMPLE_FILE_NAME = "<plot example>"
SINGLE_STATEMENT_MODE = "single"
IMAGE_LINE = "![Plot drawn by the example](data:image/svg+xml;base64,{encoded_image}){{ .plot-image }}"
LINE_SEPARATOR = "\n"


class ShownImages:
	"""
	The SVG images of the Plots and Figures shown while examples run.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from figure_images import ShownImages
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing
	>>> shown_images = ShownImages()
	>>> shown_images.record(FigureDrawing(lambda target: target.suptitle("Sales"), (3.0, 2.0)))
	>>> shown_images.images[0].startswith("<?xml")
	True
	"""

	def __init__(self) -> None:
		"""
		Start without image.

		.. versionadded:: 0.1.0
		"""
		self.images = list[str]()

	def record(self, drawing: FigureDrawing) -> None:
		"""
		Draw a shown Plot or Figure as an SVG image and keep it, in place of the display of ``show``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		drawing
			What the Plot or the Figure draws, and its size.
		"""
		figure = build_figure(drawing)
		svg_image = write_svg_image(figure)
		self.images.append(svg_image)


def write_svg_image(figure: Figure) -> str:
	"""
	Return a matplotlib figure written as an SVG image.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		The figure to write.

	Returns
	-------
	str
		The SVG text.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from figure_images import write_svg_image
	>>> "<svg" in write_svg_image(Figure())
	True
	"""
	image_buffer = io.StringIO()
	figure.savefig(image_buffer, format=SVG_FORMAT)
	svg_image = image_buffer.getvalue()

	return svg_image


def write_image_line(svg_image: str) -> str:
	"""
	Return the Markdown line showing an SVG image, embedded in the page.

	.. versionadded:: 0.1.0

	Parameters
	----------
	svg_image
		The SVG text.

	Returns
	-------
	str
		A Markdown image whose source is the image itself, with the ``plot-image`` class.

	Examples
	--------
	>>> from figure_images import write_image_line
	>>> write_image_line("<svg/>")
	'![Plot drawn by the example](data:image/svg+xml;base64,PHN2Zy8+){ .plot-image }'
	"""
	image_bytes = svg_image.encode(TEXT_ENCODING)
	encoded_bytes = base64.b64encode(image_bytes)
	encoded_image = encoded_bytes.decode(TEXT_ENCODING)
	image_line = IMAGE_LINE.format(encoded_image=encoded_image)

	return image_line


def run_examples(examples: list[doctest.Example]) -> list[list[str]]:
	r"""
	Run doctest examples in order, in a shared namespace, and return the images each one showed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	examples
		The examples of one docstring.

	Returns
	-------
	list[list[str]]
		For each example, the SVG images of the Plots it showed, in order.

	Raises
	------
	Exception
		Any error an example raises, so a broken example stops the documentation build.

	Examples
	--------
	>>> import doctest
	>>> from figure_images import run_examples
	>>> examples = doctest.DocTestParser().get_examples(">>> total = 1 + 2\n>>> total\n3\n")
	>>> run_examples(examples)
	[[], []]
	"""
	shown_images = ShownImages()
	namespace = dict[str, Any]()
	example_images = list[list[str]]()
	printed_output = io.StringIO()

	with contextlib.ExitStack() as patches:
		for function_path in SHOWN_FUNCTION_PATHS:
			function_patch = mock.patch(function_path, shown_images.record)
			patches.enter_context(function_patch)

		printed_redirection = contextlib.redirect_stdout(printed_output)
		patches.enter_context(printed_redirection)

		for example in examples:
			image_count = len(shown_images.images)
			code = compile(example.source, EXAMPLE_FILE_NAME, SINGLE_STATEMENT_MODE)
			exec(code, namespace)
			new_images = shown_images.images[image_count:]
			example_images.append(new_images)

	return example_images


def insert_plot_images(docstring_text: str) -> str:
	r"""
	Return a docstring with the image of each shown Plot right under the example showing it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring_text
		The text of a docstring.

	Returns
	-------
	str
		The same text, each example calling ``.show()`` followed by an empty line and its image lines.
		A docstring without ``.show()`` is returned unchanged, without running its examples.

	Examples
	--------
	>>> from figure_images import insert_plot_images
	>>> text = ">>> import numdaplot as ndp\n>>> ndp.Plot.line(ndp.Array.from_list([1.0]), ndp.LineChart()).show()"
	>>> insert_plot_images(text).splitlines()[3].startswith("![Plot drawn by the example]")
	True
	"""
	if SHOW_CALL not in docstring_text:
		return docstring_text

	parser = doctest.DocTestParser()
	examples = parser.get_examples(docstring_text)
	example_images = run_examples(examples)
	lines = docstring_text.split(LINE_SEPARATOR)
	shown_examples = zip(examples, example_images, strict=True)
	reversed_examples = reversed(list(shown_examples))

	for example, images in reversed_examples:
		if images == []:
			continue

		source_line_count = example.source.count(LINE_SEPARATOR)
		output_line_count = example.want.count(LINE_SEPARATOR)
		end_line = example.lineno + source_line_count + output_line_count
		image_lines = [write_image_line(image) for image in images]
		lines[end_line:end_line] = ["", *image_lines, ""]

	shown_text = LINE_SEPARATOR.join(lines)

	return shown_text


class FigureImages(griffe.Extension):
	"""
	Griffe extension showing the image of each plot example under its code.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler, before the
	extensions changing the indentation and the links of the docstrings.

	.. versionadded:: 0.1.0
	"""

	def on_object(self, *, obj: griffe.Object, **kwargs: Any) -> None:
		"""
		Insert the images of the plot examples of the docstring of an object, if it has one.

		.. versionadded:: 0.1.0

		Parameters
		----------
		obj
			A module, class, function or attribute read by griffe.
		**kwargs
			The other arguments griffe gives to its extensions, unused.
		"""
		if obj.docstring is None:
			return

		shown_text = insert_plot_images(obj.docstring.value)
		obj.docstring.value = shown_text
