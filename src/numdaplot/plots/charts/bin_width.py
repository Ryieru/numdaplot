"""
Bins of a histogram given by their width.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_bin_width_error import InvalidBinWidthError
from numdaplot.settings.field_types import require_field_types


@dataclass(frozen=True)
class BinWidth:
	"""
	Bins of a ``HistogramChart`` given by their width, their bounds being multiples of it.

	With a width of 5, the bins are 10 to 15, 15 to 20 and so on, whatever the smallest value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The width of each bin, above 0.

	Raises
	------
	InvalidSettingTypeError
		When a setting is not of the type its annotation names.
	InvalidBinWidthError
		When the width is 0 or negative.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 21.0])
	>>> chart = ndp.HistogramChart(bins=ndp.BinWidth(2.5))
	>>> plot = ndp.plot_histogram(prices, chart)
	>>> plot.show()
	"""

	width: float

	def __post_init__(self) -> None:
		"""
		Check the width of the bins.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When a setting is not of the type its annotation names.
		InvalidBinWidthError
			When the width is 0 or negative.
		"""
		require_field_types(self)

		if self.width <= 0:
			raise InvalidBinWidthError(self.width)
