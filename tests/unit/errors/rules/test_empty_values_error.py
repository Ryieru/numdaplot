"""
Unit tests of EmptyValuesError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.rules.empty_values_error import EMPTY_VALUES_MESSAGE, EmptyValuesError


def test_empty_values_error_is_a_numdaplot_error() -> None:
	"""
	Check that EmptyValuesError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(EmptyValuesError, NumdaplotError)


def test_empty_values_error_explains_that_a_value_is_expected() -> None:
	"""
	Check the message of the error.

	.. versionadded:: 0.1.0
	"""
	error = EmptyValuesError()

	error_text = str(error)
	assert error_text == EMPTY_VALUES_MESSAGE
