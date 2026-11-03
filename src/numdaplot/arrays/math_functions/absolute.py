"""
Absolute value math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction


@dataclass(frozen=True)
class Absolute(MathFunction):
	"""
	Absolute value of each value, its distance to 0: -3 and 3 both give 3.

	Missing values stay missing.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Absolute()
	Absolute()
	"""
