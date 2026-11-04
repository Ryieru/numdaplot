"""
Unit tests of UnsupportedDataError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.unsupported_data_error import UnsupportedDataError

OWNER_NAME = "PieChart"
DATA_NAME = "an Array"
EXPECTED_MESSAGE = "PieChart cannot draw an Array, use a Table."


def test_unsupported_data_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedDataError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedDataError, NumdaplotError)


def test_unsupported_data_error_message_states_what_refuses_the_data() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedDataError(OWNER_NAME, DATA_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unsupported_data_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedDataError(OWNER_NAME, DATA_NAME)

	assert error.owner_name == OWNER_NAME
	assert error.data_name == DATA_NAME
