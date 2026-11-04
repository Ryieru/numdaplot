"""
Texts of datetimes and durations shown for an Array.

.. versionadded:: 0.1.0
"""

from typing import Any, Literal, cast

import numpy
from numpy.typing import NDArray

type DatetimeUnit = Literal["s", "ms", "us", "ns"]
DATETIME_UNITS = tuple[DatetimeUnit, ...](("s", "ms", "us", "ns"))
ISO_TIME_SEPARATOR = "T"
TIME_SEPARATOR = " "
NOT_A_TIME_TEXT = "NaT"
NANOSECONDS_PER_SECOND = 1_000_000_000
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3_600
SECONDS_PER_DAY = 86_400
NANOSECOND_DIGITS = 9
CLOCK_DIGITS = 2
DAYS_SUFFIX = " days "
CLOCK_SEPARATOR = ":"
FRACTION_SEPARATOR = "."
NEGATIVE_CLOCK_SIGN = "+"
NANOSECOND_DTYPE = "timedelta64[ns]"


def format_datetimes(values: NDArray[numpy.datetime64]) -> NDArray[numpy.str_]:
	"""
	Return the text of each datetime, such as ``2026-01-02 10:30:00``.

	Fractions of a second are written only when a value has one, with the same number of digits for every value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a datetime Array.

	Returns
	-------
	NDArray[numpy.str_]
		One text per value, of the same shape, ``NaT`` for a missing value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.time_text import format_datetimes
	>>> format_datetimes(numpy.array(["2026-01-02T10:30:00.25", "NaT"], dtype="datetime64[ns]")).tolist()
	['2026-01-02 10:30:00.250', 'NaT']
	"""
	unit = find_datetime_unit(values)
	iso_texts = numpy.datetime_as_string(values, unit=unit)
	spaced_texts = numpy.strings.replace(iso_texts, ISO_TIME_SEPARATOR, TIME_SEPARATOR)
	missing = numpy.isnat(values)
	datetime_texts = numpy.where(missing, NOT_A_TIME_TEXT, spaced_texts)

	return datetime_texts


def find_datetime_unit(values: NDArray[numpy.datetime64]) -> DatetimeUnit:
	"""
	Return the shortest unit, from the second to the nanosecond, that writes every datetime exactly.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a datetime Array.

	Returns
	-------
	DatetimeUnit
		A numpy unit code: ``"s"``, ``"ms"``, ``"us"`` or ``"ns"``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.time_text import find_datetime_unit
	>>> find_datetime_unit(numpy.array(["2026-01-02T10:30:00.25"], dtype="datetime64[ns]"))
	'ms'
	"""
	present = ~numpy.isnat(values)
	present_values = values[present]

	for unit in DATETIME_UNITS:
		unit_dtype = numpy.dtype(f"datetime64[{unit}]")
		truncated_values = present_values.astype(unit_dtype)
		is_exact = bool(numpy.all(truncated_values == present_values))
		if is_exact:
			return unit

	finest_unit = DATETIME_UNITS[-1]

	return finest_unit


def format_durations(values: NDArray[numpy.timedelta64]) -> NDArray[numpy.str_]:
	"""
	Return the text of each duration as pandas writes it, such as ``1 days 12:00:00``.

	A negative duration counts whole days down, then the time up: 12 hours less is ``-1 days +12:00:00``.
	Fractions of a second are written with nine digits, only for the values that have one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a duration Array.

	Returns
	-------
	NDArray[numpy.str_]
		One text per value, of the same shape, ``NaT`` for a missing value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.time_text import format_durations
	>>> format_durations(numpy.array([36, -12], dtype="timedelta64[h]")).tolist()
	['1 days 12:00:00', '-1 days +12:00:00']
	"""
	nanosecond_values = values.astype(NANOSECOND_DTYPE)
	missing = numpy.isnat(nanosecond_values)
	nanoseconds = nanosecond_values.view(numpy.int64)
	whole_seconds, fractions = numpy.divmod(nanoseconds, NANOSECONDS_PER_SECOND)
	days, day_seconds = numpy.divmod(whole_seconds, SECONDS_PER_DAY)
	hours, hour_seconds = numpy.divmod(day_seconds, SECONDS_PER_HOUR)
	minutes, seconds = numpy.divmod(hour_seconds, SECONDS_PER_MINUTE)
	day_numbers = days.astype(str)
	day_texts = join_texts(day_numbers, DAYS_SUFFIX)
	negative = days < 0
	negative_day_texts = join_texts(day_texts, NEGATIVE_CLOCK_SIGN)
	signed_day_texts = numpy.where(negative, negative_day_texts, day_texts)
	clock_texts = join_clock_parts([hours, minutes, seconds])
	fraction_texts = format_fractions(fractions)
	whole_texts = join_texts(signed_day_texts, clock_texts)
	duration_texts = join_texts(whole_texts, fraction_texts)
	readable_texts = numpy.where(missing, NOT_A_TIME_TEXT, duration_texts)

	return readable_texts


def join_clock_parts(parts: list[NDArray[numpy.int64]]) -> NDArray[numpy.str_]:
	"""
	Return hours, minutes and seconds written with two digits each and joined by ``:``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	parts
		The hours, the minutes and the seconds, each with one number per value.

	Returns
	-------
	NDArray[numpy.str_]
		One text per value, such as ``12:05:00``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.time_text import join_clock_parts
	>>> join_clock_parts([numpy.array([12]), numpy.array([5]), numpy.array([0])]).tolist()
	['12:05:00']
	"""
	part_texts = list[NDArray[numpy.str_]]()

	for part in parts:
		number_texts = part.astype(str)
		part_text = numpy.strings.zfill(number_texts, CLOCK_DIGITS)
		part_texts.append(part_text)

	clock_texts = part_texts[0]

	for part_text in part_texts[1:]:
		separated_texts = join_texts(clock_texts, CLOCK_SEPARATOR)
		clock_texts = join_texts(separated_texts, part_text)

	return clock_texts


def format_fractions(fractions: NDArray[numpy.int64]) -> NDArray[Any]:
	"""
	Return the fraction of a second of each value, written with nine digits, or an empty text when there is none.

	.. versionadded:: 0.1.0

	Parameters
	----------
	fractions
		The nanoseconds of each value, from 0 to 999 999 999.

	Returns
	-------
	NDArray
		One text per value, such as ``.000001500`` or ``""``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.time_text import format_fractions
	>>> format_fractions(numpy.array([0, 1500])).tolist()
	['', '.000001500']
	"""
	number_texts = fractions.astype(str)
	digit_texts = numpy.strings.zfill(number_texts, NANOSECOND_DIGITS)
	fraction_texts = join_texts(FRACTION_SEPARATOR, digit_texts)
	has_fraction = fractions != 0
	shown_fractions = numpy.where(has_fraction, fraction_texts, "")

	return shown_fractions


def join_texts(left_texts: NDArray[Any] | str, right_texts: NDArray[Any] | str) -> NDArray[numpy.str_]:
	"""
	Return texts joined value by value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left_texts
		Texts, or a single text joined to every value.
	right_texts
		Texts, or a single text joined to every value.

	Returns
	-------
	NDArray[numpy.str_]
		Each left text followed by its right text.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.time_text import join_texts
	>>> join_texts(numpy.array(["1", "2"]), " days").tolist()
	['1 days', '2 days']
	"""
	# Some versions of the numpy stubs leave the types of numpy.strings.add partially unknown.
	string_functions = cast(Any, numpy.strings)
	joined_texts = string_functions.add(left_texts, right_texts)

	return joined_texts
