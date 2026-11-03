"""
Sine math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction


@dataclass(frozen=True)
class Sine(MathFunction):
	"""
	Sine of each value, read as an angle in radians.

	Missing values stay missing.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Sine()
	Sine()
	"""
