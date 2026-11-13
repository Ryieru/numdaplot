"""
Unit tests of UnsupportedImageFormatError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.files.unsupported_image_format_error import UnsupportedImageFormatError
from numdaplot.errors.numdaplot_error import NumdaplotError

EXTENSION = ".jpg"
EXPECTED_MESSAGE = "Cannot save an image as '.jpg': use .png, .svg or .pdf."


def test_unsupported_image_format_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedImageFormatError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedImageFormatError, NumdaplotError)


def test_unsupported_image_format_error_message_states_the_rejected_extension() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedImageFormatError(EXTENSION)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unsupported_image_format_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedImageFormatError(EXTENSION)

	assert error.extension == EXTENSION
