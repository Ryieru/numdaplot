"""
Unit tests of EmptyRegionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.empty_region_error import EMPTY_REGION_MESSAGE, EmptyRegionError
from numdaplot.errors.numdaplot_error import NumdaplotError


def test_empty_region_error_is_a_numdaplot_error() -> None:
	"""
	Check that EmptyRegionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(EmptyRegionError, NumdaplotError)


def test_empty_region_error_explains_that_rows_or_columns_are_needed() -> None:
	"""
	Check the message of the error.

	.. versionadded:: 0.1.0
	"""
	error = EmptyRegionError()

	error_text = str(error)
	assert error_text == EMPTY_REGION_MESSAGE
