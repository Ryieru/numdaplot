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
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.types.numpy_mapping import to_numpy_dtype
from numdaplot.types.type import Type
from numdaplot.types.value_family import ValueFamily, find_family

TIME_FAMILIES = frozenset({ValueFamily.MOMENT, ValueFamily.DURATION, ValueFamily.TIME})
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
		(numpy.add, ValueFamily.TIME, ValueFamily.DURATION): ValueFamily.TIME,
		(numpy.add, ValueFamily.DURATION, ValueFamily.TIME): ValueFamily.TIME,
		(numpy.subtract, ValueFamily.TIME, ValueFamily.DURATION): ValueFamily.TIME,
		(numpy.subtract, ValueFamily.TIME, ValueFamily.TIME): ValueFamily.DURATION,
		(numpy.add, ValueFamily.MOMENT, ValueFamily.TIME): ValueFamily.MOMENT,
		(numpy.add, ValueFamily.TIME, ValueFamily.MOMENT): ValueFamily.MOMENT,
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
	ValueFamily.TIME: to_numpy_dtype(Type.DURATION),
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
	A date counts as midnight next to a datetime. Times of day give durations when subtracted, move by a
	duration within the same day, and give a datetime when added to a date.

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
		When the operation does not apply to these types, such as a date plus a number, or a datetime plus a time of
		day.
	TimeOverflowError
		When an operand or a result is outside the range of nanoseconds, about 1677 to 2262 for dates and
		datetimes, and about 292 years for durations, or a time of day moves past midnight.

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

	require_date_next_to_time(left_type, right_type, symbol)
	result_family = TIME_RESULTS[operation_key]
	shifts_date = Type.DATE in (left_type, right_type) and ValueFamily.DURATION in (left_family, right_family)
	keeps_date = shifts_date and result_family == ValueFamily.MOMENT
	result_type = find_time_result_type(result_family, keeps_date)
	operands = [left, right]
	combined_values = combine_nanoseconds(operands, function, result_type, symbol)
	if result_type == Type.TIME:
		times = store_time_result(combined_values, symbol)
		return times

	if not keeps_date:
		return combined_values

	date_shift = to_nanoseconds(right, right_family)
	if left_family == ValueFamily.DURATION:
		date_shift = to_nanoseconds(left, left_family)

	require_whole_days(date_shift)
	date_dtype = to_numpy_dtype(Type.DATE)
	shifted_dates = combined_values.astype(date_dtype)

	return shifted_dates


def combine_nanoseconds(operands: list[Operand], function: numpy.ufunc, result_type: Type, symbol: str) -> NDArray[Any]:
	"""
	Return an arithmetic function applied to operands counted in nanoseconds, refusing results that do not fit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The left and the right operand, values of Arrays or single values.
	function
		The numpy function, such as ``numpy.add``.
	result_type
		The type of the result, named by the errors.
	symbol
		The operator shown in error messages, such as ``"+"``.

	Returns
	-------
	NDArray
		The result, dates and datetimes in ``datetime64[ns]`` and durations in ``timedelta64[ns]``.

	Raises
	------
	TimeOverflowError
		When an operand or the result is outside the range of nanoseconds.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_arithmetic import combine_nanoseconds
	>>> durations = numpy.array([1], dtype="timedelta64[s]")
	>>> combine_nanoseconds([durations, timedelta(seconds=1)], numpy.add, ndp.Type.DURATION, "+")
	array([2000000000], dtype='timedelta64[ns]')
	"""
	left, right = operands
	left_type = find_operand_type(left)
	right_type = find_operand_type(right)
	require_nanoseconds_fit(left, left_type, symbol)
	require_nanoseconds_fit(right, right_type, symbol)
	left_family = find_family(left_type)
	right_family = find_family(right_type)
	left_values = to_nanoseconds(left, left_family)
	right_values = to_nanoseconds(right, right_family)
	# A time of day moved by a duration is first computed as a duration, then checked against midnight.
	fitted_type = Type.DURATION if result_type == Type.TIME else result_type
	try:
		left_numbers = widen_large_integers(left_values)
		right_numbers = widen_large_integers(right_values)
		number_operands = [left_numbers, right_numbers]
		require_time_result_fits(number_operands, function, fitted_type, symbol)
		combined_values = function(left_numbers, right_numbers)
	except OverflowError as error:
		raise TimeOverflowError(symbol, fitted_type.name) from error

	return combined_values


def store_time_result(durations: NDArray[Any], symbol: str) -> NDArray[numpy.timedelta64]:
	"""
	Return times of day computed as durations since midnight, refusing those past midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	durations
		The times since midnight in ``timedelta64[ns]``, NaT where missing.
	symbol
		The operator shown in error messages, such as ``"+"``.

	Returns
	-------
	NDArray[numpy.timedelta64]
		The times of day in ``timedelta64[us]``.

	Raises
	------
	TimeOverflowError
		When a time is before midnight or from the next midnight on.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_arithmetic import store_time_result
	>>> store_time_result(numpy.array([3600000000000], dtype="timedelta64[ns]"), "+")
	array([3600000000], dtype='timedelta64[us]')
	"""
	is_missing = numpy.isnat(durations)
	is_before_midnight = durations < NO_DURATION
	is_next_day = durations >= ONE_DAY
	is_outside_day = (is_before_midnight | is_next_day) & ~is_missing
	has_outside_day = bool(is_outside_day.any())
	if has_outside_day:
		raise TimeOverflowError(symbol, Type.TIME.name)

	time_dtype = to_numpy_dtype(Type.TIME)
	times = durations.astype(time_dtype)

	return times


def require_date_next_to_time(left_type: Type, right_type: Type, symbol: str) -> None:
	"""
	Check that a time of day is only added to dates, never to datetimes, which already have a time.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left_type
		The type of the left operand.
	right_type
		The type of the right operand.
	symbol
		The operator shown in error messages, such as ``"+"``.

	Raises
	------
	IncompatibleTypesError
		When a time of day is combined with datetimes.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_arithmetic import require_date_next_to_time
	>>> try:
	... 	require_date_next_to_time(ndp.Type.DATETIME, ndp.Type.TIME, "+")
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply + to DATETIME and TIME.
	"""
	operand_types = (left_type, right_type)
	combines_datetime_with_time = Type.TIME in operand_types and Type.DATETIME in operand_types
	if combines_datetime_with_time:
		raise IncompatibleTypesError(symbol, [left_type.name, right_type.name])


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
		``DURATION``, ``TIME``, ``DATE`` or ``DATETIME``.

	Examples
	--------
	>>> from numdaplot.arrays.operations.time_arithmetic import find_time_result_type
	>>> from numdaplot.types.value_family import ValueFamily
	>>> find_time_result_type(ValueFamily.MOMENT, True)
	<Type.DATE: 14>
	"""
	if result_family == ValueFamily.DURATION:
		return Type.DURATION

	if result_family == ValueFamily.TIME:
		return Type.TIME

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
	>>> from numdaplot.types.value_family import ValueFamily
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
	>>> from numdaplot.types.value_family import ValueFamily
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
