"""
Unit tests of UnknownTimeZoneError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.dates.unknown_time_zone_error import UnknownTimeZoneError
from numdaplot.errors.numdaplot_error import NumdaplotError

NAME = "Paris"
EXPECTED_MESSAGE = "Unknown time zone 'Paris', expected an IANA name such as 'Europe/Paris' or 'UTC'."


def test_unknown_time_zone_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnknownTimeZoneError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnknownTimeZoneError, NumdaplotError)


def test_unknown_time_zone_error_message_names_the_zone() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnknownTimeZoneError(NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unknown_time_zone_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnknownTimeZoneError(NAME)

	assert error.name == NAME
