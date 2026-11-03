"""
Statistics and math functions computed on an Array.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.calculation.math_function_values import apply_math_function
from numdaplot.arrays.calculation.statistic_values import compute_statistic
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.positions.axis import Axis
from numdaplot.statistics.statistic import Statistic


class ArrayCalculation(ArrayData):
	"""
	Statistics with ``compute`` and math functions with ``apply``.

	.. versionadded:: 0.1.0
	"""

	def compute(self, statistic: Statistic, axis: Axis | None = None) -> Self:
		"""
		Return a statistic of the values, ignoring missing values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		statistic
			Any statistic of numdaplot, such as ``ndp.Mean()`` or ``ndp.Quantile(0.9)``.
		axis
			``EACH_ROW`` for one result per row, ``EACH_COLUMN`` for one per column, only for a
			two-dimensional Array. A single result for the whole Array when omitted.

		Returns
		-------
		Self
			A new Array: one value when ``axis`` is omitted, read it with ``to_value``.

		Raises
		------
		IncompatibleTypesError
			When the statistic does not apply to the type of the values, such as the mean of texts.
		DimensionError
			When an axis is given for an Array that is not two-dimensional.
		EmptyArrayError
			When the statistic needs a value, such as ``Mean``, and the whole Array, or a row or column,
			has no present value.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> temperatures = ndp.Array.from_list([12.0, None, 18.0])
		>>> temperatures.compute(ndp.Mean()).to_value()
		15.0
		"""
		statistic_values = compute_statistic(self._values, statistic, axis)
		statistic_array = self._wrap(statistic_values)

		return statistic_array

	def apply(self, function: MathFunction) -> Self:
		"""
		Return a math function applied to each value of a number Array.

		.. versionadded:: 0.1.0

		Parameters
		----------
		function
			Any math function of numdaplot, such as ``ndp.SquareRoot()`` or ``ndp.Round(decimals=2)``.

		Returns
		-------
		Self
			A new Array of the same shape. Missing values stay missing.

		Raises
		------
		IncompatibleTypesError
			When the values are not numbers.
		OutOfDomainError
			When a value is outside the domain of the function, such as the square root of -1.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([1, 4, 9]).apply(ndp.SquareRoot())
		Array([1., 2., 3.], dtype=FLOAT64)
		"""
		transformed_values = apply_math_function(self._values, function)
		transformed_array = self._wrap(transformed_values)

		return transformed_array
