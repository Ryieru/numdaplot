"""
Unit tests of InvalidTypeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.statistics.mean import Mean

SETTING_NAME = "Region rows"
EXPECTED = "an Index, a Range or None"
GIVEN_NUMBER = 0
EXPECTED_TYPE_MESSAGE = "Region rows expects an Index, a Range or None, got 0."
EXPECTED_CLASS_MESSAGE = "ndp.Mean is a class, use ndp.Mean() instead."


def test_invalid_type_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidTypeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidTypeError, NumdaplotError)


def test_invalid_type_error_names_the_setting_and_what_it_expects() -> None:
	"""
	Check the message for a value of the wrong kind, and the kept attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidTypeError(SETTING_NAME, EXPECTED, GIVEN_NUMBER)

	error_text = str(error)
	assert error_text == EXPECTED_TYPE_MESSAGE
	assert error.target_name == SETTING_NAME
	assert error.expected == EXPECTED
	assert error.given == GIVEN_NUMBER


def test_invalid_type_error_adds_the_parentheses_to_a_class() -> None:
	"""
	Check the message for a class given in place of an object.

	.. versionadded:: 0.1.0
	"""
	error = InvalidTypeError(SETTING_NAME, EXPECTED, Mean)

	error_text = str(error)
	assert error_text == EXPECTED_CLASS_MESSAGE
