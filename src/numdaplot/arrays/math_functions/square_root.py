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
	>>> areas = ndp.Array.from_list([4, 9, 16])
	>>> areas.apply(ndp.SquareRoot())
	Array([2., 3., 4.], dtype=FLOAT64)
	"""
