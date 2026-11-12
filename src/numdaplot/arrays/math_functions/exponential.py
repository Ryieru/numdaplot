"""
Exponential math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction


@dataclass(frozen=True)
class Exponential(MathFunction):
	"""
	Exponential of each value, ``e`` raised to the value: 0 gives 1, 1 gives about 2.718.

	Missing values stay missing.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Gives ``FLOAT64`` for integers of any size.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> rates = ndp.Array.from_list([0.0, 1.0])
	>>> rates.apply(ndp.Exponential())
	Array([1.        , 2.71828183], dtype=FLOAT64)
	"""
