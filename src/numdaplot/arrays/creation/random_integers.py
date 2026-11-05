"""
Uniform distribution of whole numbers.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.rules.bounds import HIGH_INCLUDED_BOUNDS, LOW_INCLUDED_BOUNDS, Bounds
from numdaplot.settings.field_types import require_field_types


@dataclass(frozen=True)
class RandomIntegers(Distribution):
	"""
	Whole numbers drawn with the same chance from ``low`` to ``high``.

	Both bounds can be drawn by default: ``RandomIntegers(low=1, high=6)`` rolls a die.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		Low bound.
	high
		High bound.
	bounds
		Which bounds can be drawn. Both are included by default.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidBoundsError
		When no whole number lies between the bounds, such as ``low`` greater than ``high``,
		or ``low=3, high=4`` with both bounds excluded.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> dice = ndp.RandomIntegers(low=1, high=6)
	>>> ndp.Array.random(dice, shape=ndp.Shape([5]), seed=0)
	Array([6, 4, 4, 2, 2], dtype=INT64)
	"""

	low: int
	high: int
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check that at least one whole number can be drawn.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidBoundsError
			When no whole number lies between the bounds.
		"""
		require_field_types(self)

		lowest_value, value_limit = find_drawn_interval(self)
		if lowest_value >= value_limit:
			raise InvalidBoundsError(self.low, self.high)


def find_drawn_interval(distribution: RandomIntegers) -> tuple[int, int]:
	"""
	Return the lowest value that can be drawn and the value that every drawn value stays below.

	.. versionadded:: 0.1.0

	Parameters
	----------
	distribution
		The distribution whose bounds are read.

	Returns
	-------
	tuple[int, int]
		The lowest drawable value, and the high limit excluded from the draw, as numpy expects them.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.random_integers import find_drawn_interval
	>>> find_drawn_interval(ndp.RandomIntegers(low=1, high=6))
	(1, 7)
	"""
	lowest_value = distribution.low
	if distribution.bounds not in LOW_INCLUDED_BOUNDS:
		lowest_value += 1

	value_limit = distribution.high
	if distribution.bounds in HIGH_INCLUDED_BOUNDS:
		value_limit += 1

	return lowest_value, value_limit
