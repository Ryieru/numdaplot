"""
Bins of a histogram given by their width.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import timedelta

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.invalid_bin_width_error import InvalidBinWidthError

NO_DURATION = timedelta(0)
LONGEST_DURATION = timedelta(days=1)


@dataclass(frozen=True)
class BinWidth:
	"""
	Bins of a ``HistogramChart`` given by their width, their bounds being multiples of it.

	With a width of 5, the bins are 10 to 15, 15 to 20 and so on, whatever the smallest value. Times of day take
	a duration: with ``timedelta(minutes=30)``, the bins are 08:00 to 08:30, 08:30 to 09:00 and so on.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The width of each bin: a number above 0 for numbers, a duration above 0 and of at most a day for times of
		day.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidBinWidthError
		When the width is 0 or negative, or a duration beyond a day.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 21.0])
	>>> chart = ndp.HistogramChart(bins=ndp.BinWidth(2.5))
	>>> plot = ndp.Plot.histogram(prices, chart)
	>>> plot.show()
	>>> from datetime import time, timedelta
	>>> hours = ndp.Array.from_list([time(8, 10), time(8, 40), time(9, 5), time(17, 50)])
	>>> half_hours = ndp.HistogramChart(bins=ndp.BinWidth(timedelta(minutes=30)))
	>>> ndp.Plot.histogram(hours, half_hours).show()
	"""

	width: float | timedelta

	def __post_init__(self) -> None:
		"""
		Check the width of the bins.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidBinWidthError
			When the width is 0 or negative, or a duration beyond a day.
		"""
		require_field_types(self)

		if isinstance(self.width, timedelta):
			is_outside_day = self.width <= NO_DURATION or self.width > LONGEST_DURATION
			if is_outside_day:
				raise InvalidBinWidthError(self.width)

			return

		if self.width <= 0:
			raise InvalidBinWidthError(self.width)
