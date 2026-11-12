"""
Unit tests of ValueConversionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.rejected_dates import RejectedDate, RejectedDatePart
from numdaplot.errors.value_conversion_error import ValueConversionError

SOURCE_TYPE_NAME = "FLOAT64"
TARGET_TYPE_NAME = "INT64"
EXPECTED_MESSAGE = "Cannot store FLOAT64 values as INT64 without losing information."
REJECTED_VALUE = 2.5
EXPECTED_REJECTED_VALUE_MESSAGE = "Cannot store the FLOAT64 value 2.5 as INT64 without losing information."
TEXT_TYPE_NAME = "TEXT"
DATETIME_TYPE_NAME = "DATETIME"
REJECTED_TEXT = "31/12/2026"
DATE_FORMAT_NAME = "YEAR_MONTH_DAY_TIME"
EXPECTED_UNREADABLE_DATE_MESSAGE = (
	"Cannot read the TEXT value '31/12/2026' as DATETIME with the format YEAR_MONTH_DAY_TIME. "
	"Give the format of the values with format=, using DateFormat or CustomDateFormat."
)

HALF_DAY = RejectedDatePart("day", 3.5)
FEBRUARY_31 = RejectedDate(2025, 2, 31)
EXPECTED_HALF_DAY_MESSAGE = "Cannot use the FLOAT64 value 3.5 as a day: date parts must be whole numbers."
EXPECTED_FEBRUARY_31_MESSAGE = "Cannot build a DATE from the year 2025, the month 2 and the day 31."
EXPECTED_UNREADABLE_TIME_MESSAGE = (
	"Cannot read the TEXT value '25:00' as TIME with the format HH:MM:SS. Give the format of the values with format=, "
	"using a CustomDateFormat of a time only."
)


def test_value_conversion_error_is_a_numdaplot_error() -> None:
	"""
	Check that ValueConversionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ValueConversionError, NumdaplotError)


def test_value_conversion_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_value_conversion_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	assert error.source_type_name == SOURCE_TYPE_NAME
	assert error.target_type_name == TARGET_TYPE_NAME


def test_value_conversion_error_message_shows_the_rejected_value() -> None:
	"""
	Check that a known rejected value appears in the message.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME, REJECTED_VALUE)

	error_text = str(error)
	assert error_text == EXPECTED_REJECTED_VALUE_MESSAGE


def test_value_conversion_error_keeps_its_rejected_value() -> None:
	"""
	Check that the rejected value is available as an attribute, and None when not given.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME, REJECTED_VALUE)
	unknown_value_error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	assert error.rejected_value == REJECTED_VALUE
	assert unknown_value_error.rejected_value is None


def test_value_conversion_error_message_names_the_format_of_an_unreadable_date() -> None:
	"""
	Check that a rejected text and a date format give the message pointing to the format setting.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(TEXT_TYPE_NAME, DATETIME_TYPE_NAME, REJECTED_TEXT, DATE_FORMAT_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_UNREADABLE_DATE_MESSAGE


def test_value_conversion_error_message_ignores_a_format_without_rejected_value() -> None:
	"""
	Check that a date format without rejected value keeps the general message.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME, date_format_name=DATE_FORMAT_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_value_conversion_error_keeps_its_date_format_name() -> None:
	"""
	Check that the format name is available as an attribute, and None when not given.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(TEXT_TYPE_NAME, DATETIME_TYPE_NAME, REJECTED_TEXT, DATE_FORMAT_NAME)
	general_error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	assert error.date_format_name == DATE_FORMAT_NAME
	assert general_error.date_format_name is None


def test_value_conversion_error_has_no_column_by_default() -> None:
	"""
	Check that a new error names no column.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	assert error.column_name is None


def test_name_column_names_the_values_without_rejected_value() -> None:
	"""
	Check the message of values without a rejected value.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)

	error.name_column("price")

	assert str(error) == "Cannot store FLOAT64 values of the column 'price' as INT64 without losing information."


def test_name_column_names_the_rejected_value() -> None:
	"""
	Check the message of a rejected value.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError("TEXT", "FLOAT64", "abc")

	error.name_column("price")

	assert (
		str(error) == "Cannot store the TEXT value 'abc' of the column 'price' as FLOAT64 without losing information."
	)


def test_name_column_keeps_the_date_format_advice() -> None:
	"""
	Check the message of an unreadable date.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Checks the advice speaking of the values.
	"""
	error = ValueConversionError("TEXT", "DATE", "x", "YEAR_MONTH_DAY")

	error.name_column("day")

	error_text = str(error)
	assert error_text.startswith(
		"Cannot read the TEXT value 'x' of the column 'day' as DATE with the format YEAR_MONTH_DAY."
	)
	assert "Give the format of the values" in error_text


def test_name_column_keeps_the_first_name() -> None:
	"""
	Check that a named column does not change.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError(SOURCE_TYPE_NAME, TARGET_TYPE_NAME)
	error.name_column("price")

	error.name_column("other")

	assert error.column_name == "price"


def test_value_conversion_error_names_a_date_part_that_is_not_whole() -> None:
	"""
	Check the message of the day 3.5.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError("FLOAT64", "DATE", HALF_DAY)

	error_text = str(error)
	assert error_text == EXPECTED_HALF_DAY_MESSAGE


def test_value_conversion_error_names_parts_that_form_no_date() -> None:
	"""
	Check the message of the 31st of February.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError("INT64", "DATE", FEBRUARY_31)

	error_text = str(error)
	assert error_text == EXPECTED_FEBRUARY_31_MESSAGE


def test_value_conversion_error_points_an_unreadable_time_to_a_time_pattern() -> None:
	"""
	Check the message of a text that is not a time of day.

	.. versionadded:: 0.1.0
	"""
	error = ValueConversionError("TEXT", "TIME", "25:00", "HH:MM:SS")

	error_text = str(error)
	assert error_text == EXPECTED_UNREADABLE_TIME_MESSAGE
