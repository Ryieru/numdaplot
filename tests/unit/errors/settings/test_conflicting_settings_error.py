"""
Unit tests of ConflictingSettingsError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.conflicting_settings_error import ConflictingSettingsError

FIRST_NAME = "color"
SECOND_NAME = "color_by"
EXPECTED_MESSAGE = "color and color_by cannot be given together."


def test_conflicting_settings_error_is_a_numdaplot_error() -> None:
	"""
	Check that ConflictingSettingsError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ConflictingSettingsError, NumdaplotError)


def test_conflicting_settings_error_message_states_both_settings() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = ConflictingSettingsError(FIRST_NAME, SECOND_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_conflicting_settings_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = ConflictingSettingsError(FIRST_NAME, SECOND_NAME)

	assert error.first_name == FIRST_NAME
	assert error.second_name == SECOND_NAME
