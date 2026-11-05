"""
Unit tests of the check of the format and the time zone change of a conversion.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.invalid_conversion_error import InvalidConversionError
from numdaplot.tables.columns.conversion import Conversion
from numdaplot.tables.columns.converted_column import require_conversion_settings

CONVERTED_NAME = "value"
UTC_ZONE = TimeZone("UTC")
ATTRIBUTE_UTC = TimeZoneChange(mode=TimeZoneMode.ATTRIBUTE, zone=UTC_ZONE)
REJECTED_SETTINGS = [
	Conversion(column=CONVERTED_NAME, dtype=Type.INT64, format=DateFormat.DAY_MONTH_YEAR),
	Conversion(column=CONVERTED_NAME, dtype=Type.DATE, format=DateFormat.DAY_MONTH_YEAR_TIME),
	Conversion(column=CONVERTED_NAME, dtype=Type.DATETIME, timezone=ATTRIBUTE_UTC),
]
FORMAT_AND_ZONE = Conversion(
	column=CONVERTED_NAME,
	dtype=Type.DATETIME,
	format=DateFormat.YEAR_MONTH_DAY_TIME,
	timezone=ATTRIBUTE_UTC,
)
ACCEPTED_SETTINGS = [
	Conversion(column=CONVERTED_NAME, dtype=Type.DATE, format=DateFormat.DAY_MONTH_YEAR),
	Conversion(column=CONVERTED_NAME, dtype=Type.DATETIME, format=DateFormat.DAY_MONTH_YEAR),
	Conversion(column=CONVERTED_NAME, dtype=Type.DATETIME, format=DateFormat.DAY_MONTH_YEAR_TIME),
]
TIME_FORMAT_ON_DATE = Conversion(column=CONVERTED_NAME, dtype=Type.DATE, format=DateFormat.YEAR_MONTH_DAY_TIME)
CUSTOM_TIME_ON_DATE = Conversion(column=CONVERTED_NAME, dtype=Type.DATE, format=CustomDateFormat("%d/%m/%Y %H:%M"))
TIME_FORMAT_WRITING_DATE = Conversion(column=CONVERTED_NAME, dtype=Type.TEXT, format=DateFormat.YEAR_MONTH_DAY_TIME)
EXPECTED_TIME_FORMAT_MESSAGE = (
	"The format YEAR_MONTH_DAY_TIME has a time, which DATE cannot hold. "
	"Convert the column to DATETIME first, then to DATE."
)
EXPECTED_CUSTOM_TIME_MESSAGE = (
	"The format %d/%m/%Y %H:%M has a time, which DATE cannot hold. Convert the column to DATETIME first, then to DATE."
)
EXPECTED_WRITING_MESSAGE = (
	"The format YEAR_MONTH_DAY_TIME has a time, which DATE cannot hold. "
	"Convert the column to DATETIME first, then to TEXT."
)
TIME_FORMAT_ON_DATE_TO_INTEGER = Conversion(
	column=CONVERTED_NAME, dtype=Type.INT64, format=DateFormat.YEAR_MONTH_DAY_TIME
)
EXPECTED_GENERAL_MESSAGE = "The setting format does not apply to a conversion from DATE to INT64."


@pytest.mark.parametrize("conversion", REJECTED_SETTINGS)
def test_require_conversion_settings_rejects_a_setting_that_does_not_apply(conversion: Conversion) -> None:
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
def test_require_conversion_settings_accepts_formats_reading_or_writing_dates(conversion: Conversion) -> None:
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
