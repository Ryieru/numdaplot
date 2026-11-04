"""
Unit tests of RefusedSettingError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.refused_setting_error import RefusedSettingError

SETTING_NAME = "MarkerShape.NONE"
OWNER_NAME = "ScatterChart"
EXPECTED_MESSAGE = "ScatterChart does not accept MarkerShape.NONE."


def test_refused_setting_error_is_a_numdaplot_error() -> None:
	"""
	Check that RefusedSettingError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(RefusedSettingError, NumdaplotError)


def test_refused_setting_error_message_states_the_setting_and_its_owner() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = RefusedSettingError(SETTING_NAME, OWNER_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_refused_setting_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = RefusedSettingError(SETTING_NAME, OWNER_NAME)

	assert error.setting_name == SETTING_NAME
	assert error.owner_name == OWNER_NAME
