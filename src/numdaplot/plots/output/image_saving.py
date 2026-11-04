"""
Image files of a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path

from matplotlib.figure import Figure

from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.errors.unsupported_image_format_error import UnsupportedImageFormatError
from numdaplot.plots.style.image_options import DEFAULT_DPI, ImageOptions

IMAGE_FORMATS = {".png": "png", ".svg": "svg", ".pdf": "pdf"}
RESOLUTION_EXTENSION = ".png"
OPTIONS_NAME = "ImageOptions"
IMAGE_OWNER = "A {extension} image"


def find_image_format(path: Path) -> str:
	"""
	Return the image format named by the extension of a path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the image, ending with ``.png``, ``.svg`` or ``.pdf`` in lowercase or uppercase.

	Returns
	-------
	str
		The matplotlib name of the format: ``png``, ``svg`` or ``pdf``.

	Raises
	------
	UnsupportedImageFormatError
		When the path has another extension or none.

	Examples
	--------
	>>> from pathlib import Path
	>>> from numdaplot.plots.output.image_saving import find_image_format
	>>> find_image_format(Path("sales.SVG"))
	'svg'
	"""
	extension = path.suffix.lower()
	if extension not in IMAGE_FORMATS:
		raise UnsupportedImageFormatError(path.suffix)

	image_format = IMAGE_FORMATS[extension]

	return image_format


def choose_resolution(path: Path, options: ImageOptions | None) -> int:
	"""
	Return the number of dots per inch an image is saved with.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the image, with a supported extension.
	options
		The settings of a PNG image, or None.

	Returns
	-------
	int
		The resolution of the options, 100 without them.

	Raises
	------
	RefusedSettingError
		When options are given for an SVG or PDF image, which has no resolution.

	Examples
	--------
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.output.image_saving import choose_resolution
	>>> try:
	... 	choose_resolution(Path("sales.svg"), ndp.ImageOptions(dpi=200))
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	A .svg image does not accept ImageOptions.
	"""
	if options is None:
		return DEFAULT_DPI

	extension = path.suffix.lower()
	if extension != RESOLUTION_EXTENSION:
		image_name = IMAGE_OWNER.format(extension=extension)
		raise RefusedSettingError(OPTIONS_NAME, image_name)

	return options.dpi


def save_figure(figure: Figure, path: Path, image_format: str, resolution: int) -> None:
	"""
	Save a matplotlib figure as an image.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		The figure to save.
	path
		The path of the image.
	image_format
		The matplotlib name of the format, as ``find_image_format`` gives it.
	resolution
		The number of dots per inch, as ``choose_resolution`` gives it.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.output.image_saving import save_figure
	>>> path = Path(tempfile.mkdtemp()) / "empty.pdf"
	>>> save_figure(Figure(), path, "pdf", 100)
	>>> path.read_bytes()[:4]
	b'%PDF'
	"""
	figure.savefig(path, format=image_format, dpi=resolution)
