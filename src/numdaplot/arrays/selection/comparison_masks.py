"""
Masks of the rules comparing each value with reference values.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.type_requirements import require_comparable
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.arrays.selection.time_reference import compare_with_reference
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
	Return which values satisfy a rule comparing them with a single reference value.

	A missing value never satisfies the rule, not even ``NotEqual``. A date, a datetime or a duration that nanoseconds
	cannot hold lies beyond every datetime or duration: ``Less`` accepts them all for a reference in the year 3000.

	.. versionadded:: 0.1.0

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

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.comparison_masks import build_comparison_mask
	>>> build_comparison_mask(numpy.array([1, 5, 9]), ndp.Greater(4))
	array([False,  True,  True])
	"""
	rule_class = type(rule)
	require_comparable(values, rule.value, rule_class.__name__)

	compare = COMPARISON_FUNCTIONS[rule_class]
	matches = compare_with_reference(values, rule.value, compare)
	missing = find_missing(values)
	present = ~missing
	mask = matches & present

	return mask


def build_between_mask(values: NDArray[Any], rule: Between[Any]) -> NDArray[numpy.bool_]:
	"""
	Return which values lie inside the interval of a ``Between`` rule.

	.. versionadded:: 0.1.0

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

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.comparison_masks import build_between_mask
	>>> build_between_mask(numpy.array([1, 5, 9]), ndp.Between(low=1, high=5, bounds=ndp.Bounds.HIGH_ONLY))
	array([False,  True, False])
	"""
	require_comparable(values, rule.low, BETWEEN_NAME)

	compare_with_low = numpy.greater
	if rule.bounds in LOW_INCLUDED_BOUNDS:
		compare_with_low = numpy.greater_equal

	compare_with_high = numpy.less
	if rule.bounds in HIGH_INCLUDED_BOUNDS:
		compare_with_high = numpy.less_equal

	above_low = compare_with_reference(values, rule.low, compare_with_low)
	below_high = compare_with_reference(values, rule.high, compare_with_high)
	missing = find_missing(values)
	present = ~missing
	mask = above_low & below_high & present

	return mask
