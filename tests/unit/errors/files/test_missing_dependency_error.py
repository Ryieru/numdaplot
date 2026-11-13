"""
Unit tests of MissingDependencyError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.files.missing_dependency_error import MissingDependencyError
from numdaplot.errors.numdaplot_error import NumdaplotError

PACKAGE_NAME = "openpyxl"
EXTRA_NAME = "excel"
EXPECTED_MESSAGE = "This file format needs the openpyxl package, install it with: pip install numdaplot[excel]"


def test_missing_dependency_error_is_a_numdaplot_error() -> None:
	"""
	Check that MissingDependencyError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(MissingDependencyError, NumdaplotError)


def test_missing_dependency_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = MissingDependencyError(PACKAGE_NAME, EXTRA_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_missing_dependency_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = MissingDependencyError(PACKAGE_NAME, EXTRA_NAME)

	assert error.package_name == PACKAGE_NAME
	assert error.extra_name == EXTRA_NAME
