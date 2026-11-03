"""
Unit tests of the reading and writing of Stata files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas

from numdaplot.tables.files.stata_file import read_stata_file, write_stata_file

FILE_NAME = "sales.dta"
PRICES = {"price": [1.5, 8.0]}
EXPECTED_PRICES = [1.5, 8.0]
EXPECTED_COLUMN_NAMES = ["price"]


def test_stata_file_gives_back_its_columns_without_row_numbers(tmp_path: Path) -> None:
	"""
	Check that a written Stata file is read back with the same column and values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(PRICES)

	write_stata_file(frame, path)
	read_frame = read_stata_file(path)

	column_names = list(read_frame.columns)
	price_column = read_frame["price"]
	prices = price_column.tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert prices == EXPECTED_PRICES
