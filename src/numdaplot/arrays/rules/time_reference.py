"""
Comparison of nanosecond values with a date, a datetime or a duration that nanoseconds cannot hold.

Such a reference lies beyond every stored value, so the answer is known without converting it, which numpy
either refuses or does wrongly.

.. versionadded:: 0.1.0
"""

from datetime import timedelta
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.operand import LONGEST_MICROSECOND_DURATION, convert_time_value
from numdaplot.arrays.operations.time_bounds import NANOSECOND_DTYPES
from numdaplot.column_storage.time_range import is_python_time_in_range

MICROSECOND_DURATION_DTYPE = numpy.dtype("timedelta64[us]")
AFTER_EVERY_VALUE = 1
BEFORE_EVERY_VALUE = -1
ANY_STORED_VALUE = 0
NO_DURATION = timedelta(0)
FIRST_YEAR_AFTER_ZERO = 1970


def is_far_reference(values: NDArray[Any], reference: object) -> bool:
	"""
	Return whether a reference value lies beyond everything nanosecond values can hold.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	reference
		A single Python value.

	Returns
	-------
	bool
		True for a date, a datetime or a duration out of range, beside values stored in nanoseconds, and for a duration
		that microseconds cannot count, beside durations stored in microseconds.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numpy
	>>> from numdaplot.arrays.rules.time_reference import is_far_reference
	>>> moments = numpy.array(["2026-01-31"], dtype="datetime64[ns]")
	>>> is_far_reference(moments, datetime(3000, 1, 1)), is_far_reference(moments, datetime(2026, 1, 1))
	(True, False)
	"""
	if values.dtype == MICROSECOND_DURATION_DTYPE and isinstance(reference, timedelta):
		is_too_long = abs(reference) > LONGEST_MICROSECOND_DURATION
		return is_too_long

	if values.dtype not in NANOSECOND_DTYPES:
		return False

	in_range = is_python_time_in_range(reference)

	return not in_range


def find_far_side(reference: Any) -> int:
	"""
	Return on which side of every stored value a reference out of range lies.

	.. versionadded:: 0.1.0

	Parameters
	----------
	reference
		A date, a datetime or a duration out of range.

	Returns
	-------
	int
		1 after every value, -1 before every value.

	Examples
	--------
	>>> from datetime import date, timedelta
	>>> from numdaplot.arrays.rules.time_reference import find_far_side
	>>> find_far_side(date(3000, 1, 1)), find_far_side(date(1000, 1, 1)), find_far_side(timedelta(days=-200000))
	(1, -1, -1)
	"""
	if isinstance(reference, timedelta):
		is_after = reference > NO_DURATION
	else:
		is_after = reference.year >= FIRST_YEAR_AFTER_ZERO

	if is_after:
		return AFTER_EVERY_VALUE

	return BEFORE_EVERY_VALUE


def compare_with_reference(values: NDArray[Any], reference: Any, compare: numpy.ufunc) -> NDArray[numpy.bool_]:
	"""
	Return the comparison of each value with a reference value, which may be out of range.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	reference
		A single Python value.
	compare
		The numpy comparison, such as ``numpy.less``, with the values on its left.

	Returns
	-------
	NDArray[numpy.bool_]
		The result for each value, a missing value not being set apart.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numpy
	>>> from numdaplot.arrays.rules.time_reference import compare_with_reference
	>>> moments = numpy.array(["2026-01-31"], dtype="datetime64[ns]")
	>>> compare_with_reference(moments, datetime(3000, 1, 1), numpy.less)
	array([ True])
	"""
	is_far = is_far_reference(values, reference)
	if is_far:
		far_side = find_far_side(reference)
		same_answer = compare(ANY_STORED_VALUE, far_side)
		far_matches = numpy.full(values.shape, same_answer, dtype=numpy.bool_)
		return far_matches

	numpy_reference = convert_time_value(reference)
	matches = compare(values, numpy_reference)

	return matches


def remove_far_references(values: NDArray[Any], references: list[Any]) -> list[Any]:
	"""
	Return the reference values that may equal a stored value, those out of range never doing so.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	references
		Single Python values.

	Returns
	-------
	list[Any]
		The values kept, in their order.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numpy
	>>> from numdaplot.arrays.rules.time_reference import remove_far_references
	>>> moments = numpy.array(["2026-01-31"], dtype="datetime64[ns]")
	>>> remove_far_references(moments, [datetime(2026, 1, 31), datetime(3000, 1, 1)])
	[datetime.datetime(2026, 1, 31, 0, 0)]
	"""
	near_references = [reference for reference in references if not is_far_reference(values, reference)]

	return near_references
