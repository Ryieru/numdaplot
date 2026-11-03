"""
A given count of evenly spaced numbers between two bounds.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.rules.bounds import Bounds

LOWEST_COUNT_WITH_BOTH_BOUNDS = 2
LOWEST_COUNT = 1


@dataclass(frozen=True)
class Spacing:
	"""
	A given count of evenly spaced numbers from ``start`` to ``stop``, used by ``Array.from_spacing``.

	``bounds`` tells whether ``start`` and ``stop`` are among the values. With ``start=0``,
	``stop=1`` and ``count=4``:

	- ``INCLUDED`` gives 0, 0.333, 0.667, 1;
	- ``LOW_ONLY`` gives 0, 0.25, 0.5, 0.75;
	- ``HIGH_ONLY`` gives 0.25, 0.5, 0.75, 1;
	- ``EXCLUDED`` gives 0.2, 0.4, 0.6, 0.8.

	.. versionadded:: 0.1.0

	Parameters
	----------
	start
		First bound.
	stop
		Second bound, lower than ``start`` for decreasing values.
	count
		Number of values, at least 2 when both bounds are included, at least 1 otherwise.
	bounds
		Which bounds are among the values. Both are included by default.

	Raises
	------
	InvalidCountError
		When ``count`` is too low for the bounds.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_spacing(ndp.Spacing(start=0, stop=1, count=5))
	Array([0.  , 0.25, 0.5 , 0.75, 1.  ], dtype=FLOAT64)
	>>> ndp.Array.from_spacing(ndp.Spacing(start=0, stop=1, count=4, bounds=ndp.Bounds.EXCLUDED))
	Array([0.2, 0.4, 0.6, 0.8], dtype=FLOAT64)
	"""

	start: float
	stop: float
	count: int
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check that the count is high enough for the bounds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidCountError
			When ``count`` is too low for the bounds.
		"""
		lowest_count = LOWEST_COUNT
		if self.bounds == Bounds.INCLUDED:
			lowest_count = LOWEST_COUNT_WITH_BOTH_BOUNDS

		if self.count < lowest_count:
			raise InvalidCountError(self.count, lowest_count)
