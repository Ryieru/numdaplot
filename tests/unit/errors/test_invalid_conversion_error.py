"""
Unit tests of InvalidConversionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_conversion_error import InvalidConversionError
from numdaplot.errors.numdaplot_error import NumdaplotError

SETTING_NAME = "format"
SOURCE_TYPE_NAME = "INT64"
TARGET_TYPE_NAME = "TEXT"
EXPECTED_MESSAGE = "The setting format does not apply to a conversion from INT64 to TEXT."
DATE_TYPE_NAME = "DATE"
TEXT_TYPE_NAME = "TEXT"
DATE_FORMAT_NAME = "YEAR_MONTH_DAY_TIME"
EXPECTED_WRITING_MESSAGE = (
	"The format YEAR_MONTH_DAY_TIME has a time, which DATE cannot hold. "
	"Convert the column to DATETIME first, then to TEXT."
)
EXPECTED_TIME_FORMAT_MESSAGE = (
	"The format YEAR_MONTH_DAY_TIME has a time, which DATE cannot hold. "
	"Convert the column to DATETIME first, then to DATE."
)
EXPECTED_DATE_ON_TIME_MESSAGE = (
	"The format DAY_MONTH_YEAR has a date, which TIME cannot hold. Give a CustomDateFormat of a time only, "
	'such as "%H:%M".'
)


def test_invalid_conversion_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidConversionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidConversionError, NumdaplotError)


def test_invalid_conversion_error_message_names_the_setting_and_the_types() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidConversionError(SETTING_NAME, SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_conversion_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidConversionError(SETTING_NAME, SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	assert error.setting_name == SETTING_NAME
	assert error.source_type_name == SOURCE_TYPE_NAME
	assert error.target_type_name == TARGET_TYPE_NAME


def test_invalid_conversion_error_message_points_a_time_format_to_datetimes() -> None:
	"""
	Check the message of a format with a time read as dates.

	.. versionadded:: 0.1.0
	"""
	error = InvalidConversionError(SETTING_NAME, TEXT_TYPE_NAME, DATE_TYPE_NAME, DATE_FORMAT_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_TIME_FORMAT_MESSAGE


def test_invalid_conversion_error_message_names_the_target_type_after_datetimes() -> None:
	"""
	Check that a format with a time used to write dates names the type to convert to last.

	.. versionadded:: 0.1.0
	"""
	error = InvalidConversionError(SETTING_NAME, DATE_TYPE_NAME, TEXT_TYPE_NAME, DATE_FORMAT_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_WRITING_MESSAGE


def test_invalid_conversion_error_keeps_its_date_format_name() -> None:
	"""
	Check that the format name is available as an attribute, and None when not given.

	.. versionadded:: 0.1.0
	"""
	error = InvalidConversionError(SETTING_NAME, TEXT_TYPE_NAME, DATE_TYPE_NAME, DATE_FORMAT_NAME)
	general_error = InvalidConversionError(SETTING_NAME, SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	assert error.date_format_name == DATE_FORMAT_NAME
	assert general_error.date_format_name is None


def test_invalid_conversion_error_points_a_date_format_on_times_to_a_time_pattern() -> None:
	"""
	Check the message of a format with a date given to times of day.

	.. versionadded:: 0.1.0
	"""
	error = InvalidConversionError("format", "TEXT", "TIME", "DAY_MONTH_YEAR")

	error_text = str(error)
	assert error_text == EXPECTED_DATE_ON_TIME_MESSAGE
