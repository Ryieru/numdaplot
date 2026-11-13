"""
Unit tests of CsvReadOptions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.csv.csv_read_options import CsvReadOptions
from numdaplot.tables.files.encoding import Encoding

COMMA = ","
SEMICOLON = ";"
DOUBLE_SEMICOLON = ";;"


def test_csv_read_options_use_a_comma_and_utf_8_by_default() -> None:
	"""
	Check the default separator and encoding.

	.. versionadded:: 0.1.0
	"""
	options = CsvReadOptions()

	assert options.separator == COMMA
	assert options.encoding == Encoding.UTF_8


def test_csv_read_options_keep_their_settings() -> None:
	"""
	Check that given settings are available as attributes.

	.. versionadded:: 0.1.0
	"""
	options = CsvReadOptions(separator=SEMICOLON, encoding=Encoding.LATIN_1)

	assert options.separator == SEMICOLON
	assert options.encoding == Encoding.LATIN_1


def test_csv_read_options_reject_a_separator_that_is_not_one_character() -> None:
	"""
	Check that the separator is checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSeparatorError):
		CsvReadOptions(separator=DOUBLE_SEMICOLON)


def test_csv_read_options_clean_the_column_names_by_default() -> None:
	"""
	Check that the column names are cleaned by default.

	.. versionadded:: 0.1.0
	"""
	options = CsvReadOptions()

	assert options.column_names == ColumnNames.CLEANED


def test_csv_read_options_read_the_default_missing_texts_when_omitted() -> None:
	"""
	Check that no list of missing texts is given by default.

	.. versionadded:: 0.1.0
	"""
	options = CsvReadOptions()

	assert options.missing_texts is None


def test_csv_read_options_keep_their_own_copy_of_the_missing_texts() -> None:
	"""
	Check that changing the given list afterwards does not change the settings.

	.. versionadded:: 0.1.0
	"""
	missing_texts = ["N/A"]
	options = CsvReadOptions(missing_texts=missing_texts)

	missing_texts.append("-")

	assert options.missing_texts == ["N/A"]
