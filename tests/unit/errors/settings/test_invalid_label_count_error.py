"""
Unit tests of InvalidLabelCountError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.invalid_label_count_error import InvalidLabelCountError

BRACKET_COUNT = 2
LABEL_COUNT = 3
EXPECTED_MESSAGE = "Expected 2 labels, one per bracket, got 3."


def test_invalid_label_count_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidLabelCountError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidLabelCountError, NumdaplotError)


def test_invalid_label_count_error_gives_both_counts() -> None:
	"""
	Check the message and the attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidLabelCountError(BRACKET_COUNT, LABEL_COUNT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.bracket_count == BRACKET_COUNT
	assert error.label_count == LABEL_COUNT
