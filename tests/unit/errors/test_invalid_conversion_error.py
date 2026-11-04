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
