"""
Settings of a PNG image of a Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.files.invalid_resolution_error import InvalidResolutionError

DEFAULT_DPI = 100
MINIMUM_DPI = 1


@dataclass(frozen=True)
class ImageOptions:
	"""
	Settings of a PNG image of a Plot, used by ``Plot.save``.

	The format of an image always comes from the extension of its path. SVG and PDF images are drawn with
	lines and texts, so they have no resolution and refuse these options.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dpi
		The number of pixels per inch of the image, 100 by default. It only changes the sharpness: a Plot of
		6.4 by 4.8 inches gives 640 by 480 pixels at 100, and 1280 by 960 pixels at 200.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidResolutionError
		When ``dpi`` is lower than 1.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> from matplotlib.image import imread
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "prices.png"
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> plot = ndp.Plot.line(prices)
	>>> plot.save(path, ndp.ImageOptions(dpi=200))
	>>> imread(path).shape
	(960, 1280, 4)
	"""

	dpi: int = DEFAULT_DPI

	def __post_init__(self) -> None:
		"""
		Check that the resolution is at least 1 dot per inch.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidResolutionError
			When ``dpi`` is lower than 1.
		"""
		require_field_types(self)

		if self.dpi < MINIMUM_DPI:
			raise InvalidResolutionError(self.dpi)
