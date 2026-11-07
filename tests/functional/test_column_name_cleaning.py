"""
Functional tests of the cleaning of the column names a Table reads.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas
import pytest

import numdaplot as ndp

SEMICOLON = ";"
VEHICLES_CSV = '"id_vehicule\n"; catv ;speed\n1;7;50\n'
EXPECTED_CLEANED_NAMES = ["id_vehicule", "catv", "speed"]
EXPECTED_KEPT_NAMES = ["id_vehicule\n", " catv ", "speed"]
COLLIDING_CSV = "id,id \n1,2\n"
EXPECTED_COLLISION_MESSAGE = (
	"The column names 'id' and 'id ' both become 'id' once cleaned. Use ColumnNames.KEPT to keep them as written."
)
BLANK_NAME_CSV = "id,  \n1,2\n"
EXPECTED_BLANK_MESSAGE = "Expected a column name as a non-empty text, got ''."
SPACED_JSON = '[{" city ": "Paris", "count\\n": 2}]'
EXPECTED_JSON_NAMES = ["city", "count"]
SPACED_NAME = " price "
CLEANED_NAME = "price"
SPEEDS = [50, 80]


def write_file(tmp_path: Path, file_name: str, content: str) -> Path:
	"""
	Write a text file and return its path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	file_name
		The name of the file.
	content
		Its text.

	Returns
	-------
	Path
		The path of the file.
	"""
	path = tmp_path / file_name
	path.write_text(content)

	return path


def build_spaced_prices() -> ndp.Table:
	"""
	Return a Table whose only column name has spaces around it.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The Table.
	"""
	prices = ndp.Array.from_list([1.5])
	table = ndp.Table.from_arrays({SPACED_NAME: prices})

	return table


def test_a_csv_header_with_line_breaks_and_spaces_is_cleaned(tmp_path: Path) -> None:
	"""
	Check that a BAAC-like header loses the line break and the spaces around its names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_file(tmp_path, "vehicles.csv", VEHICLES_CSV)

	vehicles = ndp.Table.from_csv(path, ndp.CsvReadOptions(separator=SEMICOLON))

	assert vehicles.column_names == EXPECTED_CLEANED_NAMES


def test_a_csv_header_is_kept_as_written_when_asked(tmp_path: Path) -> None:
	"""
	Check that ColumnNames.KEPT keeps every name as written.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_file(tmp_path, "vehicles.csv", VEHICLES_CSV)
	options = ndp.CsvReadOptions(separator=SEMICOLON, column_names=ndp.ColumnNames.KEPT)

	vehicles = ndp.Table.from_csv(path, options)

	assert vehicles.column_names == EXPECTED_KEPT_NAMES


def test_two_names_that_become_the_same_are_both_named(tmp_path: Path) -> None:
	"""
	Check the message of two names that differ only by a space.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_file(tmp_path, "ids.csv", COLLIDING_CSV)

	with pytest.raises(ndp.DuplicateColumnError) as error_info:
		ndp.Table.from_csv(path)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_COLLISION_MESSAGE


def test_a_name_made_of_spaces_is_refused_once_cleaned(tmp_path: Path) -> None:
	"""
	Check that a name holding only spaces becomes empty and raises InvalidColumnNameError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_file(tmp_path, "ids.csv", BLANK_NAME_CSV)

	with pytest.raises(ndp.InvalidColumnNameError) as error_info:
		ndp.Table.from_csv(path)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_BLANK_MESSAGE


def test_json_keys_are_cleaned(tmp_path: Path) -> None:
	"""
	Check that the keys of a JSON file lose their spaces and line breaks.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = write_file(tmp_path, "cities.json", SPACED_JSON)

	cities = ndp.Table.from_json(path)

	assert cities.column_names == EXPECTED_JSON_NAMES


def test_an_excel_header_is_cleaned(tmp_path: Path) -> None:
	"""
	Check that the first row of an Excel sheet loses the spaces around its names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / "prices.xlsx"
	spaced_prices = build_spaced_prices()
	spaced_prices.to_excel(path)

	prices = ndp.Table.from_excel(path)

	assert prices.column_names == [CLEANED_NAME]


def test_a_parquet_file_is_cleaned_unless_kept(tmp_path: Path) -> None:
	"""
	Check that Parquet names are cleaned by default and kept with ParquetReadOptions.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / "prices.parquet"
	spaced_prices = build_spaced_prices()
	spaced_prices.to_parquet(path)
	kept_options = ndp.ParquetReadOptions(column_names=ndp.ColumnNames.KEPT)

	cleaned_prices = ndp.Table.from_parquet(path)
	kept_prices = ndp.Table.from_parquet(path, kept_options)

	assert cleaned_prices.column_names == [CLEANED_NAME]
	assert kept_prices.column_names == [SPACED_NAME]


def test_a_pandas_dataframe_is_cleaned_unless_kept() -> None:
	"""
	Check that from_pandas cleans the names by default and keeps them with ColumnNames.KEPT.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({SPACED_NAME: SPEEDS})

	cleaned_table = ndp.Table.from_pandas(frame)
	kept_table = ndp.Table.from_pandas(frame, ndp.ColumnNames.KEPT)

	assert cleaned_table.column_names == [CLEANED_NAME]
	assert kept_table.column_names == [SPACED_NAME]


def test_arrays_keep_the_names_written_in_the_code() -> None:
	"""
	Check that from_arrays never cleans the names.

	.. versionadded:: 0.1.0
	"""
	table = build_spaced_prices()

	assert table.column_names == [SPACED_NAME]
