"""
Unit tests of UnsupportedTypeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.types.unsupported_type_error import UnsupportedTypeError
from numdaplot.types.library import Library

TYPE_NAME = "CATEGORY"
EXPECTED_MESSAGE = "The type CATEGORY has no equivalent between numdaplot and numpy."


def test_unsupported_type_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedTypeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedTypeError, NumdaplotError)


def test_unsupported_type_error_message_names_the_type_and_the_library() -> None:
	"""
	Check that the message states the type and the library name.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedTypeError(TYPE_NAME, Library.NUMPY)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unsupported_type_error_keeps_the_type_and_the_library() -> None:
	"""
	Check that the type name and the library are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedTypeError(TYPE_NAME, Library.NUMPY)

	assert error.type_name == TYPE_NAME
	assert error.library == Library.NUMPY
