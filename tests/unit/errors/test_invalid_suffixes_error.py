"""
Unit tests of InvalidSuffixesError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_suffixes_error import InvalidSuffixesError
from numdaplot.errors.numdaplot_error import NumdaplotError

LEFT_SUFFIX = "_2025"
RIGHT_SUFFIX = "_2025"
EXPECTED_MESSAGE = "Expected two different non-empty suffixes, got '_2025' and '_2025'."


def test_invalid_suffixes_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidSuffixesError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidSuffixesError, NumdaplotError)


def test_invalid_suffixes_error_names_both_suffixes() -> None:
	"""
	Check the message and the attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSuffixesError(LEFT_SUFFIX, RIGHT_SUFFIX)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.left == LEFT_SUFFIX
	assert error.right == RIGHT_SUFFIX
