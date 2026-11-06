"""
Unit tests of TimeOverflowError.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.time_overflow_error import TimeOverflowError

OPERATION_NAME = "*"
COLUMN_NAME = "when"
OTHER_COLUMN_NAME = "other"
DURATION_NAME = "DURATION"
DURATION_MESSAGE = "The operation * gives values outside the range of DURATION, about 292 years before or after zero."
DATETIME_MESSAGE = "The operation * gives values outside the range of DATETIME, from 1677 to 2262."
DATE_MESSAGE = "The operation * gives values outside the range of DATE, from 1677 to 2262 in a calculation."
NAMED_MESSAGE = (
	"The operation * gives values of the column 'when' outside the range of DURATION, "
	"about 292 years before or after zero."
)


def test_time_overflow_error_is_a_numdaplot_error() -> None:
	"""
	Check that TimeOverflowError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(TimeOverflowError, NumdaplotError)


@pytest.mark.parametrize(
	("type_name", "expected_message"),
	[("DURATION", DURATION_MESSAGE), ("DATETIME", DATETIME_MESSAGE), ("DATE", DATE_MESSAGE)],
)
def test_time_overflow_error_message_gives_the_range_of_the_type(type_name: str, expected_message: str) -> None:
	"""
	Check the message of each type.

	.. versionadded:: 0.1.0
	"""
	error = TimeOverflowError(OPERATION_NAME, type_name)

	error_text = str(error)
	assert error_text == expected_message


def test_time_overflow_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = TimeOverflowError(OPERATION_NAME, DURATION_NAME)

	assert error.operation_name == OPERATION_NAME
	assert error.type_name == DURATION_NAME
	assert error.column_name is None


def test_name_column_adds_the_column_to_the_message() -> None:
	"""
	Check the message once the column is named.

	.. versionadded:: 0.1.0
	"""
	error = TimeOverflowError(OPERATION_NAME, DURATION_NAME)

	error.name_column(COLUMN_NAME)

	error_text = str(error)
	assert error_text == NAMED_MESSAGE
	assert error.column_name == COLUMN_NAME


def test_name_column_keeps_the_first_column() -> None:
	"""
	Check that a second name does not replace the first one.

	.. versionadded:: 0.1.0
	"""
	error = TimeOverflowError(OPERATION_NAME, DURATION_NAME)
	error.name_column(COLUMN_NAME)

	error.name_column(OTHER_COLUMN_NAME)

	assert error.column_name == COLUMN_NAME
