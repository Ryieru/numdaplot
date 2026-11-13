"""
Bins of a histogram given by their number.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.settings.invalid_count_error import InvalidCountError

MINIMUM_BIN_COUNT = 1


@dataclass(frozen=True)
class BinCount:
	"""
	Bins of a ``HistogramChart`` given by their number, of the same width from the smallest to the largest value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	count
		The number of bins, at least 1.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidCountError
		When the count is lower than 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 15.0])
	>>> chart = ndp.HistogramChart(bins=ndp.BinCount(4))
	>>> plot = ndp.Plot.histogram(prices, chart)
	>>> plot.show()
	"""

	count: int

	def __post_init__(self) -> None:
		"""
		Check the number of bins.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidCountError
			When the count is lower than 1.
		"""
		require_field_types(self)

		if self.count < MINIMUM_BIN_COUNT:
			raise InvalidCountError(self.count, MINIMUM_BIN_COUNT)
