"""
Rule keeping the values inside an interval.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.rule import Rule
from numdaplot.rules.rule_values import require_single_value

LOW_SETTING = "Between low"
HIGH_SETTING = "Between high"


# The type parameter has the name of the alias holding the same types: the documentation shows the alias,
# and both bounds must be of one type.
@dataclass(frozen=True)
class Between[OrderedValue: (int, float, str, date, datetime, timedelta)](Rule):
	"""
	Keep the values inside an interval.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		Low bound of the interval, an ``OrderedValue`` such as ``10``, ``"A"`` or ``date(2026, 1, 1)``.
	high
		High bound of the interval, an ``OrderedValue`` such as ``20``, ``"M"`` or ``date(2026, 12, 31)``, greater than
		or equal to ``low`` and of a comparable kind.
	bounds
		Which bounds are part of the interval. Both are included by default.

	Raises
	------
	InvalidSettingTypeError
		When ``low`` or ``high`` is not a single value, such as an Array, a list or None.
	InvalidBoundsError
		When ``low`` is greater than ``high``, or when they cannot be compared,
		such as a number and a text, or a date and a datetime.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([8, 10, 15, 20, 31])
	>>> ages.select(ndp.Between(low=10, high=20))
	Array([10, 15, 20], dtype=INT64)
	>>> ages.select(ndp.Between(low=10, high=20, bounds=ndp.Bounds.EXCLUDED))
	Array([15], dtype=INT64)
	"""

	low: OrderedValue
	high: OrderedValue
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check that both bounds are single values and that the low bound is not greater than the high bound.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When ``low`` or ``high`` is not a single value.
		InvalidBoundsError
			When ``low`` is greater than ``high``, or when they cannot be compared.
		"""
		require_single_value(LOW_SETTING, self.low)
		require_single_value(HIGH_SETTING, self.high)

		try:
			is_reversed = self.low > self.high
		except TypeError as error:
			raise InvalidBoundsError(self.low, self.high) from error

		if is_reversed:
			raise InvalidBoundsError(self.low, self.high)
