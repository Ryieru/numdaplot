"""
Unit tests of ValueConversionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.value_conversion_error import ValueConversionError

SOURCE_TYPE_NAME = "FLOAT64"
TARGET_TYPE_NAME = "INT64"
EXPECTED_MESSAGE = "Cannot store FLOAT64 values as INT64 without losing information."
REJECTED_VALUE = 2.5
EXPECTED_REJECTED_VALUE_MESSAGE = "Cannot store the FLOAT64 value 2.5 as INT64 without losing information."


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
