"""
Unit tests of IrregularListError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.positions.irregular_list_error import IrregularListError

EXPECTED_MESSAGE = "Expected nested lists of equal lengths."


def test_irregular_list_error_is_a_numdaplot_error() -> None:
	"""
	Check that IrregularListError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(IrregularListError, NumdaplotError)


def test_irregular_list_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = IrregularListError()

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
