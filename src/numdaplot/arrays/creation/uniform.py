"""
Uniform distribution of decimals.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError


@dataclass(frozen=True)
class Uniform(Distribution):
	"""
	Decimals drawn with the same chance anywhere from ``low`` to ``high``.

	``high`` itself is never drawn, as in numpy. Use ``RandomIntegers`` for whole numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		Lowest value that can be drawn.
	high
		Value that every drawn value stays below, greater than or equal to ``low``.

	Raises
	------
	InvalidBoundsError
		When ``low`` is greater than ``high``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.random(ndp.Uniform(low=0, high=1), shape=ndp.Shape((3,)), seed=0)
	Array([0.63696169, 0.26978671, 0.04097352], dtype=FLOAT64)
	"""

	low: float
	high: float

	def __post_init__(self) -> None:
		"""
		Check that the low bound is not greater than the high bound.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidBoundsError
			When ``low`` is greater than ``high``.
		"""
		if self.low > self.high:
			raise InvalidBoundsError(self.low, self.high)
