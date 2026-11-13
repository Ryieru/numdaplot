"""
Unit tests of CsvWriteOptions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.tables.files.csv.csv_write_options import CsvWriteOptions
from numdaplot.tables.files.encoding import Encoding

COMMA = ","
SEMICOLON = ";"
DOUBLE_SEMICOLON = ";;"
DECIMALS = 2
NEGATIVE_DECIMALS = -1


def test_csv_write_options_use_a_comma_utf_8_and_every_digit_by_default() -> None:
	"""
	Check the default separator, encoding and decimals.

	.. versionadded:: 0.1.0
	"""
	options = CsvWriteOptions()

	assert options.separator == COMMA
	assert options.encoding == Encoding.UTF_8
	assert options.decimals is None


def test_csv_write_options_keep_their_settings() -> None:
	"""
	Check that given settings are available as attributes.

	.. versionadded:: 0.1.0
	"""
	options = CsvWriteOptions(separator=SEMICOLON, encoding=Encoding.LATIN_1, decimals=DECIMALS)

	assert options.separator == SEMICOLON
	assert options.encoding == Encoding.LATIN_1
	assert options.decimals == DECIMALS


def test_csv_write_options_reject_a_separator_that_is_not_one_character() -> None:
	"""
	Check that the separator is checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSeparatorError):
		CsvWriteOptions(separator=DOUBLE_SEMICOLON)


def test_csv_write_options_reject_negative_decimals() -> None:
	"""
	Check that the number of decimals is checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		CsvWriteOptions(decimals=NEGATIVE_DECIMALS)
