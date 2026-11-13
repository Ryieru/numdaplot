"""
Unit tests of InvalidSheetNameError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.files.invalid_sheet_name_error import InvalidSheetNameError
from numdaplot.errors.numdaplot_error import NumdaplotError

SHEET = "Sales/2026"
EXPECTED_MESSAGE = "Expected a sheet name of 1 to 31 characters without [ ] : * ? / \\, got 'Sales/2026'."


def test_invalid_sheet_name_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidSheetNameError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidSheetNameError, NumdaplotError)


def test_invalid_sheet_name_error_names_the_rules_of_excel() -> None:
	"""
	Check the message and the kept sheet name.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSheetNameError(SHEET)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.sheet == SHEET
