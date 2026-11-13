"""
Unit tests of InvalidTimeZoneChangeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.dates.invalid_time_zone_change_error import InvalidTimeZoneChangeError
from numdaplot.errors.numdaplot_error import NumdaplotError

MODE_NAME = "REMOVE"
NEEDS_ZONE = False
EXPECTED_MESSAGE = "TimeZoneMode.REMOVE takes no zone."
SHIFT_NAME = "SHIFT"
EXPECTED_MISSING_MESSAGE = "TimeZoneMode.SHIFT needs a zone."


def test_invalid_time_zone_change_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidTimeZoneChangeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidTimeZoneChangeError, NumdaplotError)


def test_invalid_time_zone_change_error_message_states_the_extra_zone() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidTimeZoneChangeError(MODE_NAME, NEEDS_ZONE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_time_zone_change_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidTimeZoneChangeError(MODE_NAME, NEEDS_ZONE)

	assert error.mode_name == MODE_NAME
	assert error.needs_zone == NEEDS_ZONE


def test_invalid_time_zone_change_error_message_states_the_missing_zone() -> None:
	"""
	Check the message of a mode needing a zone.

	.. versionadded:: 0.1.0
	"""
	error = InvalidTimeZoneChangeError(SHIFT_NAME, True)

	error_text = str(error)
	assert error_text == EXPECTED_MISSING_MESSAGE
