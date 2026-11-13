"""
Normal distribution of decimals.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.errors.distributions.invalid_deviation_error import InvalidDeviationError

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
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidDeviationError
		When ``deviation`` is lower than 0.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.random(ndp.Normal(mean=170, deviation=10), shape=ndp.Shape([3]), seed=0)
	Array([171.25730221, 168.67895137, 176.4042265 ], dtype=FLOAT64)
	"""

	mean: float
	deviation: float

	def __post_init__(self) -> None:
		"""
		Check that the standard deviation is not negative.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidDeviationError
			When ``deviation`` is lower than 0.
		"""
		require_field_types(self)

		if self.deviation < LOWEST_DEVIATION:
			raise InvalidDeviationError(self.deviation)
