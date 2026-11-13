"""
Unit tests of the check of the separator of a CSV file.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.files.invalid_separator_error import InvalidSeparatorError
from numdaplot.tables.files.csv.csv_separator import require_separator

SEMICOLON = ";"
REJECTED_SEPARATORS = ["", ";;"]


def test_require_separator_accepts_one_character() -> None:
	"""
	Check that a separator of one character raises nothing.

	.. versionadded:: 0.1.0
	"""
	require_separator(SEMICOLON)


@pytest.mark.parametrize("separator", REJECTED_SEPARATORS)
def test_require_separator_rejects_a_separator_that_is_not_one_character(separator: str) -> None:
	"""
	Check that an empty or longer separator raises InvalidSeparatorError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		A rejected separator.
	"""
	with pytest.raises(InvalidSeparatorError):
		require_separator(separator)
