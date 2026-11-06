"""
Arithmetic between dates, datetimes, durations and numbers.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.conversion.time_text import format_durations
from numdaplot.arrays.operations.operand import Operand, convert_time_value, find_operand_type
from numdaplot.arrays.operations.time_bounds import require_nanoseconds_fit
from numdaplot.arrays.operations.time_result_bounds import require_time_result_fits, widen_large_integers
from numdaplot.data_types.numpy_mapping import to_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.value_conversion_error import ValueConversionError

TIME_FAMILIES = frozenset({ValueFamily.MOMENT, ValueFamily.DURATION})
# The family of the result of each accepted operation, by function and families of the left and right operands.
type TimeOperation = tuple[numpy.ufunc, ValueFamily, ValueFamily]
TIME_RESULTS = dict[TimeOperation, ValueFamily](
	{
		(numpy.add, ValueFamily.MOMENT, ValueFamily.DURATION): ValueFamily.MOMENT,
		(numpy.add, ValueFamily.DURATION, ValueFamily.MOMENT): ValueFamily.MOMENT,
		(numpy.add, ValueFamily.DURATION, ValueFamily.DURATION): ValueFamily.DURATION,
		(numpy.subtract, ValueFamily.MOMENT, ValueFamily.MOMENT): ValueFamily.DURATION,
		(numpy.subtract, ValueFamily.MOMENT, ValueFamily.DURATION): ValueFamily.MOMENT,
		(numpy.subtract, ValueFamily.DURATION, ValueFamily.DURATION): ValueFamily.DURATION,
		(numpy.multiply, ValueFamily.DURATION, ValueFamily.NUMBER): ValueFamily.DURATION,
		(numpy.multiply, ValueFamily.NUMBER, ValueFamily.DURATION): ValueFamily.DURATION,
		(numpy.true_divide, ValueFamily.DURATION, ValueFamily.NUMBER): ValueFamily.DURATION,
	}
)
DURATION_DIVISION = (numpy.true_divide, ValueFamily.DURATION, ValueFamily.DURATION)
DURATION_DIVISION_OPERATION = "Dividing a duration by a duration"
DURATION_DIVISION_ALTERNATIVE = "apply(ndp.DurationIn(unit=...))"
TIMEDELTA_PRODUCT_OPERATION = "Multiplying numbers by a single duration"
TIMEDELTA_PRODUCT_ALTERNATIVE = "apply(ndp.ToDuration(unit=...))"
NANOSECOND_DTYPES = {
	ValueFamily.MOMENT: to_numpy_dtype(Type.DATETIME),
	ValueFamily.DURATION: to_numpy_dtype(Type.DURATION),
}
ONE_DAY = numpy.timedelta64(1, "D")
NO_DURATION = numpy.timedelta64(0, "ns")


def involves_time(left: Operand, right: Operand) -> bool:
	"""
	Return whether one of two operands holds dates, datetimes or durations.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of an Array, or a single value.
	right
		The values of an Array, or a single value.

	Returns
	-------
	bool
		True when at least one side is a date, a datetime or a duration.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_arithmetic import involves_time
	>>> involves_time(numpy.array([1, 2]), timedelta(days=1))
	True
	"""
	left_type = find_operand_type(left)
	right_type = find_operand_type(right)
	left_family = find_family(left_type)
	right_family = find_family(right_type)
	has_time = left_family in TIME_FAMILIES or right_family in TIME_FAMILIES

	return has_time


def combine_time_values(left: Operand, right: Operand, function: numpy.ufunc, symbol: str) -> NDArray[Any]:
	"""
	Return the result of an arithmetic function between dates, datetimes, durations and numbers.

	Dates and datetimes give durations when subtracted; a duration added to or subtracted from a date gives
	a date, and from a datetime a datetime; durations add, subtract, and multiply or divide by numbers.
	A date counts as midnight next to a datetime.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of an Array, or a single value.
	right
		The values of an Array, or a single value. At least one side holds dates, datetimes or durations.
	function
		The numpy function, such as ``numpy.add``.
	symbol
		The operator shown in error messages, such as ``"+"``.

	Returns
	-------
	NDArray
		Dates, datetimes in nanoseconds or durations in nanoseconds.

	Raises
	------
	RefusedOperationError
		When a duration is divided by a duration, or numbers are multiplied by a single duration.
	ValueConversionError
		When a duration added to or subtracted from dates is not a whole number of days.
	IncompatibleTypesError
		When the operation does not apply to these types, such as a date plus a number.
	TimeOverflowError
		When an operand or a result is outside the range of nanoseconds, about 1677 to 2262 for dates and
		datetimes, and about 292 years for durations.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_arithmetic import combine_time_values
	>>> combine_time_values(numpy.array(["2026-01-31"], dtype="datetime64[D]"), timedelta(days=1), numpy.add, "+")
	array(['2026-02-01'], dtype='datetime64[D]')
	"""
	left_type = find_operand_type(left)
	right_type = find_operand_type(right)
	left_family = find_family(left_type)
	right_family = find_family(right_type)
	operation_key = (function, left_family, right_family)
	require_time_operation(left, right, operation_key)
	if operation_key not in TIME_RESULTS:
		raise IncompatibleTypesError(symbol, [left_type.name, right_type.name])

	combines_date = Type.DATE in (left_type, right_type)
	result_family = TIME_RESULTS[operation_key]
	keeps_date = combines_date and result_family == ValueFamily.MOMENT
	result_type = find_time_result_type(result_family, keeps_date)
	require_nanoseconds_fit(left, left_type, symbol)
	require_nanoseconds_fit(right, right_type, symbol)
	left_values = to_nanoseconds(left, left_family)
	right_values = to_nanoseconds(right, right_family)
	try:
		left_numbers = widen_large_integers(left_values)
		right_numbers = widen_large_integers(right_values)
		operands = [left_numbers, right_numbers]
		require_time_result_fits(operands, function, result_type, symbol)
		combined_values = function(left_numbers, right_numbers)
	except OverflowError as error:
		raise TimeOverflowError(symbol, result_type.name) from error

	if not keeps_date:
		return combined_values

	date_shift = right_values
	if left_family == ValueFamily.DURATION:
		date_shift = left_values

	require_whole_days(date_shift)
	date_dtype = to_numpy_dtype(Type.DATE)
	shifted_dates = combined_values.astype(date_dtype)

	return shifted_dates


def find_time_result_type(result_family: ValueFamily, keeps_date: bool) -> Type:
	"""
	Return the type of the result of an accepted operation on times.

	.. versionadded:: 0.1.0

	Parameters
	----------
	result_family
		The family of the result, ``MOMENT`` or ``DURATION``.
	keeps_date
		Whether the result stays a date.

	Returns
	-------
	Type
		``DURATION``, ``DATE`` or ``DATETIME``.

	Examples
	--------
	>>> from numdaplot.arrays.operations.time_arithmetic import find_time_result_type
	>>> from numdaplot.data_types.value_family import ValueFamily
	>>> find_time_result_type(ValueFamily.MOMENT, True)
	<Type.DATE: 14>
	"""
	if result_family == ValueFamily.DURATION:
		return Type.DURATION

	if keeps_date:
		return Type.DATE

	return Type.DATETIME


def require_time_operation(left: Operand, right: Operand, operation_key: TimeOperation) -> None:
	"""
	Check that an operation is not one of the duration operations written another way in numdaplot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of an Array, or a single value.
	right
		The values of an Array, or a single value.
	operation_key
		The numpy function, then the families of the left and right operands.

	Raises
	------
	RefusedOperationError
		When a duration is divided by a duration, which ``DurationIn`` does, or numbers are multiplied
		by a single duration, which ``ToDuration`` does.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_arithmetic import require_time_operation
	>>> from numdaplot.data_types.value_family import ValueFamily
	>>> key = (numpy.multiply, ValueFamily.NUMBER, ValueFamily.DURATION)
	>>> try:
	... 	require_time_operation(numpy.array([3]), timedelta(days=1), key)
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Multiplying numbers by a single duration is not available, use apply(ndp.ToDuration(unit=...)) instead.
	"""
	if operation_key == DURATION_DIVISION:
		raise RefusedOperationError(DURATION_DIVISION_OPERATION, DURATION_DIVISION_ALTERNATIVE)

	function, left_family, right_family = operation_key
	if function != numpy.multiply:
		return

	left_is_single_duration = left_family == ValueFamily.DURATION and not isinstance(left, numpy.ndarray)
	right_is_single_duration = right_family == ValueFamily.DURATION and not isinstance(right, numpy.ndarray)
	multiplies_single_duration = left_is_single_duration or right_is_single_duration
	if multiplies_single_duration:
		raise RefusedOperationError(TIMEDELTA_PRODUCT_OPERATION, TIMEDELTA_PRODUCT_ALTERNATIVE)


def to_nanoseconds(operand: Operand, family: ValueFamily) -> Any:
	"""
	Return an operand with its dates, datetimes or durations counted in nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operand
		The values of an Array, or a single value.
	family
		The family of the operand.

	Returns
	-------
	Any
		Datetimes or durations in nanoseconds, or the operand itself when it holds numbers.

	Examples
	--------
	>>> from datetime import date
	>>> from numdaplot.arrays.operations.time_arithmetic import to_nanoseconds
	>>> from numdaplot.data_types.value_family import ValueFamily
	>>> to_nanoseconds(date(2026, 1, 31), ValueFamily.MOMENT)
	np.datetime64('2026-01-31T00:00:00.000000000')
	"""
	if family not in NANOSECOND_DTYPES:
		return operand

	numpy_operand = cast(Any, operand)
	if not isinstance(operand, numpy.ndarray):
		numpy_operand = convert_time_value(operand)

	nanosecond_dtype = NANOSECOND_DTYPES[family]
	nanosecond_operand = numpy_operand.astype(nanosecond_dtype)

	return nanosecond_operand


def require_whole_days(durations: NDArray[numpy.timedelta64] | numpy.timedelta64) -> None:
	"""
	Check that durations added to or subtracted from dates are whole numbers of days.

	.. versionadded:: 0.1.0

	Parameters
	----------
	durations
		Durations in nanoseconds, an array or a single value.

	Raises
	------
	ValueConversionError
		When a duration is not a whole number of days, citing the first one.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_arithmetic import require_whole_days
	>>> try:
	... 	require_whole_days(numpy.array([36], dtype="timedelta64[h]").astype("timedelta64[ns]"))
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store the DURATION value '1 days 12:00:00' as DATE without losing information.
	"""
	duration_values = numpy.atleast_1d(durations)
	present_durations = duration_values[~numpy.isnat(duration_values)]
	remainders = present_durations % ONE_DAY
	partial_days = present_durations[remainders != NO_DURATION]
	partial_count = len(partial_days)
	if partial_count == 0:
		return

	partial_texts = format_durations(partial_days)
	first_partial_text = str(partial_texts[0])
	raise ValueConversionError(Type.DURATION.name, Type.DATE.name, first_partial_text)
