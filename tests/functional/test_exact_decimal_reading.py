"""
Functional tests of decimals read from texts, the same on every version of pandas.

.. versionadded:: 0.1.0
"""

import warnings
from pathlib import Path

import pytest

import numdaplot as ndp

EXACT_DECIMALS = [
	1234567.891,
	0.1,
	0.1 + 0.2,
	1 / 3,
	1e-20,
	1.5e300,
	123456789012.345,
	5e-324,
	1.7976931348623157e308,
	4179.3200000000015,
]
FILE_NAME = "sales.csv"
COLUMN_NAME = "price"


def write_decimals(path: Path) -> None:
	"""
	Write the decimals of the tests in a CSV file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file.
	"""
	prices = ndp.Array.from_list(EXACT_DECIMALS)
	table = ndp.Table.from_arrays({COLUMN_NAME: prices})
	table.to_csv(path)


def test_from_csv_reads_the_exact_decimals_written_by_to_csv(tmp_path: Path) -> None:
	"""
	Check that writing then reading a file keeps every digit.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / FILE_NAME
	write_decimals(path)

	table = ndp.Table.from_csv(path)

	prices = table.column(COLUMN_NAME)
	price_list = prices.to_list()
	assert price_list == EXACT_DECIMALS


def test_from_csv_gives_no_warning_of_pandas(tmp_path: Path) -> None:
	"""
	Check that the setting deprecated by recent versions of pandas is not given to them.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / FILE_NAME
	write_decimals(path)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		ndp.Table.from_csv(path)

	assert caught_warnings == []


def test_from_csv_keeps_missing_values_and_integers(tmp_path: Path) -> None:
	"""
	Check the other columns of a file read exactly.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / FILE_NAME
	path.write_text("count,price\n1,0.30000000000000004\n,\n", encoding="utf-8")

	table = ndp.Table.from_csv(path)

	prices = table.column(COLUMN_NAME)
	missing_prices = prices.check(ndp.IsMissing())
	first_price = prices.to_list()[0]
	missing_list = missing_prices.to_list()
	assert table.column_types["count"] == ndp.Type.INT64
	assert first_price == 0.1 + 0.2
	assert missing_list == [False, True]


def build_texts(texts: list[str | None]) -> ndp.Table:
	"""
	Return a Table with a column of texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		The texts.

	Returns
	-------
	ndp.Table
		The column ``price``.
	"""
	column = ndp.Array.from_list(texts)
	table = ndp.Table.from_arrays({COLUMN_NAME: column})

	return table


def test_convert_reads_the_exact_decimals_of_texts() -> None:
	"""
	Check every digit of texts read as ``FLOAT64``.

	.. versionadded:: 0.1.0
	"""
	texts = list[str | None]([repr(decimal) for decimal in EXACT_DECIMALS])
	table = build_texts(texts)
	conversion = ndp.TableConversion(columns=[COLUMN_NAME], dtype=ndp.Type.FLOAT64)

	converted_table = table.convert(conversion)

	prices = converted_table.column(COLUMN_NAME)
	price_list = prices.to_list()
	assert price_list == EXACT_DECIMALS


def test_convert_keeps_missing_texts_missing_with_exact_decimals() -> None:
	"""
	Check that positions stay right around a missing text.

	.. versionadded:: 0.1.0
	"""
	table = build_texts([None, "0.30000000000000004", " 1e3 "])
	conversion = ndp.TableConversion(columns=[COLUMN_NAME], dtype=ndp.Type.FLOAT64)

	converted_table = table.convert(conversion)

	prices = converted_table.column(COLUMN_NAME)
	missing_prices = prices.check(ndp.IsMissing())
	price_list = prices.to_list()
	missing_list = missing_prices.to_list()
	assert price_list[1:] == [0.1 + 0.2, 1000.0]
	assert missing_list == [True, False, False]


def test_convert_still_refuses_a_text_that_is_not_a_number() -> None:
	"""
	Check that the exact reading only looks at texts already accepted.

	.. versionadded:: 0.1.0
	"""
	table = build_texts(["1.5", "abc"])
	conversion = ndp.TableConversion(columns=[COLUMN_NAME], dtype=ndp.Type.FLOAT64)

	with pytest.raises(ndp.ValueConversionError):
		table.convert(conversion)


@pytest.mark.parametrize("text", ["inf", "-inf"])
def test_convert_reads_infinite_texts(text: str) -> None:
	"""
	Check texts pandas accepts as infinite values.

	.. versionadded:: 0.1.0
	"""
	table = build_texts([text])
	conversion = ndp.TableConversion(columns=[COLUMN_NAME], dtype=ndp.Type.FLOAT64)

	converted_table = table.convert(conversion)

	prices = converted_table.column(COLUMN_NAME)
	price_list = prices.to_list()
	assert price_list == [float(text)]
