"""
Unit tests of UnsupportedIndexError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.unsupported_index_error import UnsupportedIndexError

EXPECTED_MESSAGE = "A Table has no index, call reset_index() on the DataFrame first to keep its index as a column."


def test_unsupported_index_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedIndexError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedIndexError, NumdaplotError)


def test_unsupported_index_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedIndexError()

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
