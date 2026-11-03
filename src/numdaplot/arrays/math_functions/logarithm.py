"""
Logarithm math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.errors.invalid_base_error import InvalidBaseError

LOWEST_EXCLUDED_BASE = 0
FORBIDDEN_BASE = 1


@dataclass(frozen=True)
class Logarithm(MathFunction):
	"""
	Logarithm of each value: with ``base=10``, 1000 gives 3.

	Applying it to a value lower than or equal to 0 raises ``OutOfDomainError``.
	Missing values stay missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	base
		Base of the logarithm, greater than 0 and different from 1.
		The natural logarithm, of base ``e``, when omitted.

	Raises
	------
	InvalidBaseError
		When ``base`` is lower than or equal to 0, or equal to 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Logarithm(base=10)
	Logarithm(base=10)
	"""

	base: float | None = None

	def __post_init__(self) -> None:
		"""
		Check that the base can be used.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidBaseError
			When ``base`` is lower than or equal to 0, or equal to 1.
		"""
		if self.base is None:
			return

		if self.base <= LOWEST_EXCLUDED_BASE:
			raise InvalidBaseError(self.base)

		if self.base == FORBIDDEN_BASE:
			raise InvalidBaseError(self.base)
