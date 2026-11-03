"""
Rule keeping the values inside an interval.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.rule import Rule


@dataclass(frozen=True)
class Between[BoundValue: (int, float, str, date, datetime, timedelta)](Rule):
	"""
	Keep the values inside an interval.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		Low bound of the interval.
	high
		High bound of the interval, greater than or equal to ``low`` and of a comparable kind.
	bounds
		Which bounds are part of the interval. Both are included by default.

	Raises
	------
	InvalidBoundsError
		When ``low`` is greater than ``high``, or when they cannot be compared,
		such as a number and a text, or a date and a datetime.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Between(low=10, high=20)
	Between(low=10, high=20, bounds=<Bounds.INCLUDED: 1>)
	"""

	low: BoundValue
	high: BoundValue
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check that the low bound is not greater than the high bound.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidBoundsError
			When ``low`` is greater than ``high``, or when they cannot be compared.
		"""
		try:
			is_reversed = self.low > self.high
		except TypeError as error:
			raise InvalidBoundsError(self.low, self.high) from error

		if is_reversed:
			raise InvalidBoundsError(self.low, self.high)
