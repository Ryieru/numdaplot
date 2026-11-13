"""
Unit tests of the image files of a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path

import pytest
from matplotlib.figure import Figure, FigureBase

from numdaplot.errors.files.file_exists_error import FileExistsError
from numdaplot.errors.files.unsupported_image_format_error import UnsupportedImageFormatError
from numdaplot.errors.settings.refused_setting_error import RefusedSettingError
from numdaplot.files.conflict import Conflict
from numdaplot.plots.drawing.plot_drawing import FigureDrawing
from numdaplot.plots.output.image_saving import choose_resolution, find_image_format, save_figure, write_image
from numdaplot.plots.style.image_options import ImageOptions

PNG_PATH = Path("sales.png")
SVG_PATH = Path("sales.svg")
PDF_PATH = Path("sales.PDF")
REJECTED_PATHS = [Path("sales.jpg"), Path("sales")]
HIGH_RESOLUTION = 200
DEFAULT_RESOLUTION = 100
PNG_SIGNATURE = b"\x89PNG"
SMALL_INCHES = (3.0, 2.0)
OLD_CONTENT = "old"


def draw_title(target: FigureBase) -> None:
	"""
	Draw a title on a matplotlib figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target
		The figure drawn on.
	"""
	target.suptitle("Sales")


TITLE_DRAWING = FigureDrawing(draw_title, SMALL_INCHES)


@pytest.mark.parametrize(
	("path", "expected_format"),
	[(PNG_PATH, "png"), (SVG_PATH, "svg"), (PDF_PATH, "pdf")],
)
def test_find_image_format_reads_the_extension_in_any_case(path: Path, expected_format: str) -> None:
	"""
	Check that each supported extension names its format, in lowercase or uppercase.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		A path with a supported extension.
	expected_format
		The matplotlib name of its format.
	"""
	image_format = find_image_format(path)

	assert image_format == expected_format


@pytest.mark.parametrize("path", REJECTED_PATHS)
def test_find_image_format_rejects_another_extension_or_none(path: Path) -> None:
	"""
	Check that a JPEG path and a path without extension raise UnsupportedImageFormatError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		A rejected path.
	"""
	with pytest.raises(UnsupportedImageFormatError):
		find_image_format(path)


def test_choose_resolution_defaults_to_100() -> None:
	"""
	Check the resolution without options.

	.. versionadded:: 0.1.0
	"""
	resolution = choose_resolution(SVG_PATH, None)

	assert resolution == DEFAULT_RESOLUTION


def test_choose_resolution_reads_the_options_of_a_png_image() -> None:
	"""
	Check that a PNG image takes the resolution of its options.

	.. versionadded:: 0.1.0
	"""
	resolution = choose_resolution(PNG_PATH, ImageOptions(dpi=HIGH_RESOLUTION))

	assert resolution == HIGH_RESOLUTION


def test_choose_resolution_refuses_options_for_a_pdf_image() -> None:
	"""
	Check that options for a PDF image raise RefusedSettingError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedSettingError):
		choose_resolution(PDF_PATH, ImageOptions())


def test_save_figure_writes_the_image_in_its_format(tmp_path: Path) -> None:
	"""
	Check that a PNG image is written.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / PNG_PATH

	save_figure(Figure(), path, "png", DEFAULT_RESOLUTION)

	image_start = path.read_bytes()[:4]
	assert image_start == PNG_SIGNATURE


def test_write_image_saves_the_drawing_in_the_format_of_the_extension(tmp_path: Path) -> None:
	"""
	Check that a drawing saved as .png is a PNG image.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / PNG_PATH

	write_image(TITLE_DRAWING, image_path, None, Conflict.ERROR)

	image_start = image_path.read_bytes()[:4]
	assert image_start == PNG_SIGNATURE


def test_write_image_refuses_to_overwrite_with_error(tmp_path: Path) -> None:
	"""
	Check that an existing file raises FileExistsError and keeps its content.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / SVG_PATH
	image_path.write_text(OLD_CONTENT)

	with pytest.raises(FileExistsError):
		write_image(TITLE_DRAWING, image_path, None, Conflict.ERROR)

	assert image_path.read_text() == OLD_CONTENT


def test_write_image_replaces_a_file_with_replace(tmp_path: Path) -> None:
	"""
	Check that REPLACE overwrites an existing file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / SVG_PATH
	image_path.write_text(OLD_CONTENT)

	write_image(TITLE_DRAWING, image_path, None, Conflict.REPLACE)

	assert image_path.read_text().startswith("<?xml")
