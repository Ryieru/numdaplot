"""
Unit tests of the reading and writing of CSV files.

.. versionadded:: 0.1.0
"""

import warnings
from pathlib import Path

import pandas
import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.tables.files.csv_file import (
	find_mixed_columns,
	read_csv_file,
	read_csv_header,
	read_pandas_csv,
	write_csv_file,
)
from numdaplot.tables.files.csv_read_options import CsvReadOptions
from numdaplot.tables.files.csv_write_options import CsvWriteOptions
from numdaplot.tables.files.encoding import Encoding

FILE_NAME = "sales.csv"
SEMICOLON_CONTENT = "city;price\nParis;1.5\nLyon;\n"
EXPECTED_COLUMN_NAMES = ["city", "price"]
EXPECTED_CITIES = ["Paris", "Lyon"]
EXPECTED_ROW_COUNT = 2
REPEATED_NAME_CONTENT = "price,price\n1,2\n"
EXPECTED_REPEATED_HEADER = ["price", "price"]
EMPTY_NAME_CONTENT = "city,\nParis,1\n"
INTEGER_CONTENT = "count\n1\n\n3\n"
INTEGER_DTYPE_NAME = "Int64"
LATIN_1_CONTENT = "ville\nB\u00e9ziers\n"
EXPECTED_LATIN_1_CITIES = ["B\u00e9ziers"]
WRITTEN_FRAME = {"city": ["Paris", None], "price": [1.5, 8.0]}
EXPECTED_WRITTEN_CONTENT = "city;price\nParis;1.5\n;8.0\n"
SEMICOLON = ";"
EMPTY_CONTENT = ""
# More rows than one block of pandas.read_csv, so the first block only holds numbers.
LONG_ROW_COUNT = 300_000
LONG_HEADER = "code;count\n"
LONG_NUMBER_ROW = "01;1\n"
LONG_LAST_ROW = "2A;2\n"
EXPECTED_FIRST_CODE = "01"
EXPECTED_LAST_CODE = "2A"
MIXED_COLUMN_NAMES = ["code"]
NO_COLUMN_NAMES = list[str]()
TEXT_SETTINGS = {"usecols": MIXED_COLUMN_NAMES, "dtype": str}
NO_SETTINGS = dict[str, object]()
MIXED_CODES = [1, "2A"]
MIXED_FLAGS = [True, "x"]
SAME_KIND_TEXTS = ["a", "b"]
INTEGERS_AND_DECIMALS = [1, 2.5]
PRICES = [1.5, 2.0]
OBJECT_DTYPE = object
CODES_CONTENT = "code,count\nN/A,1\n,2\nB,3\n"
EXPECTED_CODES_WITH_EMPTY_ONLY = ["N/A", pandas.NA, "B"]
EXPECTED_CODES_WITHOUT_MISSING = ["N/A", "", "B"]


def write_long_codes(tmp_path: Path) -> Path:
	"""
	Write a CSV file whose ``code`` column holds ``01`` in its whole first block, then ``2A`` on its last row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.

	Returns
	-------
	Path
		The path of the file.
	"""
	path = tmp_path / FILE_NAME
	number_rows = LONG_NUMBER_ROW * LONG_ROW_COUNT
	content = LONG_HEADER + number_rows + LONG_LAST_ROW
	path.write_text(content)

	return path


def test_read_csv_file_reads_every_row_with_its_separator(tmp_path: Path) -> None:
	"""
	Check that a CSV file separated by semicolons gives its columns and rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(SEMICOLON_CONTENT)

	options = CsvReadOptions(separator=SEMICOLON)

	frame = read_csv_file(path, options)

	column_names = list(frame.columns)
	city_column = frame["city"]
	cities = city_column.tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert cities == EXPECTED_CITIES


def test_read_csv_file_keeps_integers_with_missing_values_as_integers(tmp_path: Path) -> None:
	"""
	Check that a column of integers with an empty value is read with a nullable integer dtype.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(INTEGER_CONTENT)

	frame = read_csv_file(path, CsvReadOptions())

	count_column = frame["count"]
	dtype_name = str(count_column.dtype)
	assert dtype_name == INTEGER_DTYPE_NAME


def test_read_csv_file_gives_no_column_for_an_empty_file(tmp_path: Path) -> None:
	"""
	Check that an empty file gives an empty DataFrame.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(EMPTY_CONTENT)

	frame = read_csv_file(path, CsvReadOptions())

	assert frame.empty


def test_read_csv_file_rejects_a_repeated_column_name(tmp_path: Path) -> None:
	"""
	Check that two columns of the same name raise DuplicateColumnError instead of being renamed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(REPEATED_NAME_CONTENT)

	with pytest.raises(DuplicateColumnError):
		read_csv_file(path, CsvReadOptions())


def test_read_csv_file_rejects_an_empty_column_name(tmp_path: Path) -> None:
	"""
	Check that an empty header cell raises InvalidColumnNameError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(EMPTY_NAME_CONTENT)

	with pytest.raises(InvalidColumnNameError):
		read_csv_file(path, CsvReadOptions())


def test_read_csv_file_decodes_its_encoding(tmp_path: Path) -> None:
	"""
	Check that a Latin-1 file is decoded with its encoding.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(LATIN_1_CONTENT, encoding=Encoding.LATIN_1.value)

	options = CsvReadOptions(encoding=Encoding.LATIN_1)

	frame = read_csv_file(path, options)

	city_column = frame["ville"]
	cities = city_column.tolist()
	assert cities == EXPECTED_LATIN_1_CITIES


def test_read_csv_file_reads_mixed_blocks_again_as_texts(tmp_path: Path) -> None:
	"""
	Check that a column whose first block holds only numbers keeps the texts of the file, leading zeros included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_codes(tmp_path)
	options = CsvReadOptions(separator=SEMICOLON)

	frame = read_csv_file(path, options)

	code_column = frame["code"]
	codes = code_column.tolist()
	assert codes[0] == EXPECTED_FIRST_CODE
	assert codes[-1] == EXPECTED_LAST_CODE


def test_read_csv_file_keeps_the_types_of_the_other_columns(tmp_path: Path) -> None:
	"""
	Check that a column whose blocks share one type keeps it when another column is read again as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_codes(tmp_path)
	options = CsvReadOptions(separator=SEMICOLON)

	frame = read_csv_file(path, options)

	count_column = frame["count"]
	dtype_name = str(count_column.dtype)
	assert dtype_name == INTEGER_DTYPE_NAME


def test_read_pandas_csv_hides_the_pandas_mixed_type_warning(tmp_path: Path) -> None:
	"""
	Check that reading a file whose blocks get different types emits no warning.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_codes(tmp_path)
	options = CsvReadOptions(separator=SEMICOLON)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		read_pandas_csv(path, options, NO_SETTINGS)

	assert caught_warnings == []


def test_read_pandas_csv_reads_the_given_columns_as_texts(tmp_path: Path) -> None:
	"""
	Check that the column settings choose the columns read and read them as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_codes(tmp_path)
	options = CsvReadOptions(separator=SEMICOLON)

	frame = read_pandas_csv(path, options, TEXT_SETTINGS)

	column_names = list(frame.columns)
	code_column = frame["code"]
	first_code = code_column.iloc[0]
	assert column_names == MIXED_COLUMN_NAMES
	assert first_code == EXPECTED_FIRST_CODE


@pytest.mark.parametrize("mixed_values", [MIXED_CODES, MIXED_FLAGS])
def test_find_mixed_columns_names_a_column_of_numbers_or_booleans_and_texts(mixed_values: list[object]) -> None:
	"""
	Check that a column of Python objects mixing numbers or booleans with texts is named.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mixed_values
		The values of the column.
	"""
	code_column = pandas.Series(mixed_values, dtype=OBJECT_DTYPE)
	price_column = pandas.Series(PRICES)
	frame = pandas.DataFrame({"code": code_column, "price": price_column})

	mixed_names = find_mixed_columns(frame)

	assert mixed_names == MIXED_COLUMN_NAMES


@pytest.mark.parametrize("values", [SAME_KIND_TEXTS, INTEGERS_AND_DECIMALS])
def test_find_mixed_columns_ignores_values_that_keep_one_type(values: list[object]) -> None:
	"""
	Check that texts alone, or integers with decimals that become decimals, are not named.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of the column.
	"""
	column = pandas.Series(values, dtype=OBJECT_DTYPE)
	frame = pandas.DataFrame({"code": column})

	mixed_names = find_mixed_columns(frame)

	assert mixed_names == NO_COLUMN_NAMES


def test_read_csv_file_reads_only_the_given_missing_texts(tmp_path: Path) -> None:
	"""
	Check that N/A stays a text when only the empty text is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(CODES_CONTENT)

	frame = read_csv_file(path, CsvReadOptions(missing_texts=[""]))

	code_column = frame["code"]
	codes = code_column.tolist()
	assert codes == EXPECTED_CODES_WITH_EMPTY_ONLY


def test_read_csv_file_reads_an_empty_value_as_a_text_without_missing_text(tmp_path: Path) -> None:
	"""
	Check that an empty list of missing texts reads an empty value as an empty text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(CODES_CONTENT)

	frame = read_csv_file(path, CsvReadOptions(missing_texts=[]))

	code_column = frame["code"]
	codes = code_column.tolist()
	assert codes == EXPECTED_CODES_WITHOUT_MISSING


def test_read_csv_header_keeps_repeated_names(tmp_path: Path) -> None:
	"""
	Check that the header is read as written, repeated names included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(REPEATED_NAME_CONTENT)

	header = read_csv_header(path, CsvReadOptions())

	assert header == EXPECTED_REPEATED_HEADER


def test_write_csv_file_writes_missing_values_as_empty_values(tmp_path: Path) -> None:
	"""
	Check the written text: names first, separator, no row numbers, empty missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(WRITTEN_FRAME)

	options = CsvWriteOptions(separator=SEMICOLON)

	write_csv_file(frame, path, options)

	content = path.read_text()
	assert content == EXPECTED_WRITTEN_CONTENT
