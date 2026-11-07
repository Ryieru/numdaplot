"""
Functional tests of the number of decimals written in a CSV file.

.. versionadded:: 0.1.0
"""

from datetime import date
from pathlib import Path

import numpy

import numdaplot as ndp

NOISY_SUM = 0.1 + 0.2


def write_csv(table: ndp.Table, tmp_path: Path, options: ndp.CsvWriteOptions) -> str:
	"""
	Return the text of a CSV file written from a Table.

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
	path = tmp_path / "sales.csv"
	table.to_csv(path, options)
	file_text = path.read_text()

	return file_text


def test_decimals_round_and_keep_their_zeros(tmp_path: Path) -> None:
	"""
	Check the values of a decimal column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	table = ndp.Table.from_arrays({"price": ndp.Array.from_list([NOISY_SUM, 1.5, 2.0])})

	file_text = write_csv(table, tmp_path, ndp.CsvWriteOptions(decimals=2))

	assert file_text == "price\n0.30\n1.50\n2.00\n"


def test_zero_decimals_writes_whole_numbers(tmp_path: Path) -> None:
	"""
	Check the lowest number of decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.6])})

	file_text = write_csv(table, tmp_path, ndp.CsvWriteOptions(decimals=0))

	assert file_text == "price\n2\n"


def test_decimals_apply_to_a_single_precision_column(tmp_path: Path) -> None:
	"""
	Check a FLOAT32 column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	values = numpy.array([0.1], dtype=numpy.float32)
	table = ndp.Table.from_arrays({"price": ndp.Array.from_numpy(values)})

	file_text = write_csv(table, tmp_path, ndp.CsvWriteOptions(decimals=3))

	assert file_text == "price\n0.100\n"


def test_decimals_leave_other_columns_and_missing_values(tmp_path: Path) -> None:
	"""
	Check that only the present decimals change.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	table = ndp.Table.from_arrays(
		{
			"price": ndp.Array.from_list([1.5, None]),
			"count": ndp.Array.from_list([3, 4]),
			"city": ndp.Array.from_list(["Paris", "Lyon"]),
			"day": ndp.Array.from_list([date(2026, 1, 2), date(2026, 1, 3)]),
		}
	)

	file_text = write_csv(table, tmp_path, ndp.CsvWriteOptions(decimals=2))

	assert file_text == "price,count,city,day\n1.50,3,Paris,2026-01-02\n,4,Lyon,2026-01-03\n"


def test_decimals_work_with_the_other_settings(tmp_path: Path) -> None:
	"""
	Check the separator with the decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	table = ndp.Table.from_arrays({"a": ndp.Array.from_list([1.5]), "b": ndp.Array.from_list([2.5])})

	file_text = write_csv(table, tmp_path, ndp.CsvWriteOptions(separator=";", decimals=1))

	assert file_text == "a;b\n1.5;2.5\n"


def test_without_decimals_the_file_keeps_every_digit(tmp_path: Path) -> None:
	"""
	Check the text of a decimal when no rounding is asked.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	table = ndp.Table.from_arrays({"price": ndp.Array.from_list([NOISY_SUM])})

	file_text = write_csv(table, tmp_path, ndp.CsvWriteOptions())

	assert file_text == "price\n0.30000000000000004\n"
