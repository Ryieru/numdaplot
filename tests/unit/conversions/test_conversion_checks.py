"""
Unit tests of the check of the format and the time zone change of a conversion.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.conversions.conversion_checks import (
	require_booleans_setting,
	require_brackets_setting,
	require_conversion_settings,
	require_format_setting,
	require_time_format_setting,
	require_time_zone_setting,
)
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.invalid_conversion_error import InvalidConversionError
from numdaplot.types.type import Type

CONVERTED_NAME = "value"
UTC_ZONE = TimeZone("UTC")
ATTRIBUTE_UTC = TimeZoneChange(mode=TimeZoneMode.ATTRIBUTE, zone=UTC_ZONE)
REJECTED_SETTINGS = [
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.INT64, format=DateFormat.DAY_MONTH_YEAR),
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATE, format=DateFormat.DAY_MONTH_YEAR_TIME),
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATETIME, timezone=ATTRIBUTE_UTC),
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.BOOL, booleans=BooleanRule.NONZERO_TRUE),
]
FORMAT_AND_ZONE = TableConversion(
	columns=[CONVERTED_NAME],
	dtype=Type.DATETIME,
	format=DateFormat.YEAR_MONTH_DAY_TIME,
	timezone=ATTRIBUTE_UTC,
)
ACCEPTED_SETTINGS = [
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATE, format=DateFormat.DAY_MONTH_YEAR),
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATETIME, format=DateFormat.DAY_MONTH_YEAR),
	TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATETIME, format=DateFormat.DAY_MONTH_YEAR_TIME),
]
TIME_FORMAT_ON_DATE = TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATE, format=DateFormat.YEAR_MONTH_DAY_TIME)
CUSTOM_TIME_ON_DATE = TableConversion(
	columns=[CONVERTED_NAME], dtype=Type.DATE, format=CustomDateFormat("%d/%m/%Y %H:%M")
)
TIME_FORMAT_WRITING_DATE = TableConversion(
	columns=[CONVERTED_NAME], dtype=Type.TEXT, format=DateFormat.YEAR_MONTH_DAY_TIME
)
EXPECTED_TIME_FORMAT_MESSAGE = (
	"The format YEAR_MONTH_DAY_TIME has a time, which DATE cannot hold. "
	"Convert the values to DATETIME first, then to DATE."
)
EXPECTED_CUSTOM_TIME_MESSAGE = (
	"The format %d/%m/%Y %H:%M has a time, which DATE cannot hold. Convert the values to DATETIME first, then to DATE."
)
EXPECTED_WRITING_MESSAGE = (
	"The format YEAR_MONTH_DAY_TIME has a time, which DATE cannot hold. "
	"Convert the values to DATETIME first, then to TEXT."
)
TIME_FORMAT_ON_DATE_TO_INTEGER = TableConversion(
	columns=[CONVERTED_NAME], dtype=Type.INT64, format=DateFormat.YEAR_MONTH_DAY_TIME
)
EXPECTED_GENERAL_MESSAGE = "The setting format does not apply to a conversion from DATE to INT64."
ARRAY_TIME_FORMAT_TO_INTEGER = ArrayConversion(dtype=Type.INT64, format=DateFormat.YEAR_MONTH_DAY_TIME)
ARRAY_PLAIN_CONVERSION = ArrayConversion(dtype=Type.INT64)
NONZERO_TO_BOOLEANS = TableConversion(columns=[CONVERTED_NAME], dtype=Type.BOOL, booleans=BooleanRule.NONZERO_TRUE)
NONZERO_TO_INTEGERS = TableConversion(columns=[CONVERTED_NAME], dtype=Type.INT64, booleans=BooleanRule.NONZERO_TRUE)
PLAIN_TO_BOOLEANS = TableConversion(columns=[CONVERTED_NAME], dtype=Type.BOOL)
EXPECTED_BOOLEANS_MESSAGE = "The setting booleans does not apply to a conversion from TEXT to BOOL."
TIME_PATTERN = CustomDateFormat("%H:%M")
DATE_PATTERN = CustomDateFormat("%d/%m/%Y")


@pytest.mark.parametrize("conversion", REJECTED_SETTINGS)
def test_require_conversion_settings_rejects_a_setting_that_does_not_apply(conversion: TableConversion) -> None:
	"""
	Check formats and time zone changes given to conversions they do not apply to.

	.. versionadded:: 0.1.0

	Parameters
	----------
	conversion
		A conversion with a setting that does not apply to its types, the column being TEXT.
	"""
	with pytest.raises(InvalidConversionError):
		require_conversion_settings(Type.TEXT, conversion)


def test_require_conversion_settings_rejects_a_format_on_datetimes_changing_zone() -> None:
	"""
	Check that a format next to a time zone change raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidConversionError):
		require_conversion_settings(Type.DATETIME, FORMAT_AND_ZONE)


@pytest.mark.parametrize("conversion", ACCEPTED_SETTINGS)
def test_require_conversion_settings_accepts_formats_reading_or_writing_dates(conversion: TableConversion) -> None:
	"""
	Check formats reading texts as dates.

	.. versionadded:: 0.1.0

	Parameters
	----------
	conversion
		A conversion of texts with a fitting format.
	"""
	require_conversion_settings(Type.TEXT, conversion)


@pytest.mark.parametrize("source_type", [Type.TEXT, Type.CATEGORY])
def test_require_conversion_settings_points_a_time_format_on_dates_to_datetimes(source_type: Type) -> None:
	"""
	Check that reading texts or categories as dates with a time format explains how to convert them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the texts read.
	"""
	with pytest.raises(InvalidConversionError) as caught_error:
		require_conversion_settings(source_type, TIME_FORMAT_ON_DATE)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_TIME_FORMAT_MESSAGE


def test_require_conversion_settings_shows_the_pattern_of_a_custom_time_format() -> None:
	"""
	Check that a custom format with a time read as dates is named by its pattern.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidConversionError) as caught_error:
		require_conversion_settings(Type.TEXT, CUSTOM_TIME_ON_DATE)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_CUSTOM_TIME_MESSAGE


def test_require_conversion_settings_points_writing_dates_with_a_time_format_to_datetimes() -> None:
	"""
	Check that writing dates with a time format explains how to convert them.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidConversionError) as caught_error:
		require_conversion_settings(Type.DATE, TIME_FORMAT_WRITING_DATE)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_WRITING_MESSAGE


def test_require_conversion_settings_keeps_the_general_message_when_no_format_applies() -> None:
	"""
	Check that a time format on a conversion that uses no format names the setting and the types.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidConversionError) as caught_error:
		require_conversion_settings(Type.DATE, TIME_FORMAT_ON_DATE_TO_INTEGER)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_GENERAL_MESSAGE


def test_require_conversion_settings_checks_the_format_of_an_array_conversion() -> None:
	"""
	Check that the settings of an Array, without time zone change, still have their format checked.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidConversionError) as error_info:
		require_conversion_settings(Type.DATE, ARRAY_TIME_FORMAT_TO_INTEGER)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_GENERAL_MESSAGE


def test_require_conversion_settings_accepts_an_array_conversion_without_setting() -> None:
	"""
	Check that the settings of an Array without format nor boolean rule are accepted.

	.. versionadded:: 0.2.0
	"""
	require_conversion_settings(Type.TEXT, ARRAY_PLAIN_CONVERSION)


@pytest.mark.parametrize("source_type", [Type.INT64, Type.UINT8, Type.FLOAT32])
def test_require_booleans_setting_accepts_numbers_read_as_booleans(source_type: Type) -> None:
	"""
	Check that a boolean rule given to a conversion of numbers to BOOL raises nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		A number type.
	"""
	require_booleans_setting(source_type, NONZERO_TO_BOOLEANS)


@pytest.mark.parametrize(
	("source_type", "conversion"),
	[
		(Type.TEXT, NONZERO_TO_BOOLEANS),
		(Type.BOOL, NONZERO_TO_BOOLEANS),
		(Type.FLOAT64, NONZERO_TO_INTEGERS),
	],
)
def test_require_booleans_setting_rejects_another_conversion(source_type: Type, conversion: TableConversion) -> None:
	"""
	Check that a boolean rule given to another conversion than numbers to BOOL raises InvalidConversionError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the converted column.
	conversion
		A conversion with a boolean rule.
	"""
	with pytest.raises(InvalidConversionError):
		require_booleans_setting(source_type, conversion)


def test_require_booleans_setting_names_the_setting_and_the_types() -> None:
	"""
	Check the message of a boolean rule that does not apply.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidConversionError) as error_info:
		require_booleans_setting(Type.TEXT, NONZERO_TO_BOOLEANS)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_BOOLEANS_MESSAGE


def test_require_booleans_setting_accepts_an_omitted_rule() -> None:
	"""
	Check that a conversion without boolean rule raises nothing, whatever its types.

	.. versionadded:: 0.1.0
	"""
	require_booleans_setting(Type.TEXT, PLAIN_TO_BOOLEANS)


def test_require_time_zone_setting_rejects_a_change_of_texts() -> None:
	"""
	Check that a time zone change given to a conversion of texts raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	zone_change = TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATETIME, timezone=ATTRIBUTE_UTC)

	with pytest.raises(InvalidConversionError):
		require_time_zone_setting(Type.TEXT, zone_change)


def test_require_format_setting_rejects_a_format_between_numbers() -> None:
	"""
	Check that a date format given to a conversion between numbers raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	day_first = TableConversion(columns=[CONVERTED_NAME], dtype=Type.INT64, format=DateFormat.DAY_MONTH_YEAR)

	with pytest.raises(InvalidConversionError):
		require_format_setting(Type.FLOAT64, day_first)


def test_require_brackets_setting_accepts_numbers_to_categories() -> None:
	"""
	Check that brackets given to a conversion of numbers to CATEGORY raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_brackets_setting(Type.FLOAT64, Type.CATEGORY)


@pytest.mark.parametrize(("source_type", "target_type"), [(Type.TEXT, Type.CATEGORY), (Type.INT64, Type.TEXT)])
def test_require_brackets_setting_rejects_another_conversion(source_type: Type, target_type: Type) -> None:
	"""
	Check that brackets given to texts, or to another type than CATEGORY, raise InvalidConversionError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the column.
	target_type
		The new type.
	"""
	with pytest.raises(InvalidConversionError):
		require_brackets_setting(source_type, target_type)


@pytest.mark.parametrize(
	("source_type", "target_type"), [(Type.TEXT, Type.TIME), (Type.TIME, Type.TEXT), (Type.TIME, Type.CATEGORY)]
)
def test_require_time_format_setting_accepts_a_time_pattern(source_type: Type, target_type: Type) -> None:
	"""
	Check that a pattern of a time only reads and writes times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the column.
	target_type
		The new type.
	"""
	require_time_format_setting(source_type, target_type, TIME_PATTERN)


@pytest.mark.parametrize("time_format", [DATE_PATTERN, DateFormat.DAY_MONTH_YEAR])
def test_require_time_format_setting_rejects_a_format_with_a_date(time_format: DateFormat | CustomDateFormat) -> None:
	"""
	Check that a pattern or a common format holding a date raises InvalidConversionError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	time_format
		A format with a date.
	"""
	with pytest.raises(InvalidConversionError):
		require_time_format_setting(Type.TEXT, Type.TIME, time_format)


def test_require_time_format_setting_rejects_a_conversion_without_text() -> None:
	"""
	Check that a format given to datetimes converted to times raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidConversionError):
		require_time_format_setting(Type.DATETIME, Type.TIME, TIME_PATTERN)


def test_require_conversion_settings_rejects_a_time_pattern_for_dates() -> None:
	"""
	Check that a pattern without date given to a conversion of texts to DATETIME raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATETIME, format=TIME_PATTERN)

	with pytest.raises(InvalidConversionError):
		require_conversion_settings(Type.TEXT, conversion)
