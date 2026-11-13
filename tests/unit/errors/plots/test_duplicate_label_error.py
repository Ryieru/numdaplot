"""
Unit tests of DuplicateLabelError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.duplicate_label_error import DuplicateLabelError

LABEL = "Paris"
EXPECTED_MESSAGE = "The label 'Paris' appears more than once."


def test_duplicate_label_error_is_a_numdaplot_error() -> None:
	"""
	Check that DuplicateLabelError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(DuplicateLabelError, NumdaplotError)


def test_duplicate_label_error_message_states_the_repeated_label() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateLabelError(LABEL)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_duplicate_label_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateLabelError(LABEL)

	assert error.label == LABEL
