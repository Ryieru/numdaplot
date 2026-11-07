"""
Conversion of a Table column to another type.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.invalid_conversion_error import InvalidConversionError
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.tables.columns.boolean_conversion import convert_booleans_to_numbers, convert_numbers_to_booleans
from numdaplot.tables.columns.boolean_rule import BooleanRule
from numdaplot.tables.columns.conversion import Conversion
from numdaplot.tables.columns.date_conversion import (
	convert_moments,
	find_format_name,
	has_time,
	parse_dates,
	write_dates,
	write_durations,
)
from numdaplot.tables.columns.number_conversion import convert_numbers, parse_numbers
from numdaplot.tables.columns.text_conversion import parse_booleans
from numdaplot.tables.columns.time_zone_conversion import change_time_zone
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.frame_normalization import convert_to_type

CONVERT_OPERATION = "convert"
WRITABLE_FAMILIES = frozenset({ValueFamily.NUMBER, ValueFamily.BOOL, ValueFamily.TEXT})
WRITTEN_TYPES = frozenset({Type.TEXT, Type.CATEGORY})
FORMAT_SETTING = "format"
TIMEZONE_SETTING = "timezone"
BOOLEANS_SETTING = "booleans"
DEFAULT_BOOLEAN_RULE = BooleanRule.ZERO_ONE
NUMBERS_TO_NUMBERS = (ValueFamily.NUMBER, ValueFamily.NUMBER)
TEXTS_TO_NUMBERS = (ValueFamily.TEXT, ValueFamily.NUMBER)
TEXTS_TO_BOOLEANS = (ValueFamily.TEXT, ValueFamily.BOOL)
BOOLEANS_TO_NUMBERS = (ValueFamily.BOOL, ValueFamily.NUMBER)
NUMBERS_TO_BOOLEANS = (ValueFamily.NUMBER, ValueFamily.BOOL)


def convert_column(column: Column, conversion: Conversion) -> Column:
	"""
	Return a Table column converted to another type, missing values staying missing.

	.. versionadded:: 0.1.0

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
	>>> from numdaplot.tables.columns.converted_column import convert_column
	>>> texts = pandas.Series(["1", None, "3"], dtype="string")
	>>> convert_column(texts, ndp.Conversion(column="count", dtype=ndp.Type.INT64)).tolist()
	[1, <NA>, 3]
	"""
	source_type = find_column_type(column)
	require_conversion_settings(source_type, conversion)
	if conversion.timezone is not None:
		zone_column = change_time_zone(column, conversion.timezone)
		return zone_column

	if source_type == conversion.dtype:
		column_copy = column.copy()
		return column_copy

	try:
		time_column = convert_time_column(column, source_type, conversion)
	except pandas.errors.OutOfBoundsDatetime as error:
		raise TimeOverflowError(CONVERT_OPERATION, conversion.dtype.name) from error

	if time_column is not None:
		return time_column

	plain_column = convert_plain_column(column, source_type, conversion)

	return plain_column


def require_conversion_settings(source_type: Type, conversion: Conversion) -> None:
	"""
	Check that the format, the time zone change and the boolean rule of a conversion apply to its types.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	conversion
		The new type and the settings.

	Raises
	------
	InvalidConversionError
		When a time zone change is given to another conversion than datetimes to datetimes, a format to another
		conversion than texts to dates or dates to texts, a format with a time to dates, or a boolean rule to another
		conversion than numbers to booleans.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.converted_column import require_conversion_settings
	>>> day_and_time = ndp.Conversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR_TIME)
	>>> try:
	... 	require_conversion_settings(ndp.Type.TEXT, day_and_time)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The format DAY_MONTH_YEAR_TIME has a time, which DATE cannot hold.
	Convert the column to DATETIME first, then to DATE.
	"""
	require_time_zone_setting(source_type, conversion)
	require_format_setting(source_type, conversion)
	require_booleans_setting(source_type, conversion)


def require_time_zone_setting(source_type: Type, conversion: Conversion) -> None:
	"""
	Check that a time zone change, when given, is given to a conversion of datetimes to datetimes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	conversion
		The new type and the settings.

	Raises
	------
	InvalidConversionError
		When a time zone change is given to another conversion.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.converted_column import require_time_zone_setting
	>>> to_paris = ndp.TimeZoneChange(zone=ndp.TimeZone("Europe/Paris"), mode=ndp.TimeZoneMode.ATTRIBUTE)
	>>> zone_change = ndp.Conversion(column="day", dtype=ndp.Type.DATETIME, timezone=to_paris)
	>>> try:
	... 	require_time_zone_setting(ndp.Type.TEXT, zone_change)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The setting timezone does not apply to a conversion from TEXT to DATETIME.
	"""
	if conversion.timezone is None:
		return

	target_type = conversion.dtype
	changes_datetimes = source_type == Type.DATETIME and target_type == Type.DATETIME
	if not changes_datetimes:
		raise InvalidConversionError(TIMEZONE_SETTING, source_type.name, target_type.name)


def require_format_setting(source_type: Type, conversion: Conversion) -> None:
	"""
	Check that a date format, when given, is given to a conversion of texts to dates or of dates to texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	conversion
		The new type and the settings.

	Raises
	------
	InvalidConversionError
		When a format is given to another conversion, or a format with a time to dates.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.converted_column import require_format_setting
	>>> day_first = ndp.DateFormat.DAY_MONTH_YEAR
	>>> price_texts = ndp.Conversion(column="price", dtype=ndp.Type.TEXT, format=day_first)
	>>> try:
	... 	require_format_setting(ndp.Type.FLOAT64, price_texts)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The setting format does not apply to a conversion from FLOAT64 to TEXT.
	"""
	if conversion.format is None:
		return

	target_type = conversion.dtype
	source_family = find_family(source_type)
	target_family = find_family(target_type)
	reads_dates = source_family == ValueFamily.TEXT and target_family == ValueFamily.MOMENT
	writes_dates = source_family == ValueFamily.MOMENT and target_type in WRITTEN_TYPES
	date_type = source_type
	if reads_dates:
		date_type = target_type

	format_has_time = has_time(conversion.format)
	misses_time = date_type == Type.DATE and format_has_time
	uses_format = reads_dates or writes_dates
	if not uses_format:
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name)

	if misses_time:
		format_name = find_format_name(target_type, conversion.format)
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name, format_name)


def require_booleans_setting(source_type: Type, conversion: Conversion) -> None:
	"""
	Check that a boolean rule, when given, is given to a conversion of numbers to booleans.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	conversion
		The new type and the settings.

	Raises
	------
	InvalidConversionError
		When a boolean rule is given to another conversion.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.converted_column import require_booleans_setting
	>>> rule = ndp.BooleanRule.NONZERO_TRUE
	>>> try:
	... 	require_booleans_setting(ndp.Type.TEXT, ndp.Conversion(column="paid", dtype=ndp.Type.BOOL, booleans=rule))
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The setting booleans does not apply to a conversion from TEXT to BOOL.
	"""
	if conversion.booleans is None:
		return

	target_type = conversion.dtype
	source_family = find_family(source_type)
	reads_numbers = source_family == ValueFamily.NUMBER and target_type == Type.BOOL
	if not reads_numbers:
		raise InvalidConversionError(BOOLEANS_SETTING, source_type.name, target_type.name)


def convert_time_column(column: Column, source_type: Type, conversion: Conversion) -> Column | None:
	"""
	Return a column converted between texts, dates, datetimes and durations.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of another type than the target.
	source_type
		The type of the column.
	conversion
		The new type and the date format.

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
	>>> from numdaplot.tables.columns.converted_column import convert_time_column
	>>> texts = pandas.Series(["2026-12-31"], dtype="string")
	>>> convert_time_column(texts, ndp.Type.TEXT, ndp.Conversion(column="day", dtype=ndp.Type.DATE)).tolist()
	[Timestamp('2026-12-31 00:00:00')]
	"""
	target_type = conversion.dtype
	source_family = find_family(source_type)
	target_family = find_family(target_type)
	if source_family == ValueFamily.TEXT and target_family == ValueFamily.MOMENT:
		dates = parse_dates(column, target_type, conversion.format)
		return dates

	if source_family == ValueFamily.MOMENT and target_family == ValueFamily.MOMENT:
		moments = convert_moments(column, target_type)
		return moments

	is_written = target_type in WRITTEN_TYPES
	if not is_written:
		return None

	if source_family == ValueFamily.MOMENT:
		date_texts = write_dates(column, conversion.format)
		written_dates = convert_to_type(date_texts, target_type)
		return written_dates

	if source_family == ValueFamily.DURATION:
		duration_texts = write_durations(column)
		written_durations = convert_to_type(duration_texts, target_type)
		return written_durations

	return None


def convert_plain_column(column: Column, source_type: Type, conversion: Conversion) -> Column:
	"""
	Return a column converted between numbers, booleans, texts and categories.

	.. versionadded:: 0.1.0

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
	>>> from numdaplot.tables.columns.converted_column import convert_plain_column
	>>> to_text = ndp.Conversion(column="price", dtype=ndp.Type.TEXT)
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
	>>> from numdaplot.tables.columns.converted_column import write_plain_column
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


def read_plain_column(column: Column, source_type: Type, conversion: Conversion) -> Column:
	"""
	Return a column of numbers, booleans, texts or categories converted to numbers or booleans.

	.. versionadded:: 0.1.0

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
	>>> from numdaplot.tables.columns.converted_column import read_plain_column
	>>> to_integers = ndp.Conversion(column="paid", dtype=ndp.Type.INT64)
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
