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
	.. versionchanged:: 0.2.0
		Gives ``FLOAT64`` for integers of any size.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import math
	>>> angles = ndp.Array.from_list([0.0, math.pi / 2])
	>>> angles.apply(ndp.Sine())
	Array([0., 1.], dtype=FLOAT64)
	"""
