"""
Functional tests of reading and writing Tables in files.

pandas cannot write SAS files, so the SAS data and SAS transport tests read two sample files of tests/data,
copied from the test files of pandas 2.3.0 (BSD-3-Clause, Copyright the pandas development team).

.. versionadded:: 0.1.0
"""

import builtins
from pathlib import Path

import pytest

import numdaplot as ndp

CSV_NAME = "sales.csv"
SALES_CSV = "city;count;price;paid;day\nParis;2;1.5;True;2026-01-31\nLyon;;8.0;False;\n"
EXPECTED_CSV_TYPES = {
	"city": ndp.Type.TEXT,
	"count": ndp.Type.INT64,
	"price": ndp.Type.FLOAT64,
	"paid": ndp.Type.BOOL,
	"day": ndp.Type.TEXT,
}
EXPECTED_ROW_COUNT = 2
SEMICOLON = ";"
JSON_NAME = "sales.json"
JSONL_NAME = "sales.jsonl"
PARQUET_NAME = "sales.parquet"
EXCEL_NAME = "sales.xlsx"
STATA_NAME = "sales.dta"
PRICES = [1.5, 8.0]
COUNTS = [3.0, None]
REPLACED_PRICES = [2.5]
MISSING_SAS_NAME = "missing.sas7bdat"
MISSING_XPT_NAME = "missing.xpt"
SHEET_NAME = "Sales"
DATA_FOLDER = Path(__file__).parent.parent / "data"
AIRLINE_PATH = DATA_FOLDER / "airline.sas7bdat"
EXPECTED_AIRLINE_ROW_COUNT = 32
EXPECTED_AIRLINE_COLUMNS = ["YEAR", "Y", "W", "R", "L", "K"]
EXPECTED_FIRST_YEAR = 1948.0
ACTIVITY_PATH = DATA_FOLDER / "paxraw_d_short.xpt"
EXPECTED_ACTIVITY_ROW_COUNT = 100
EXPECTED_FIRST_SEQUENCE = 31128.0
FIRST_ROW = ndp.Index(0)


def build_sales() -> ndp.Table:
	"""
	Return a Table of two sales with a missing city and a missing count.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The sales.
	"""
	cities = ndp.Array.from_list(["Paris", "Lyon"])
	prices = ndp.Array.from_list(PRICES)
	counts = ndp.Array.from_list(COUNTS)
	sales = ndp.Table.from_arrays({"city": cities, "price": prices, "count": counts})

	return sales


def test_a_csv_file_gives_a_type_to_each_column(tmp_path: Path) -> None:
	"""
	Check the guessed types: integers with a hole stay integers and dates stay texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / CSV_NAME
	path.write_text(SALES_CSV)

	sales = ndp.Table.from_csv(path, ndp.CsvReadOptions(separator=SEMICOLON))

	assert sales.column_types == EXPECTED_CSV_TYPES
	assert sales.row_count == EXPECTED_ROW_COUNT


def test_a_table_written_in_csv_reads_back_the_same(tmp_path: Path) -> None:
	"""
	Check that writing then reading a CSV file gives an equal Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / CSV_NAME
	sales = build_sales()

	sales.to_csv(path)
	read_sales = ndp.Table.from_csv(path)

	is_equal = read_sales.is_equal(ndp.Equality(other=sales))
	assert is_equal


@pytest.mark.parametrize(
	("file_name", "layout"),
	[
		(JSON_NAME, ndp.JsonLayout.RECORDS),
		(JSONL_NAME, ndp.JsonLayout.LINES),
	],
)
def test_a_table_written_in_json_reads_back_the_same(tmp_path: Path, file_name: str, layout: ndp.JsonLayout) -> None:
	"""
	Check that both JSON layouts give back an equal Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	file_name
		The name of the file.
	layout
		The layout of the rows.
	"""
	path = tmp_path / file_name
	sales = build_sales()
	write_options = ndp.JsonWriteOptions(layout=layout)
	read_options = ndp.JsonReadOptions(layout=layout)

	sales.to_json(path, write_options)
	read_sales = ndp.Table.from_json(path, read_options)

	is_equal = read_sales.is_equal(ndp.Equality(other=sales))
	assert is_equal


def test_a_parquet_file_keeps_every_type(tmp_path: Path) -> None:
	"""
	Check that a Parquet file gives back the same types, categories included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / PARQUET_NAME
	sales = build_sales()
	category_sales = sales.convert(ndp.Conversion(column="city", dtype=ndp.Type.CATEGORY))

	category_sales.to_parquet(path)
	read_sales = ndp.Table.from_parquet(path)

	is_equal = read_sales.is_equal(ndp.Equality(other=category_sales, types=ndp.TypeMatch.STRICT))
	assert is_equal


def test_an_excel_sheet_reads_back_the_same(tmp_path: Path) -> None:
	"""
	Check that a named Excel sheet gives back an equal Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / EXCEL_NAME
	sales = build_sales()
	write_options = ndp.ExcelWriteOptions(sheet=SHEET_NAME)
	read_options = ndp.ExcelReadOptions(sheet=SHEET_NAME)

	sales.to_excel(path, write_options)
	read_sales = ndp.Table.from_excel(path, read_options)

	is_equal = read_sales.is_equal(ndp.Equality(other=sales))
	assert is_equal


def test_a_stata_file_reads_back_its_numbers(tmp_path: Path) -> None:
	"""
	Check that the prices of a Stata file come back unchanged.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / STATA_NAME
	sales = build_sales()

	sales.to_stata(path)
	read_sales = ndp.Table.from_stata(path)

	prices = read_sales.column("price")
	price_list = prices.to_list()
	assert price_list == PRICES


def test_an_existing_file_is_kept_unless_replaced(tmp_path: Path) -> None:
	"""
	Check that a second write raises FileExistsError, and REPLACE overwrites.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / CSV_NAME
	sales = build_sales()
	sales.to_csv(path)
	new_prices = ndp.Array.from_list(REPLACED_PRICES)
	new_sales = ndp.Table.from_arrays({"price": new_prices})

	with pytest.raises(ndp.FileExistsError):
		new_sales.to_csv(path)

	new_sales.to_csv(path, on_conflict=ndp.Conflict.REPLACE)
	read_sales = ndp.Table.from_csv(path)
	prices = read_sales.column("price")
	price_list = prices.to_list()
	assert price_list == REPLACED_PRICES


def test_a_missing_sas_file_is_caught_as_the_python_error(tmp_path: Path) -> None:
	"""
	Check that code catching the Python FileNotFoundError catches a missing SAS data file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / MISSING_SAS_NAME

	with pytest.raises(builtins.FileNotFoundError):
		ndp.Table.from_sas(path)


def test_a_missing_xpt_file_is_caught_as_a_numdaplot_error(tmp_path: Path) -> None:
	"""
	Check that code catching NumdaplotError catches a missing XPT file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / MISSING_XPT_NAME

	with pytest.raises(ndp.NumdaplotError):
		ndp.Table.from_xpt(path)


def test_a_sas_data_file_gives_its_columns_as_decimals() -> None:
	"""
	Check the size, the column names and the first year of a real SAS data file.

	.. versionadded:: 0.1.0
	"""
	airline = ndp.Table.from_sas(AIRLINE_PATH)

	first_year = airline.take(ndp.Region(rows=FIRST_ROW, columns=["YEAR"]))
	first_year_value = first_year.to_value()
	column_types = set(airline.column_types.values())
	assert airline.row_count == EXPECTED_AIRLINE_ROW_COUNT
	assert airline.column_names == EXPECTED_AIRLINE_COLUMNS
	assert column_types == {ndp.Type.FLOAT64}
	assert first_year_value == EXPECTED_FIRST_YEAR


def test_a_sas_transport_file_gives_its_rows() -> None:
	"""
	Check the size and the first sequence number of a real XPT file.

	.. versionadded:: 0.1.0
	"""
	activity = ndp.Table.from_xpt(ACTIVITY_PATH)

	first_sequence = activity.take(ndp.Region(rows=FIRST_ROW, columns=["SEQN"]))
	first_sequence_value = first_sequence.to_value()
	assert activity.row_count == EXPECTED_ACTIVITY_ROW_COUNT
	assert first_sequence_value == EXPECTED_FIRST_SEQUENCE
