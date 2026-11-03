"""
Unit tests of ValueConversionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.value_conversion_error import ValueConversionError

SOURCE_TYPE_NAME = "FLOAT64"
TARGET_TYPE_NAME = "INT64"
EXPECTED_MESSAGE = "Cannot store FLOAT64 values as INT64 without losing information."


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
