"""
Normal distribution of decimals.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.errors.invalid_deviation_error import InvalidDeviationError

LOWEST_DEVIATION = 0


@dataclass(frozen=True)
class Normal(Distribution):
	"""
	Decimals drawn around a mean, following a bell curve.

	About 68 % of the values fall within one standard deviation of the mean.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mean
		Center of the bell curve.
	deviation
		Standard deviation, how far the values spread around the mean, at least 0.

	Raises
	------
	InvalidDeviationError
		When ``deviation`` is lower than 0.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> heights = ndp.Array.random(ndp.Normal(mean=170, deviation=10), shape=ndp.Shape((3,)), seed=0)
	>>> heights.apply(ndp.Round())
	Array([171., 169., 176.], dtype=FLOAT64)
	"""

	mean: float
	deviation: float

	def __post_init__(self) -> None:
		"""
		Check that the standard deviation is not negative.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidDeviationError
			When ``deviation`` is lower than 0.
		"""
		if self.deviation < LOWEST_DEVIATION:
			raise InvalidDeviationError(self.deviation)
