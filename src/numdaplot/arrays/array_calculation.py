"""
Statistics, math functions and time functions computed on an Array.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.calculation.math_function_values import apply_math_function
from numdaplot.arrays.calculation.statistic_values import compute_statistic
from numdaplot.arrays.calculation.time_function_values import apply_time_function
from numdaplot.arrays.mapping.mapped_values import map_values
from numdaplot.arrays.mapping.value_mapping import ValueMapping
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.dates.time_function import TimeFunction
from numdaplot.positions.axis import Axis
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.statistics.statistic import Statistic


class ArrayCalculation(ArrayData):
	"""
	Statistics with ``compute``, math and time functions with ``apply``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def compute(self, statistic: Statistic, axis: Axis | None = None) -> Self:
		"""
		Return a statistic of the values, ignoring missing values unless ``Count`` is set to include them.

		.. versionadded:: 0.1.0

		Parameters
		----------
		statistic
			A ``Statistic``, such as ``ndp.Mean()`` or ``ndp.Quantile(0.9)``: see ``Statistic`` for every statistic.
		axis
			``EACH_ROW`` for one result per row, ``EACH_COLUMN`` for one per column, only for a
			two-dimensional Array. A single result for the whole Array when omitted.

		Returns
		-------
		Self
			A new Array: one value when ``axis`` is omitted, read it with ``to_value``.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the statistic does not apply to the type of the values, such as the mean of texts.
		DimensionError
			When an axis is given for an Array that is not two-dimensional.
		EmptyArrayError
			When the statistic needs a value, such as ``Mean``, and the whole Array, or a row or column,
			has no present value.
		IntegerOverflowError
			When the ``Sum`` of integers does not fit their type.

		Warns
		-----
		CalculationWarning
			When a result on decimals becomes an infinite value or NaN.

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

	@checked_arguments
	def apply(self, function: MathFunction | TimeFunction | ValueMapping) -> Self:
		"""
		Return a math function, a time function or a value mapping applied to each value.

		.. versionadded:: 0.1.0
		.. versionchanged:: 0.2.0
			Accepts a ``ValueMapping`` keeping the values it does not list, with ``others=Unmatched.KEEP``.

		Parameters
		----------
		function
			A ``MathFunction``, such as ``ndp.SquareRoot()``, applied to numbers, or a ``TimeFunction``,
			such as ``ndp.DatePart(unit=ndp.DatePartUnit.MONTH)``, applied to dates, datetimes, durations or
			numbers as each one states: see ``MathFunction`` and ``TimeFunction`` for every function. Or a
			``ValueMapping`` giving a new value to listed values, such as codes replaced by labels.

		Returns
		-------
		Self
			A new Array of the same shape. Missing values stay missing.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the function does not apply to the type of the values, or a ``ValueMapping`` with
			``Unmatched.KEEP`` gives new values of another family than the kept values, such as texts among numbers.
		OutOfDomainError
			When a value is outside the domain of a math function, such as the square root of -1.
		UnmatchedValueError
			When a value has no ``ValueChange`` in a ``ValueMapping`` whose ``others`` is ``Unmatched.ERROR``.
		UnsupportedMissingError
			When a ``ValueMapping`` gives integers or booleans and a missing value.

		Warns
		-----
		CalculationWarning
			When a result of a math function becomes an infinite value or NaN.

		Examples
		--------
		>>> from datetime import date
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([1, 4, 9]).apply(ndp.SquareRoot())
		Array([1., 2., 3.], dtype=FLOAT64)
		>>> ndp.Array.from_list([date(2026, 3, 14)]).apply(ndp.DatePart(unit=ndp.DatePartUnit.MONTH))
		Array([3.], dtype=FLOAT64)
		>>> sexes = ndp.ValueMapping(changes=[ndp.ValueChange(1, "M"), ndp.ValueChange(2, "F")])
		>>> ndp.Array.from_list([2, 1]).apply(sexes)
		Array(['F', 'M'], dtype=TEXT)
		"""
		if isinstance(function, ValueMapping):
			mapped_values = map_values(self._values, function)
			mapped_array = self._wrap(mapped_values)
			return mapped_array

		if isinstance(function, TimeFunction):
			time_values = apply_time_function(self._values, function)
			time_array = self._wrap(time_values)
			return time_array

		transformed_values = apply_math_function(self._values, function)
		transformed_array = self._wrap(transformed_values)

		return transformed_array
