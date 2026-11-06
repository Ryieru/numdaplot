"""
Functional tests of the decimals written in a JSON file.

.. versionadded:: 0.1.0
"""

import json
from datetime import date
from pathlib import Path

import numpy
import pytest

import numdaplot as ndp

LOWER_THIRD = 1 / 3
NOISY_SUM = 0.1 + 0.2
LARGE_DECIMAL = 1234567.891
TINY_DECIMAL = 5e-324
HUGE_DECIMAL = 1.7976931348623157e308
EXACT_DECIMALS = [LOWER_THIRD, NOISY_SUM, LARGE_DECIMAL, TINY_DECIMAL, HUGE_DECIMAL, 100.0]
FILE_NAME = "sales.json"
SINGLE_PRECISION = 0.1
INFINITE_MESSAGE = "Cannot store the FLOAT64 value inf of the column 'price' as JSON without losing information."
NEGATIVE_INFINITE_MESSAGE = (
	"Cannot store the FLOAT64 value -inf of the column 'price' as JSON without losing information."
)
READ_REFUSAL = "Table.from_json does not accept decimals."
LINES_OPTIONS = ndp.JsonOptions(layout=ndp.JsonLayout.LINES)
ROUNDED_OPTIONS = ndp.JsonOptions(decimals=2)


def build_prices(values: list[float | None], dtype: ndp.Type | None = None) -> ndp.Table:
	"""
	Return a Table with a column of decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The decimals.
	dtype
		The type of the column, guessed when omitted.

	Returns
	-------
	ndp.Table
		The column ``price``.
	"""
	prices = ndp.Array.from_list(values, dtype=dtype)
	table = ndp.Table.from_arrays({"price": prices})

	return table


def write_text(table: ndp.Table, tmp_path: Path, options: ndp.JsonOptions | None = None) -> str:
	"""
	Return the text of a JSON file written from a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table.
	tmp_path
		A temporary folder.
	options
		The settings of the file.

	Returns
	-------
	str
		The text of the file.
	"""
	path = tmp_path / FILE_NAME
	table.to_json(path, options)
	file_text = path.read_text(encoding="utf-8")

	return file_text


def test_decimals_come_back_exactly_after_a_file(tmp_path: Path) -> None:
	"""
	Check that writing then reading a file keeps every digit.

	.. versionadded:: 0.1.0
	"""
	table = build_prices(list[float | None](EXACT_DECIMALS))
	path = tmp_path / FILE_NAME
	table.to_json(path)

	read_table = ndp.Table.from_json(path)

	read_prices = read_table.column("price")
	read_list = read_prices.to_list()
	assert read_list == EXACT_DECIMALS


def test_decimals_are_written_in_their_shortest_form(tmp_path: Path) -> None:
	"""
	Check that a decimal shows no digit beyond what gives its value.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([LARGE_DECIMAL])

	file_text = write_text(table, tmp_path)

	assert file_text == '[{"price":1234567.891}]'


def test_a_single_precision_decimal_is_written_in_its_shortest_form(tmp_path: Path) -> None:
	"""
	Check that ``FLOAT32`` does not show the digits of its value in 64 bits.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([SINGLE_PRECISION, None], ndp.Type.FLOAT32)

	file_text = write_text(table, tmp_path)

	assert file_text == '[{"price":0.1},{"price":null}]'


def test_a_missing_decimal_is_written_as_null(tmp_path: Path) -> None:
	"""
	Check missing values, without an error for infinite ones.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([None, 1.5])

	file_text = write_text(table, tmp_path)

	assert file_text == '[{"price":null},{"price":1.5}]'


def test_columns_stay_in_their_order_with_every_type(tmp_path: Path) -> None:
	"""
	Check columns of decimals between other columns, and what pandas writes for the others.

	.. versionadded:: 0.1.0
	"""
	columns = {
		"city": ndp.Array.from_list(['Par"is\né']),
		"price": ndp.Array.from_list([LOWER_THIRD]),
		"count": ndp.Array.from_list([2]),
		"day": ndp.Array.from_list([date(2026, 1, 31)]),
		"cost": ndp.Array.from_list([NOISY_SUM]),
	}
	table = ndp.Table.from_arrays(columns)

	file_text = write_text(table, tmp_path)

	records = json.loads(file_text)
	assert list(records[0]) == list(columns)
	assert records[0]["city"] == 'Par"is\né'
	assert records[0]["price"] == LOWER_THIRD
	assert records[0]["count"] == 2
	assert records[0]["day"] == "2026-01-31T00:00:00.000"
	assert records[0]["cost"] == NOISY_SUM


def test_a_table_without_decimals_keeps_the_same_text(tmp_path: Path) -> None:
	"""
	Check a Table whose writing goes on with pandas alone.

	.. versionadded:: 0.1.0
	"""
	table = ndp.Table.from_arrays({"count": ndp.Array.from_list([1, 2])})

	file_text = write_text(table, tmp_path)

	assert file_text == '[{"count":1},{"count":2}]'


def test_one_object_per_line_ends_each_line(tmp_path: Path) -> None:
	"""
	Check the layout of one object per line, as pandas writes it.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([1.5, 2.5])

	file_text = write_text(table, tmp_path, LINES_OPTIONS)

	assert file_text == '{"price":1.5}\n{"price":2.5}\n'


@pytest.mark.parametrize("options", [None, LINES_OPTIONS])
def test_a_table_of_decimals_without_row_gives_a_file_without_row(
	tmp_path: Path, options: ndp.JsonOptions | None
) -> None:
	"""
	Check that a file without row can be read again.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list([], dtype=ndp.Type.FLOAT64)
	table = ndp.Table.from_arrays({"price": prices})
	path = tmp_path / FILE_NAME

	table.to_json(path, options)

	read_table = ndp.Table.from_json(path, options)
	assert read_table.column_names == []


@pytest.mark.parametrize(
	("value", "expected_message"),
	[(numpy.inf, INFINITE_MESSAGE), (-numpy.inf, NEGATIVE_INFINITE_MESSAGE)],
)
def test_an_infinite_decimal_is_refused(tmp_path: Path, value: float, expected_message: str) -> None:
	"""
	Check that JSON does not turn an infinite value into a missing one.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([1.5, value])

	with pytest.raises(ndp.ValueConversionError) as error_info:
		write_text(table, tmp_path)

	error_text = str(error_info.value)
	assert error_text == expected_message


def test_an_infinite_decimal_is_refused_with_rounded_decimals(tmp_path: Path) -> None:
	"""
	Check that the number of decimals does not change the refusal.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([numpy.inf])

	with pytest.raises(ndp.ValueConversionError):
		write_text(table, tmp_path, ROUNDED_OPTIONS)


def test_a_refusal_leaves_an_existing_file_as_it_was(tmp_path: Path) -> None:
	"""
	Check that nothing is written before the refusal.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / FILE_NAME
	build_prices([1.5]).to_json(path)
	table = build_prices([numpy.inf])

	with pytest.raises(ndp.ValueConversionError):
		table.to_json(path, on_conflict=ndp.Conflict.REPLACE)

	file_text = path.read_text()
	assert file_text == '[{"price":1.5}]'


def test_decimals_round_and_keep_their_zeros(tmp_path: Path) -> None:
	"""
	Check ``decimals`` as in a CSV file.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([NOISY_SUM, 1.5, None])

	file_text = write_text(table, tmp_path, ROUNDED_OPTIONS)

	assert file_text == '[{"price":0.30},{"price":1.50},{"price":null}]'


def test_no_decimal_writes_whole_numbers(tmp_path: Path) -> None:
	"""
	Check the lowest number of decimals.

	.. versionadded:: 0.1.0
	"""
	table = build_prices([2.5, 3.6])
	options = ndp.JsonOptions(decimals=0)

	file_text = write_text(table, tmp_path, options)

	assert file_text == '[{"price":2},{"price":4}]'


def test_decimals_leave_other_columns_alone(tmp_path: Path) -> None:
	"""
	Check that integers keep their digits.

	.. versionadded:: 0.1.0
	"""
	table = ndp.Table.from_arrays({"count": ndp.Array.from_list([3]), "price": ndp.Array.from_list([1.5])})

	file_text = write_text(table, tmp_path, ROUNDED_OPTIONS)

	assert file_text == '[{"count":3,"price":1.50}]'


def test_negative_decimals_are_refused() -> None:
	"""
	Check the setting itself.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidCountError):
		ndp.JsonOptions(decimals=-1)


def test_reading_refuses_decimals(tmp_path: Path) -> None:
	"""
	Check that ``decimals`` only applies to the writing.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / FILE_NAME
	build_prices([1.5]).to_json(path)

	with pytest.raises(ndp.RefusedSettingError) as error_info:
		ndp.Table.from_json(path, ROUNDED_OPTIONS)

	error_text = str(error_info.value)
	assert error_text == READ_REFUSAL
