"""
Masks of the rules comparing each value with reference values.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array_data import ArrayData, read_stored_values
from numdaplot.arrays.export.python_values import to_python_list
from numdaplot.arrays.operations.type_requirements import require_comparable
from numdaplot.arrays.rules.array_reference import compare_with_array
from numdaplot.arrays.rules.time_reference import compare_with_reference
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.errors.rules.invalid_bounds_error import InvalidBoundsError
from numdaplot.rules.between import Between
from numdaplot.rules.bounds import HIGH_INCLUDED_BOUNDS, LOW_INCLUDED_BOUNDS
from numdaplot.rules.equal import Equal
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual
from numdaplot.rules.not_equal import NotEqual
from numdaplot.rules.value_rule import ValueRule

COMPARISON_FUNCTIONS = dict[type[ValueRule[Any]], numpy.ufunc](
	{
		Equal: numpy.equal,
		NotEqual: numpy.not_equal,
		Greater: numpy.greater,
		GreaterOrEqual: numpy.greater_equal,
		Less: numpy.less,
		LessOrEqual: numpy.less_equal,
	}
)
BETWEEN_NAME = "Between"


def build_comparison_mask(values: NDArray[Any], rule: ValueRule[Any]) -> NDArray[numpy.bool_]:
	"""
	Return which values satisfy a rule comparing them with a single reference value, or with an Array of them.

	A missing value never satisfies the rule, not even ``NotEqual``. A date, a datetime or a duration that nanoseconds
	cannot hold lies beyond every datetime or duration: ``Less`` accepts them all for a reference in the year 3000.
	An Array as reference compares each value with the value at its position, a missing one matching nothing.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an Array as reference value.

	Parameters
	----------
	values
		The values of an Array.
	rule
		``Equal``, ``NotEqual``, ``Greater``, ``GreaterOrEqual``, ``Less`` or ``LessOrEqual``.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each value satisfying the rule.

	Raises
	------
	IncompatibleTypesError
		When the reference value cannot be compared with the values.
	ShapeMismatchError
		When an Array as reference does not have the shape of the values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.comparison_masks import build_comparison_mask
	>>> build_comparison_mask(numpy.array([1, 5, 9]), ndp.Greater(4))
	array([False,  True,  True])
	"""
	rule_class = type(rule)
	rule_name = rule_class.__name__
	compare = COMPARISON_FUNCTIONS[rule_class]
	reference = rule.value
	if isinstance(reference, ArrayData):
		matches = compare_with_array(values, reference, compare, rule_name)
	else:
		require_comparable(values, reference, rule_name)
		matches = compare_with_reference(values, reference, compare)

	missing = find_missing(values)
	present = ~missing
	mask = matches & present

	return mask


def build_between_mask(values: NDArray[Any], rule: Between[Any]) -> NDArray[numpy.bool_]:
	"""
	Return which values lie inside the interval of a ``Between`` rule.

	A bound given by an Array gives each value the bound at its position. A missing value, or a missing bound, is never
	inside.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts bounds given by Arrays.

	Parameters
	----------
	values
		The values of an Array.
	rule
		The interval and the bounds it includes.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each value inside the interval. A missing value is never inside.

	Raises
	------
	IncompatibleTypesError
		When the bounds cannot be compared with the values.
	ShapeMismatchError
		When a bound given by an Array does not have the shape of the values.
	InvalidBoundsError
		At the first position whose low bound is greater than its high bound.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.comparison_masks import build_between_mask
	>>> build_between_mask(numpy.array([1, 5, 9]), ndp.Between(low=1, high=5, bounds=ndp.Bounds.HIGH_ONLY))
	array([False,  True, False])
	"""
	compare_with_low = numpy.greater
	if rule.bounds in LOW_INCLUDED_BOUNDS:
		compare_with_low = numpy.greater_equal

	compare_with_high = numpy.less
	if rule.bounds in HIGH_INCLUDED_BOUNDS:
		compare_with_high = numpy.less_equal

	above_low = compare_with_bound(values, rule.low, compare_with_low)
	below_high = compare_with_bound(values, rule.high, compare_with_high)
	require_ordered_bounds(rule)
	missing = find_missing(values)
	present = ~missing
	mask = above_low & below_high & present

	return mask


def compare_with_bound(values: NDArray[Any], bound: Any, compare: numpy.ufunc) -> NDArray[numpy.bool_]:
	"""
	Return the comparison of each value with a bound of a ``Between`` rule: a single value or an Array.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values compared.
	bound
		A single Python value, or an Array of the shape of the values.
	compare
		The numpy comparison, with the values on its left.

	Returns
	-------
	NDArray[numpy.bool_]
		The result at each position, False where a bound given by an Array is missing.

	Raises
	------
	IncompatibleTypesError
		When the bound cannot be compared with the values.
	ShapeMismatchError
		When a bound given by an Array does not have the shape of the values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.comparison_masks import compare_with_bound
	>>> highs = ndp.Array.from_list([20.0, 10.0])
	>>> compare_with_bound(numpy.array([18.0, 18.0]), highs, numpy.less_equal)
	array([ True, False])
	"""
	if isinstance(bound, ArrayData):
		array_matches = compare_with_array(values, bound, compare, BETWEEN_NAME)
		return array_matches

	require_comparable(values, bound, BETWEEN_NAME)
	matches = compare_with_reference(values, bound, compare)

	return matches


def require_ordered_bounds(rule: Between[Any]) -> None:
	"""
	Check that a ``Between`` rule with a bound given by an Array has no position whose low bound is above its high one.

	Bounds given as single values are checked when the rule is created. A position with a missing bound is left aside.

	.. versionadded:: 0.2.0

	Parameters
	----------
	rule
		The interval.

	Raises
	------
	InvalidBoundsError
		At the first position whose low bound is greater than its high bound.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.comparison_masks import require_ordered_bounds
	>>> lows = ndp.Array.from_list([10.0, 30.0])
	>>> try:
	... 	require_ordered_bounds(ndp.Between(lows, 20.0))
	... except ndp.InvalidBoundsError as error:
	... 	print(error)
	Expected comparable bounds with low <= high, got low=30.0 and high=20.0.
	"""
	low = rule.low
	high = rule.high
	if isinstance(low, ArrayData):
		low_values = read_stored_values(low)
		reversed_positions = compare_with_bound(low_values, high, numpy.greater)
	elif isinstance(high, ArrayData):
		high_values = read_stored_values(high)
		reversed_positions = compare_with_bound(high_values, low, numpy.less)
	else:
		return

	has_reversed = bool(reversed_positions.any())
	if not has_reversed:
		return

	first_position = int(numpy.argmax(reversed_positions))
	reversed_low = read_bound_value(low, first_position)
	reversed_high = read_bound_value(high, first_position)
	raise InvalidBoundsError(reversed_low, reversed_high)


def read_bound_value(bound: Any, position: int) -> Any:
	"""
	Return the bound of a ``Between`` rule at a position, as a Python value.

	.. versionadded:: 0.2.0

	Parameters
	----------
	bound
		A single Python value, or a one-dimensional Array.
	position
		The position in the flattened values.

	Returns
	-------
	Any
		The single value itself, or the value of the Array at the position.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.comparison_masks import read_bound_value
	>>> read_bound_value(ndp.Array.from_list([10.0, 30.0]), 1), read_bound_value(20.0, 1)
	(30.0, 20.0)
	"""
	if not isinstance(bound, ArrayData):
		return bound

	bound_values = read_stored_values(bound)
	flat_values = bound_values.ravel()
	position_values = flat_values[position : position + 1]
	python_values = to_python_list(position_values)
	bound_value = python_values[0]

	return bound_value
