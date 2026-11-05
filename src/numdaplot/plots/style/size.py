"""
Width and height of a Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_size_error import InvalidSizeError
from numdaplot.plots.style.size_unit import SizeUnit

DEFAULT_WIDTH = 6.4
DEFAULT_HEIGHT = 4.8


@dataclass(frozen=True)
class Size:
	"""
	Width and height of a Plot, used by ``PlotStyle``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The width, 6.4 inches by default.
	height
		The height, 4.8 inches by default.
	unit
		The unit of the width and the height, ``SizeUnit.INCH`` by default.

	Raises
	------
	InvalidSizeError
		When the width or the height is zero or negative.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.PlotStyle(size=ndp.Size(width=6, height=2.5))
	>>> plot = ndp.plot_line(prices, style=style)
	>>> plot.show()
	"""

	width: float = DEFAULT_WIDTH
	height: float = DEFAULT_HEIGHT
	unit: SizeUnit = SizeUnit.INCH

	def __post_init__(self) -> None:
		"""
		Check that the width and the height are positive.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSizeError
			When the width or the height is zero or negative.
		"""
		is_positive = self.width > 0 and self.height > 0
		if not is_positive:
			raise InvalidSizeError(self.width, self.height)
