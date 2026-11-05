"""
Values drawn from a random distribution.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.arrays.creation.normal import Normal
from numdaplot.arrays.creation.random_integers import RandomIntegers, find_drawn_interval
from numdaplot.arrays.creation.uniform import Uniform
from numdaplot.arrays.shape import Shape
from numdaplot.errors.invalid_seed_error import InvalidSeedError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.settings.setting_types import require_object_not_class

LOWEST_SEED = 0
UNKNOWN_DISTRIBUTION_OPERATION = "The distribution {distribution_name}"
UNKNOWN_DISTRIBUTION_ALTERNATIVE = "a distribution of numdaplot"
DISTRIBUTION_SETTING = "random distribution"
DISTRIBUTION_EXPECTED = "a distribution such as ndp.Uniform(low=0, high=1)"


def draw_random_values(distribution: Distribution, shape: Shape, seed: int | None) -> NDArray[Any]:
	"""
	Return values drawn from a random distribution.

	.. versionadded:: 0.1.0

	Parameters
	----------
	distribution
		The law followed by the values.
	shape
		The shape of the result.
	seed
		A number giving the same values at each call, at least 0. Different values at each call when ``None``.

	Returns
	-------
	NDArray
		Decimals for ``Uniform`` and ``Normal``, integers for ``RandomIntegers``.

	Raises
	------
	InvalidSettingTypeError
		When ``distribution`` is a class, written without its parentheses.
	InvalidSeedError
		When ``seed`` is lower than 0.
	RefusedOperationError
		When the distribution is not a distribution of numdaplot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.random_values import draw_random_values
	>>> dice = ndp.RandomIntegers(low=1, high=6)
	>>> draw_random_values(dice, ndp.Shape((4,)), 0)
	array([6, 4, 4, 2])
	"""
	require_object_not_class(DISTRIBUTION_SETTING, DISTRIBUTION_EXPECTED, distribution)

	if seed is not None:
		require_valid_seed(seed)

	generator = numpy.random.default_rng(seed)
	match distribution:
		case Uniform():
			values = generator.uniform(distribution.low, distribution.high, shape.dimensions)
		case Normal():
			values = generator.normal(distribution.mean, distribution.deviation, shape.dimensions)
		case RandomIntegers():
			lowest_value, value_limit = find_drawn_interval(distribution)
			values = generator.integers(lowest_value, value_limit, shape.dimensions)
		case _:
			distribution_class = type(distribution)
			operation = UNKNOWN_DISTRIBUTION_OPERATION.format(distribution_name=distribution_class.__name__)
			raise RefusedOperationError(operation, UNKNOWN_DISTRIBUTION_ALTERNATIVE)

	return values


def require_valid_seed(seed: int) -> None:
	"""
	Check that a random seed is not negative.

	.. versionadded:: 0.1.0

	Parameters
	----------
	seed
		The seed to check.

	Raises
	------
	InvalidSeedError
		When ``seed`` is lower than 0.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.random_values import require_valid_seed
	>>> try:
	... 	require_valid_seed(-1)
	... except ndp.InvalidSeedError as error:
	... 	print(error)
	Expected a seed of at least 0, got -1.
	"""
	if seed < LOWEST_SEED:
		raise InvalidSeedError(seed)
