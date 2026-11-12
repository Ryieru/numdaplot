"""
Checks of the settings of a conversion against the types it converts between.

.. versionadded:: 0.2.0
"""

from numdaplot.conversions.conversion_settings import ConversionSettings
from numdaplot.conversions.date_formats import find_format_name, has_date, has_time
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.invalid_conversion_error import InvalidConversionError
from numdaplot.tables.columns.brackets import Brackets

WRITTEN_TYPES = frozenset({Type.TEXT, Type.CATEGORY})
FORMAT_SETTING = "format"
TIMEZONE_SETTING = "timezone"
BOOLEANS_SETTING = "booleans"


def require_conversion_settings(source_type: Type, conversion: ConversionSettings) -> None:
	"""
	Check that the format, the time zone change and the boolean rule of a conversion apply to its types.

	Only the conversion of a Table column has a time zone change.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an ``ArrayConversion``, which has no time zone change.

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
	>>> from numdaplot.conversions.conversion_checks import require_conversion_settings
	>>> day_and_time = ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR_TIME)
	>>> try:
	... 	require_conversion_settings(ndp.Type.TEXT, day_and_time)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The format DAY_MONTH_YEAR_TIME has a time, which DATE cannot hold.
	Convert the values to DATETIME first, then to DATE.
	"""
	if isinstance(conversion, TableConversion):
		require_time_zone_setting(source_type, conversion)

	require_format_setting(source_type, conversion)
	require_booleans_setting(source_type, conversion)


def require_time_zone_setting(source_type: Type, conversion: TableConversion) -> None:
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
	>>> from numdaplot.conversions.conversion_checks import require_time_zone_setting
	>>> to_paris = ndp.TimeZoneChange(zone=ndp.TimeZone("Europe/Paris"), mode=ndp.TimeZoneMode.ATTRIBUTE)
	>>> zone_change = ndp.TableConversion(column="day", dtype=ndp.Type.DATETIME, timezone=to_paris)
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


def require_format_setting(source_type: Type, conversion: ConversionSettings) -> None:
	"""
	Check that a date format, when given, is given to a conversion of texts to dates or of dates to texts.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an ``ArrayConversion``.

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
	>>> from numdaplot.conversions.conversion_checks import require_format_setting
	>>> day_first = ndp.DateFormat.DAY_MONTH_YEAR
	>>> price_texts = ndp.TableConversion(column="price", dtype=ndp.Type.TEXT, format=day_first)
	>>> try:
	... 	require_format_setting(ndp.Type.FLOAT64, price_texts)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The setting format does not apply to a conversion from FLOAT64 to TEXT.
	"""
	if conversion.format is None:
		return

	if isinstance(conversion.format, Brackets):
		require_brackets_setting(source_type, conversion.dtype)
		return

	converts_times = Type.TIME in (source_type, conversion.dtype)
	if converts_times:
		require_time_format_setting(source_type, conversion.dtype, conversion.format)
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
	format_has_date = has_date(conversion.format)
	misses_time = date_type == Type.DATE and format_has_time
	uses_format = reads_dates or writes_dates
	if not uses_format or not format_has_date:
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name)

	if misses_time:
		format_name = find_format_name(target_type, conversion.format)
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name, format_name)


def require_time_format_setting(
	source_type: Type, target_type: Type, time_format: DateFormat | CustomDateFormat
) -> None:
	"""
	Check that a format given to a conversion of times of day reads or writes them, and holds no date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	target_type
		The new type, ``TIME`` or the type a ``TIME`` column is converted to.
	time_format
		The format given.

	Raises
	------
	InvalidConversionError
		When the conversion neither reads texts as times nor writes times as texts, or the format holds a date.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.conversion_checks import require_time_format_setting
	>>> try:
	... 	require_time_format_setting(ndp.Type.TEXT, ndp.Type.TIME, ndp.DateFormat.DAY_MONTH_YEAR)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The format DAY_MONTH_YEAR has a date, which TIME cannot hold.
	Give a CustomDateFormat of a time only, such as "%H:%M".
	"""
	source_family = find_family(source_type)
	reads_times = source_family == ValueFamily.TEXT and target_type == Type.TIME
	writes_times = source_type == Type.TIME and target_type in WRITTEN_TYPES
	uses_format = reads_times or writes_times
	if not uses_format:
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name)

	format_has_date = has_date(time_format)
	if format_has_date:
		format_name = find_format_name(target_type, time_format)
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name, format_name)


def require_brackets_setting(source_type: Type, target_type: Type) -> None:
	"""
	Check that brackets are given to a conversion of numbers to categories.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	target_type
		The new type.

	Raises
	------
	InvalidConversionError
		When the column does not hold numbers, or the new type is not ``CATEGORY``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.conversion_checks import require_brackets_setting
	>>> try:
	... 	require_brackets_setting(ndp.Type.TEXT, ndp.Type.CATEGORY)
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The setting format does not apply to a conversion from TEXT to CATEGORY.
	"""
	source_family = find_family(source_type)
	cuts_numbers = source_family == ValueFamily.NUMBER and target_type == Type.CATEGORY
	if not cuts_numbers:
		raise InvalidConversionError(FORMAT_SETTING, source_type.name, target_type.name)


def require_booleans_setting(source_type: Type, conversion: ConversionSettings) -> None:
	"""
	Check that a boolean rule, when given, is given to a conversion of numbers to booleans.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an ``ArrayConversion``.

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
	>>> from numdaplot.conversions.conversion_checks import require_booleans_setting
	>>> rule = ndp.BooleanRule.NONZERO_TRUE
	>>> to_booleans = ndp.TableConversion(column="paid", dtype=ndp.Type.BOOL, booleans=rule)
	>>> try:
	... 	require_booleans_setting(ndp.Type.TEXT, to_booleans)
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
