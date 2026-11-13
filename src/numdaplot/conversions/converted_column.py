"""
Conversion of a Table column to another type.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.brackets.bracketed_column import cut_column
from numdaplot.brackets.brackets import Brackets
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import find_column_type
from numdaplot.column_storage.frame_normalization import convert_to_type
from numdaplot.conversions.boolean_conversion import convert_booleans_to_numbers, convert_numbers_to_booleans
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.conversions.conversion_checks import WRITTEN_TYPES, require_conversion_settings
from numdaplot.conversions.conversion_settings import ConversionSettings
from numdaplot.conversions.date_conversion import convert_moments, write_dates, write_durations
from numdaplot.conversions.date_reading import parse_dates
from numdaplot.conversions.number_conversion import convert_numbers, parse_numbers
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.conversions.text_conversion import parse_booleans
from numdaplot.conversions.time_conversion import keep_time_of_day, parse_times, write_times
from numdaplot.conversions.time_zone_conversion import change_time_zone
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.types.type import Type
from numdaplot.types.value_family import ValueFamily, find_family

CONVERT_OPERATION = "convert"
WRITABLE_FAMILIES = frozenset({ValueFamily.NUMBER, ValueFamily.BOOL, ValueFamily.TEXT})
DEFAULT_BOOLEAN_RULE = BooleanRule.ZERO_ONE
NUMBERS_TO_NUMBERS = (ValueFamily.NUMBER, ValueFamily.NUMBER)
TEXTS_TO_NUMBERS = (ValueFamily.TEXT, ValueFamily.NUMBER)
TEXTS_TO_BOOLEANS = (ValueFamily.TEXT, ValueFamily.BOOL)
BOOLEANS_TO_NUMBERS = (ValueFamily.BOOL, ValueFamily.NUMBER)
NUMBERS_TO_BOOLEANS = (ValueFamily.NUMBER, ValueFamily.BOOL)


def convert_column(column: Column, conversion: ConversionSettings) -> Column:
	"""
	Return a Table column converted to another type, missing values staying missing.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an ``ArrayConversion``, which converts the values of an Array placed in a column.

	Parameters
	----------
	column
		A Table column.
	conversion
		The new type, and the date format, the time zone change or the rule reading numbers as booleans.

	Returns
	-------
	Column
		The converted column, or a copy when it already has the type. Numbers, booleans and categories
		become texts as Python writes them, such as ``2.5`` or ``True``.

	Raises
	------
	InvalidConversionError
		When the format, the time zone change or the boolean rule does not apply to the conversion.
	InvalidLimitsError
		When brackets cut integers and a bracket between two limits holds no integer.
	UnmatchedValueError
		When a number is in no bracket and the brackets keep ``others=Unmatched.ERROR``.
	IncompatibleTypesError
		When the conversion is not accepted, such as a boolean to a date, or a number to a date.
	ValueConversionError
		When a value cannot be stored in the new type without losing information.
	TimeOverflowError
		When a date read or converted is outside what the new type can hold.
	TimeZoneMismatchError
		When the time zone change does not apply to whether the datetimes have a zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_column import convert_column
	>>> texts = pandas.Series(["1", None, "3"], dtype="string")
	>>> convert_column(texts, ndp.TableConversion(columns=["count"], dtype=ndp.Type.INT64)).tolist()
	[1, <NA>, 3]
	"""
	source_type = find_column_type(column)
	require_conversion_settings(source_type, conversion)
	zone_change = conversion.timezone if isinstance(conversion, TableConversion) else None
	if zone_change is not None:
		zone_column = change_time_zone(column, zone_change)
		return zone_column

	if isinstance(conversion.format, Brackets):
		bracketed_column = cut_column(column, conversion.format)
		return bracketed_column

	if source_type == conversion.dtype:
		column_copy = column.copy()
		return column_copy

	try:
		time_column = convert_time_column(column, source_type, conversion.dtype, conversion.format)
	except pandas.errors.OutOfBoundsDatetime as error:
		raise TimeOverflowError(CONVERT_OPERATION, conversion.dtype.name) from error

	if time_column is not None:
		return time_column

	plain_column = convert_plain_column(column, source_type, conversion)

	return plain_column


def convert_time_column(
	column: Column, source_type: Type, target_type: Type, date_format: DateFormat | CustomDateFormat | None
) -> Column | None:
	"""
	Return a column converted between texts, dates, datetimes and durations.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of another type than the target.
	source_type
		The type of the column.
	target_type
		The new type.
	date_format
		How dates are written as texts, the default format when None.

	Returns
	-------
	Column or None
		The converted column, or ``None`` when the conversion involves no date, datetime or duration.

	Raises
	------
	ValueConversionError
		At the first text that is not a date in the format.
	TimeOverflowError
		When a text holds a real date that the version of pandas in use cannot read.
	OutOfBoundsDatetime
		When pandas cannot store a date as ``DATETIME``, outside the range of nanoseconds.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_column import convert_time_column
	>>> texts = pandas.Series(["2026-12-31"], dtype="string")
	>>> convert_time_column(texts, ndp.Type.TEXT, ndp.Type.DATE, None).tolist()
	[Timestamp('2026-12-31 00:00:00')]
	"""
	converts_times = Type.TIME in (source_type, target_type)
	if converts_times:
		time_column = convert_times(column, source_type, target_type, date_format)
		return time_column

	source_family = find_family(source_type)
	target_family = find_family(target_type)
	if source_family == ValueFamily.TEXT and target_family == ValueFamily.MOMENT:
		dates = parse_dates(column, target_type, date_format)
		return dates

	if source_family == ValueFamily.MOMENT and target_family == ValueFamily.MOMENT:
		moments = convert_moments(column, target_type)
		return moments

	is_written = target_type in WRITTEN_TYPES
	if not is_written:
		return None

	if source_family == ValueFamily.MOMENT:
		date_texts = write_dates(column, date_format)
		written_dates = convert_to_type(date_texts, target_type)
		return written_dates

	if source_family == ValueFamily.DURATION:
		duration_texts = write_durations(column)
		written_durations = convert_to_type(duration_texts, target_type)
		return written_durations

	return None


def convert_times(
	column: Column, source_type: Type, target_type: Type, time_format: DateFormat | CustomDateFormat | None
) -> Column | None:
	"""
	Return a column converted from texts or datetimes to times of day, or from times of day to texts or categories.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of another type than the target, one of the two types being ``TIME``.
	source_type
		The type of the column.
	target_type
		The new type.
	time_format
		A pattern of a time without date, already checked, or None for the default format.

	Returns
	-------
	Column or None
		The converted column, or ``None`` for a conversion of times of day that is not accepted.

	Raises
	------
	ValueConversionError
		At the first text that is not a time in the format.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_column import convert_times
	>>> moments = pandas.Series(pandas.to_datetime(["2026-03-14 15:35"]))
	>>> convert_times(moments, ndp.Type.DATETIME, ndp.Type.TIME, None).tolist()
	[Timedelta('0 days 15:35:00')]
	"""
	custom_format = time_format if isinstance(time_format, CustomDateFormat) else None
	source_family = find_family(source_type)
	if source_family == ValueFamily.TEXT and target_type == Type.TIME:
		read_times = parse_times(column, custom_format)
		return read_times

	if source_type == Type.DATETIME and target_type == Type.TIME:
		day_times = keep_time_of_day(column)
		return day_times

	if source_type == Type.TIME and target_type in WRITTEN_TYPES:
		time_texts = write_times(column, custom_format)
		written_times = convert_to_type(time_texts, target_type)
		return written_times

	return None


def convert_plain_column(column: Column, source_type: Type, conversion: ConversionSettings) -> Column:
	"""
	Return a column converted between numbers, booleans, texts and categories.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an ``ArrayConversion``.

	Parameters
	----------
	column
		A Table column of another type than the target.
	source_type
		The type of the column.
	conversion
		The new type and the rule reading numbers as booleans.

	Returns
	-------
	Column
		The converted column.

	Raises
	------
	IncompatibleTypesError
		When the conversion is not accepted, such as a boolean to a date.
	ValueConversionError
		When a value cannot be stored in the new type without losing information.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_column import convert_plain_column
	>>> to_text = ndp.TableConversion(columns=["price"], dtype=ndp.Type.TEXT)
	>>> convert_plain_column(pandas.Series([1.5]), ndp.Type.FLOAT64, to_text).tolist()
	['1.5']
	"""
	target_type = conversion.dtype
	if target_type in WRITTEN_TYPES:
		written_column = write_plain_column(column, source_type, target_type)
		return written_column

	read_column = read_plain_column(column, source_type, conversion)

	return read_column


def write_plain_column(column: Column, source_type: Type, target_type: Type) -> Column:
	"""
	Return a column of numbers, booleans, texts or categories written as texts or categories.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of another type than the target.
	source_type
		The type of the column.
	target_type
		``TEXT`` or ``CATEGORY``.

	Returns
	-------
	Column
		The column written as Python writes each value, such as ``2.5`` or ``True``.

	Raises
	------
	IncompatibleTypesError
		When the column holds other values than numbers, booleans, texts or categories.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_column import write_plain_column
	>>> write_plain_column(pandas.Series([True]), ndp.Type.BOOL, ndp.Type.CATEGORY).tolist()
	['True']
	"""
	source_family = find_family(source_type)
	if source_family not in WRITABLE_FAMILIES:
		type_names = [source_type.name, target_type.name]
		raise IncompatibleTypesError(CONVERT_OPERATION, type_names)

	text_column = convert_to_type(column, Type.TEXT)
	if target_type == Type.CATEGORY:
		category_column = convert_to_type(text_column, Type.CATEGORY)
		return category_column

	return text_column


def read_plain_column(column: Column, source_type: Type, conversion: ConversionSettings) -> Column:
	"""
	Return a column of numbers, booleans, texts or categories converted to numbers or booleans.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an ``ArrayConversion``.

	Parameters
	----------
	column
		A Table column of another type than the target.
	source_type
		The type of the column.
	conversion
		The new type, a number type or ``BOOL``, and the rule reading numbers as booleans.

	Returns
	-------
	Column
		The converted column.

	Raises
	------
	IncompatibleTypesError
		When the conversion is not accepted, such as a boolean to a date.
	ValueConversionError
		When a value cannot be stored in the new type without losing information.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_column import read_plain_column
	>>> to_integers = ndp.TableConversion(columns=["paid"], dtype=ndp.Type.INT64)
	>>> read_plain_column(pandas.Series([True, False]), ndp.Type.BOOL, to_integers).tolist()
	[1, 0]
	"""
	target_type = conversion.dtype
	source_family = find_family(source_type)
	target_family = find_family(target_type)
	family_pair = (source_family, target_family)
	if family_pair == NUMBERS_TO_NUMBERS:
		number_column = convert_numbers(column, target_type)
		return number_column

	if family_pair == TEXTS_TO_NUMBERS:
		parsed_column = parse_numbers(column, target_type)
		return parsed_column

	if family_pair == TEXTS_TO_BOOLEANS:
		boolean_column = parse_booleans(column)
		return boolean_column

	if family_pair == BOOLEANS_TO_NUMBERS:
		boolean_numbers = convert_booleans_to_numbers(column, target_type)
		return boolean_numbers

	if family_pair == NUMBERS_TO_BOOLEANS:
		boolean_rule = conversion.booleans
		if boolean_rule is None:
			boolean_rule = DEFAULT_BOOLEAN_RULE

		number_booleans = convert_numbers_to_booleans(column, boolean_rule)
		return number_booleans

	type_names = [source_type.name, target_type.name]
	raise IncompatibleTypesError(CONVERT_OPERATION, type_names)
