"""
Application of a time function to each value of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any, Literal, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.arrays.operations.time_bounds import require_decimal_durations_fit, require_whole_durations_fit
from numdaplot.arrays.operations.type_requirements import require_family
from numdaplot.data_types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily
from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.date_period import DatePeriod
from numdaplot.dates.duration_in import DurationIn
from numdaplot.dates.duration_unit import DurationUnit
from numdaplot.dates.period_unit import PeriodUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.dates.to_duration import ToDuration
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError

MOMENT_FAMILIES = frozenset({ValueFamily.MOMENT})
DURATION_FAMILIES = frozenset({ValueFamily.DURATION})
NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})
TIME_OF_DAY_PARTS = frozenset({DatePartUnit.HOUR, DatePartUnit.MINUTE, DatePartUnit.SECOND})
PART_ATTRIBUTES = {
	DatePartUnit.YEAR: "year",
	DatePartUnit.QUARTER: "quarter",
	DatePartUnit.MONTH: "month",
	DatePartUnit.DAY: "day",
	DatePartUnit.DAY_OF_YEAR: "day_of_year",
	DatePartUnit.HOUR: "hour",
	DatePartUnit.MINUTE: "minute",
	DatePartUnit.SECOND: "second",
}
ISO_WEEK_COLUMN = "week"
# pandas numbers the days of the week from 0 for Monday, numdaplot from 1 for Monday.
WEEKDAY_SHIFT = 1
PERIOD_FREQUENCIES = {
	PeriodUnit.YEAR: "Y",
	PeriodUnit.QUARTER: "Q",
	PeriodUnit.MONTH: "M",
	# Weeks ending on Sunday, so each period starts on Monday.
	PeriodUnit.WEEK: "W-SUN",
	PeriodUnit.DAY: "D",
	PeriodUnit.HOUR: "h",
}
type DurationCode = Literal["W", "D", "h", "m", "s"]
DURATION_UNIT_CODES = dict[DurationUnit, DurationCode](
	{
		DurationUnit.WEEK: "W",
		DurationUnit.DAY: "D",
		DurationUnit.HOUR: "h",
		DurationUnit.MINUTE: "m",
		DurationUnit.SECOND: "s",
	}
)
NANOSECOND_CODE = "ns"
WHOLE_NUMBER_KINDS = frozenset({"i", "u"})
NOT_A_TIME = "NaT"
UNKNOWN_FUNCTION_OPERATION = "The time function {function_name}"
UNKNOWN_FUNCTION_ALTERNATIVE = "a time function of numdaplot"


def apply_time_function(values: NDArray[Any], function: TimeFunction) -> NDArray[Any]:
	"""
	Return the result of a time function applied to each value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	function
		Any time function of numdaplot.

	Returns
	-------
	NDArray
		The results, of the same shape. Missing values stay missing.

	Raises
	------
	IncompatibleTypesError
		When the function does not apply to the type of the values, such as an hour read from dates.
	RefusedOperationError
		When the function is not a time function of numdaplot.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.time_function_values import apply_time_function
	>>> days = numpy.array(["2026-12-31"], dtype="datetime64[D]")
	>>> apply_time_function(days, ndp.DatePart(unit=ndp.DatePartUnit.MONTH))
	array([12.])
	"""
	function_class = type(function)
	function_name = function_class.__name__

	match function:
		case DatePart():
			results = read_date_parts(values, function.unit, function_name)
		case DatePeriod():
			results = find_date_periods(values, function.unit, function_name)
		case DurationIn():
			results = count_durations(values, function.unit, function_name)
		case ToDuration():
			results = build_durations(values, function.unit, function_name)
		case _:
			operation = UNKNOWN_FUNCTION_OPERATION.format(function_name=function_name)
			raise RefusedOperationError(operation, UNKNOWN_FUNCTION_ALTERNATIVE)

	return results


def require_moments(values: NDArray[Any], needs_time_of_day: bool, function_name: str) -> None:
	"""
	Check that values are dates or datetimes, and datetimes when a time of day is needed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	needs_time_of_day
		True when the function reads or keeps hours, which dates do not have.
	function_name
		Name of the function, shown in the error message.

	Raises
	------
	IncompatibleTypesError
		When the values are not dates or datetimes, or are dates and a time of day is needed.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.time_function_values import require_moments
	>>> try:
	... 	require_moments(numpy.array(["2026-12-31"], dtype="datetime64[D]"), True, "DatePart")
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply DatePart to DATE.
	"""
	require_family(values, MOMENT_FAMILIES, function_name)
	values_type = from_numpy_dtype(values.dtype)
	misses_time_of_day = needs_time_of_day and values_type == Type.DATE
	if misses_time_of_day:
		raise IncompatibleTypesError(function_name, [values_type.name])


def read_date_parts(values: NDArray[Any], unit: DatePartUnit, function_name: str) -> NDArray[numpy.float64]:
	"""
	Return a part of each date or datetime, as a decimal number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a date or datetime Array.
	unit
		The part to read.
	function_name
		Name of the function, shown in error messages.

	Returns
	-------
	NDArray[numpy.float64]
		The parts, NaN for a missing value.

	Raises
	------
	IncompatibleTypesError
		When the values are not dates or datetimes, or are dates and the part is a time of day.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.time_function_values import read_date_parts
	>>> read_date_parts(numpy.array(["2026-12-31", "NaT"], dtype="datetime64[D]"), ndp.DatePartUnit.WEEK, "DatePart")
	array([53., nan])
	"""
	needs_time_of_day = unit in TIME_OF_DAY_PARTS
	require_moments(values, needs_time_of_day, function_name)
	flat_values = values.ravel()
	moments = pandas.DatetimeIndex(flat_values)
	if unit == DatePartUnit.WEEK:
		iso_calendar = moments.isocalendar()
		iso_weeks = iso_calendar[ISO_WEEK_COLUMN]
		flat_parts = iso_weeks.to_numpy(dtype=numpy.float64, na_value=numpy.nan)
	elif unit == DatePartUnit.WEEKDAY:
		weekdays = numpy.asarray(moments.day_of_week, dtype=numpy.float64)
		flat_parts = weekdays + WEEKDAY_SHIFT
	else:
		part_attribute = PART_ATTRIBUTES[unit]
		parts = getattr(moments, part_attribute)
		flat_parts = numpy.asarray(parts, dtype=numpy.float64)

	shaped_parts = flat_parts.reshape(values.shape)
	# Some versions of the numpy stubs widen the decimals of the reshaped parts.
	date_parts = cast(NDArray[numpy.float64], shaped_parts)

	return date_parts


def find_date_periods(values: NDArray[Any], unit: PeriodUnit, function_name: str) -> NDArray[Any]:
	"""
	Return the first moment of the period holding each date or datetime.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a date or datetime Array.
	unit
		The length of the periods.
	function_name
		Name of the function, shown in error messages.

	Returns
	-------
	NDArray
		Dates, or datetimes for ``PeriodUnit.HOUR``, NaT for a missing value.

	Raises
	------
	IncompatibleTypesError
		When the values are not dates or datetimes, or are dates and the unit is the hour.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.time_function_values import find_date_periods
	>>> find_date_periods(numpy.array(["2026-12-31"], dtype="datetime64[D]"), ndp.PeriodUnit.WEEK, "DatePeriod")
	array(['2026-12-28'], dtype='datetime64[D]')
	"""
	needs_time_of_day = unit == PeriodUnit.HOUR
	require_moments(values, needs_time_of_day, function_name)
	flat_values = values.ravel()
	moments = pandas.DatetimeIndex(flat_values)
	frequency = PERIOD_FREQUENCIES[unit]
	periods = moments.to_period(frequency)
	period_starts = periods.start_time
	result_type = Type.DATE
	if needs_time_of_day:
		result_type = Type.DATETIME

	result_dtype = to_numpy_dtype(result_type)
	flat_starts = period_starts.to_numpy(dtype=result_dtype)
	date_periods = flat_starts.reshape(values.shape)

	return date_periods


def count_durations(values: NDArray[Any], unit: DurationUnit, function_name: str) -> NDArray[numpy.float64]:
	"""
	Return each duration counted in a unit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a duration Array.
	unit
		The unit to count in.
	function_name
		Name of the function, shown in error messages.

	Returns
	-------
	NDArray[numpy.float64]
		The number of units of each duration, NaN for a missing value.

	Raises
	------
	IncompatibleTypesError
		When the values are not durations.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.time_function_values import count_durations
	>>> count_durations(numpy.array([36], dtype="timedelta64[h]"), ndp.DurationUnit.DAY, "DurationIn")
	array([1.5])
	"""
	require_family(values, DURATION_FAMILIES, function_name)
	unit_code = DURATION_UNIT_CODES[unit]
	one_unit = numpy.timedelta64(1, unit_code)
	counts = numpy.divide(values, one_unit, dtype=numpy.float64)

	return counts


def build_durations(values: NDArray[Any], unit: DurationUnit, function_name: str) -> NDArray[numpy.timedelta64]:
	"""
	Return each number read as a duration in a unit, rounded to the nanosecond.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array.
	unit
		The unit of the numbers.
	function_name
		Name of the function, shown in error messages.

	Returns
	-------
	NDArray[numpy.timedelta64]
		Durations in nanoseconds, NaT for a missing value.

	Raises
	------
	IncompatibleTypesError
		When the values are not numbers.
	TimeOverflowError
		When a duration is outside the range of nanoseconds, about 292 years.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.time_function_values import build_durations
	>>> build_durations(numpy.array([1.5, numpy.nan]), ndp.DurationUnit.DAY, "ToDuration")
	array([129600000000000,           'NaT'], dtype='timedelta64[ns]')
	"""
	require_family(values, NUMBER_FAMILIES, function_name)
	unit_code = DURATION_UNIT_CODES[unit]
	one_unit = numpy.timedelta64(1, unit_code)
	one_nanosecond = numpy.timedelta64(1, NANOSECOND_CODE)
	unit_ratio = one_unit // one_nanosecond
	nanoseconds_per_unit = int(unit_ratio)
	duration_dtype = to_numpy_dtype(Type.DURATION)
	if values.dtype.kind in WHOLE_NUMBER_KINDS:
		require_whole_durations_fit(values, nanoseconds_per_unit, function_name)
		whole_values = values.astype(numpy.int64)
		whole_nanoseconds = whole_values * nanoseconds_per_unit
		whole_durations = whole_nanoseconds.astype(duration_dtype)
		return whole_durations

	missing = numpy.isnan(values)
	decimal_nanoseconds = values * nanoseconds_per_unit
	require_decimal_durations_fit(decimal_nanoseconds, function_name)
	rounded_nanoseconds = numpy.round(decimal_nanoseconds)
	present_nanoseconds = numpy.where(missing, 0, rounded_nanoseconds)
	nanosecond_counts = present_nanoseconds.astype(numpy.int64)
	durations = nanosecond_counts.astype(duration_dtype)
	durations[missing] = numpy.timedelta64(NOT_A_TIME, NANOSECOND_CODE)

	return durations
