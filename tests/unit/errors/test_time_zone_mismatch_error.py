"""
Unit tests of TimeZoneMismatchError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError

OPERATION = "Removing the time zone"
EXPECTS_TIME_ZONE = True
EXPECTED_MESSAGE = "Removing the time zone needs datetimes with a time zone."
ARRAY_OPERATION = "An Array"
EXPECTED_NAIVE_MESSAGE = "An Array needs datetimes without a time zone."


def test_time_zone_mismatch_error_is_a_numdaplot_error() -> None:
	"""
	Check that TimeZoneMismatchError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(TimeZoneMismatchError, NumdaplotError)


def test_time_zone_mismatch_error_message_states_the_needed_zone_state() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = TimeZoneMismatchError(OPERATION, EXPECTS_TIME_ZONE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_time_zone_mismatch_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = TimeZoneMismatchError(OPERATION, EXPECTS_TIME_ZONE)

	assert error.operation == OPERATION
	assert error.expects_time_zone == EXPECTS_TIME_ZONE


def test_time_zone_mismatch_error_message_states_a_zone_is_not_wanted() -> None:
	"""
	Check the message of an operation needing datetimes without zone.

	.. versionadded:: 0.1.0
	"""
	error = TimeZoneMismatchError(ARRAY_OPERATION, False)

	error_text = str(error)
	assert error_text == EXPECTED_NAIVE_MESSAGE
