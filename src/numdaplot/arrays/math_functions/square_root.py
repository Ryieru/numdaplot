"""
Square root math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction


@dataclass(frozen=True)
class SquareRoot(MathFunction):
	"""
	Square root of each value: 9 gives 3.

	Applying it to a negative value raises ``OutOfDomainError``. Missing values stay missing.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.SquareRoot()
	SquareRoot()
	"""
