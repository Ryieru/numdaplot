"""
Unit tests of EmptyListError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.numdaplot_error import NumdaplotError

ITEM_NAME = "condition"
EXPECTED_MESSAGE = "Expected at least one condition, got an empty list."


def test_empty_list_error_is_a_numdaplot_error() -> None:
	"""
	Check that EmptyListError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(EmptyListError, NumdaplotError)


def test_empty_list_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = EmptyListError(ITEM_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_empty_list_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = EmptyListError(ITEM_NAME)

	assert error.item_name == ITEM_NAME
