"""
Unit tests of CsvOptions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.tables.files.csv_options import CsvOptions
from numdaplot.tables.files.encoding import Encoding

COMMA = ","
SEMICOLON = ";"
REJECTED_SEPARATORS = ["", ";;"]


def test_csv_options_use_a_comma_and_utf_8_by_default() -> None:
	"""
	Check the default separator and encoding.

	.. versionadded:: 0.1.0
	"""
	options = CsvOptions()

	assert options.separator == COMMA
	assert options.encoding == Encoding.UTF_8


def test_csv_options_keep_their_settings() -> None:
	"""
	Check that given settings are available as attributes.

	.. versionadded:: 0.1.0
	"""
	options = CsvOptions(separator=SEMICOLON, encoding=Encoding.LATIN_1)

	assert options.separator == SEMICOLON
	assert options.encoding == Encoding.LATIN_1


@pytest.mark.parametrize("separator", REJECTED_SEPARATORS)
def test_csv_options_reject_a_separator_that_is_not_one_character(separator: str) -> None:
	"""
	Check that an empty or longer separator raises InvalidSeparatorError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		A rejected separator.
	"""
	with pytest.raises(InvalidSeparatorError):
		CsvOptions(separator=separator)
