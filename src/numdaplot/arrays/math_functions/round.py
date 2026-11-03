"""
Rounding math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction


@dataclass(frozen=True)
class Round(MathFunction):
	"""
	Each value rounded to a number of decimals.

	A value exactly halfway is rounded to the nearest even digit, as in numpy:
	2.5 gives 2 and 3.5 gives 4. Missing values stay missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	decimals
		Number of decimals kept, 0 by default to round to whole numbers. A negative number rounds to
		tens, hundreds...: -2 turns 1234 into 1200.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Round()
	Round(decimals=0)
	>>> ndp.Round(decimals=2)
	Round(decimals=2)
	"""

	decimals: int = 0
