"""
Unit tests of InvalidLimitsError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.brackets.invalid_limits_error import InvalidLimitsError
from numdaplot.errors.numdaplot_error import NumdaplotError

UNORDERED_LIMITS = list[int | float]([0, 10, 10])
SINGLE_LIMIT = list[int | float]([0])
EMPTY_BRACKET = list[int | float]([5.2, 5.8])
EXPECTED_UNORDERED_MESSAGE = "Expected limits in strictly increasing order, got 10 after 10."
EXPECTED_SINGLE_MESSAGE = "Expected at least 2 limits, or 1 with an open first or last bracket, got 1."
EXPECTED_EMPTY_MESSAGE = "The bracket from 5.2 to 5.8 holds no integer."


def test_invalid_limits_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidLimitsError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidLimitsError, NumdaplotError)


def test_invalid_limits_error_names_the_first_limit_not_greater() -> None:
	"""
	Check the message of limits that do not strictly increase.

	.. versionadded:: 0.1.0
	"""
	error = InvalidLimitsError(UNORDERED_LIMITS)

	error_text = str(error)
	assert error_text == EXPECTED_UNORDERED_MESSAGE


def test_invalid_limits_error_counts_too_few_limits() -> None:
	"""
	Check the message of a single limit.

	.. versionadded:: 0.1.0
	"""
	error = InvalidLimitsError(SINGLE_LIMIT)

	error_text = str(error)
	assert error_text == EXPECTED_SINGLE_MESSAGE


def test_invalid_limits_error_names_a_bracket_without_integer() -> None:
	"""
	Check the message and the attribute of an empty integer bracket.

	.. versionadded:: 0.1.0
	"""
	error = InvalidLimitsError(EMPTY_BRACKET, EMPTY_BRACKET)

	error_text = str(error)
	assert error_text == EXPECTED_EMPTY_MESSAGE
	assert error.empty_bracket == EMPTY_BRACKET
