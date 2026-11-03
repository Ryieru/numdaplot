"""
Unit tests of the reading and writing of CSV files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas
import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.tables.files.csv_file import read_csv_file, read_csv_header, write_csv_file
from numdaplot.tables.files.csv_options import CsvOptions
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

	options = CsvOptions(separator=SEMICOLON)

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

	frame = read_csv_file(path, CsvOptions())

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

	frame = read_csv_file(path, CsvOptions())

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
		read_csv_file(path, CsvOptions())


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
		read_csv_file(path, CsvOptions())


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

	options = CsvOptions(encoding=Encoding.LATIN_1)

	frame = read_csv_file(path, options)

	city_column = frame["ville"]
	cities = city_column.tolist()
	assert cities == EXPECTED_LATIN_1_CITIES


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

	header = read_csv_header(path, CsvOptions())

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

	options = CsvOptions(separator=SEMICOLON)

	write_csv_file(frame, path, options)

	content = path.read_text()
	assert content == EXPECTED_WRITTEN_CONTENT
