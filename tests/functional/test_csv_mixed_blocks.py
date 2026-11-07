"""
Functional tests of a long CSV file whose columns mix numbers and texts.

.. versionadded:: 0.1.0
"""

import warnings
from pathlib import Path
from typing import Any, cast

import pandas

import numdaplot as ndp

FILE_NAME = "accidents.csv"
SEMICOLON = ";"
# More rows than one block of pandas.read_csv, so the first block only holds numbers.
LONG_ROW_COUNT = 300_000
HEADER = "dep;com;night;count;speed\n"
FIRST_BLOCK_ROW = "01;01004;true;1;50\n"
LAST_ROWS = "2A;2A004;x;2;N/A\nN/A;01004;false;3;30.5\n"
EXPECTED_FIRST_DEP = "01"
EXPECTED_LAST_DEPS = ["2A", None]
WHOLE_FILE_SETTINGS = {"sep": SEMICOLON, "dtype_backend": "numpy_nullable", "low_memory": False}
FIRST_ROW = ndp.Region(rows=ndp.Index(0))
LAST_TWO_ROWS = ndp.Region(rows=ndp.Range(LONG_ROW_COUNT, LONG_ROW_COUNT + 1))


def write_long_file(tmp_path: Path) -> Path:
	"""
	Write a CSV file whose first block holds only numbers and booleans, followed by texts on its last rows.

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
	first_block = FIRST_BLOCK_ROW * LONG_ROW_COUNT
	content = HEADER + first_block + LAST_ROWS
	path.write_text(content)

	return path


def read_whole_file(path: Path) -> ndp.Table:
	"""
	Return the Table of a CSV file that pandas reads at once instead of in blocks.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file.

	Returns
	-------
	ndp.Table
		The Table of the whole-file reading.
	"""
	# Some versions of the pandas stubs leave the parameter types of read_csv unknown.
	csv_pandas = cast(Any, pandas)
	raw_frame = csv_pandas.read_csv(path, **WHOLE_FILE_SETTINGS)
	frame = cast(pandas.DataFrame, raw_frame)
	table = ndp.Table.from_pandas(frame)

	return table


def test_a_long_csv_file_keeps_the_leading_zeros_of_a_mixed_column(tmp_path: Path) -> None:
	"""
	Check that a code column read as numbers in its first block keeps ``01`` as written.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_file(tmp_path)

	table = ndp.Table.from_csv(path, ndp.CsvOptions(separator=SEMICOLON))

	dep_column = table.column("dep")
	first_dep_array = dep_column.take(FIRST_ROW)
	first_dep = first_dep_array.to_value()
	last_dep_array = dep_column.take(LAST_TWO_ROWS)
	last_deps = last_dep_array.to_list()
	assert first_dep == EXPECTED_FIRST_DEP
	assert last_deps == EXPECTED_LAST_DEPS


def test_a_long_csv_file_gives_the_table_of_a_whole_file_reading(tmp_path: Path) -> None:
	"""
	Check that every column, mixed or not, has the type and the values pandas gives when reading the file at once.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_file(tmp_path)
	whole_table = read_whole_file(path)

	table = ndp.Table.from_csv(path, ndp.CsvOptions(separator=SEMICOLON))

	is_same_table = table.is_equal(ndp.Equality(other=whole_table))
	assert is_same_table


def test_a_long_csv_file_with_mixed_columns_emits_no_warning(tmp_path: Path) -> None:
	"""
	Check that the pandas warning about mixed types is not shown to the user.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_long_file(tmp_path)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		ndp.Table.from_csv(path, ndp.CsvOptions(separator=SEMICOLON))

	assert caught_warnings == []
