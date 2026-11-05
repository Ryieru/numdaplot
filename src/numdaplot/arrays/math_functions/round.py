"""
Rounding math function.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.settings.field_types import require_field_types


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


	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.346, 2.5, 3.5])
	>>> prices.apply(ndp.Round(decimals=2))
	Array([12.35,  2.5 ,  3.5 ], dtype=FLOAT64)
	>>> prices.apply(ndp.Round())
	Array([12.,  2.,  4.], dtype=FLOAT64)
	"""

	decimals: int = 0

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
