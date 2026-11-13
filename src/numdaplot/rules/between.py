"""
Rule keeping the values inside an interval.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.arrays.array_data import ArrayData
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.rule import Rule

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array


# The type parameter has the name of the alias holding the same types: the documentation shows the alias,
# and both bounds must be of one type. Two bounds given by Arrays tell no type, so float is the default.
@dataclass(frozen=True)
class Between[OrderedValue: (int, float, str, date, datetime, timedelta, time) = float](Rule):
	"""
	Keep the values inside an interval.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts Arrays as bounds, each value having the bounds at its position.

	Parameters
	----------
	low
		Low bound of the interval, an ``OrderedValue`` such as ``10``, ``"A"`` or ``date(2026, 1, 1)``. Or an Array of
		the shape of the tested values, one value per row for a Table column, giving each value its own low bound.
	high
		High bound of the interval, an ``OrderedValue`` such as ``20``, ``"M"`` or ``date(2026, 12, 31)``, greater than
		or equal to ``low`` and of a comparable kind. Or an Array, as ``low``. A value whose low or high bound is
		missing is not inside the interval.
	bounds
		Which bounds are part of the interval. Both are included by default.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidBoundsError
		When ``low`` is greater than ``high``, or when they cannot be compared,
		such as a number and a text, or a date and a datetime. With bounds given by Arrays, when the rule is used, at
		the first position whose low bound is greater than its high bound.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([8, 10, 15, 20, 31])
	>>> ages.select(ndp.Between(low=10, high=20))
	Array([10, 15, 20], dtype=INT64)
	>>> ages.select(ndp.Between(low=10, high=20, bounds=ndp.Bounds.EXCLUDED))
	Array([15], dtype=INT64)
	>>> temperatures = ndp.Array.from_list([18.0, 25.0, 15.0])
	>>> lows = ndp.Array.from_list([10.0, 10.0, None])
	>>> highs = ndp.Array.from_list([20.0, 20.0, 20.0])
	>>> temperatures.check(ndp.Between(lows, highs))
	Array([ True, False, False], dtype=BOOL)
	"""

	low: OrderedValue | Array
	high: OrderedValue | Array
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check the bounds: the low bound is not greater than the high bound.

		Bounds given by Arrays are checked row by row when the rule is used.

		.. versionadded:: 0.1.0
		.. versionchanged:: 0.2.0
			Leaves the bounds given by Arrays to the check made when the rule is used.

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidBoundsError
			When ``low`` is greater than ``high``, or when they cannot be compared.
		"""
		require_field_types(self)

		has_array_bound = isinstance(self.low, ArrayData) or isinstance(self.high, ArrayData)
		if has_array_bound:
			return

		try:
			is_reversed = self.low > self.high
		except TypeError as error:
			raise InvalidBoundsError(self.low, self.high) from error

		if is_reversed:
			raise InvalidBoundsError(self.low, self.high)
