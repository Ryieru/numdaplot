"""
Functional tests of the display of a Table.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

PRICE_COUNT = 10
PRICES = [float(price) for price in range(PRICE_COUNT)]
EXPECTED_TABLE_LINES = ["price", "FLOAT64"]
PREVIEW_COUNT = 3
EXPECTED_END_ROWS = ["7", "8", "9"]
HEADER_LINE_COUNT = 2
SEED = 11
ROW_NUMBER_POSITION = 0
TABLE_HTML_START = "<table"


def build_prices() -> ndp.Table:
	"""
	Return a Table of ten prices.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The prices.
	"""
	prices = ndp.Array.from_list(PRICES)
	table = ndp.Table.from_arrays({"price": prices})

	return table


def read_row_numbers(printed_text: str) -> list[str]:
	"""
	Return the row numbers printed under the header.

	.. versionadded:: 0.1.0

	Parameters
	----------
	printed_text
		The printed rows.

	Returns
	-------
	list[str]
		The first word of each row.
	"""
	lines = printed_text.splitlines()
	row_lines = lines[HEADER_LINE_COUNT:]
	row_numbers = list[str]()

	for row_line in row_lines:
		words = row_line.split()
		row_number = words[ROW_NUMBER_POSITION]
		row_numbers.append(row_number)

	return row_numbers


def test_printing_a_table_shows_the_type_under_each_name() -> None:
	"""
	Check the first two lines of the text of a Table.

	.. versionadded:: 0.1.0
	"""
	table = build_prices()

	table_text = repr(table)

	lines = table_text.splitlines()
	first_lines = lines[:HEADER_LINE_COUNT]
	header_lines = [line.strip() for line in first_lines]
	assert header_lines == EXPECTED_TABLE_LINES


def test_a_table_at_the_end_of_a_notebook_cell_shows_an_html_table() -> None:
	"""
	Check that a notebook receives an HTML table with the type under each name.

	.. versionadded:: 0.1.0
	"""
	table = build_prices()

	# Jupyter calls _repr_html_ to show an object written at the end of a cell.
	table_html = table._repr_html_()  # pyright: ignore[reportPrivateUsage]

	assert table_html.startswith(TABLE_HTML_START)
	for expected_text in EXPECTED_TABLE_LINES:
		assert expected_text in table_html


def test_a_preview_prints_the_last_rows_with_their_numbers(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that the last three rows are printed with their row numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed text.
	"""
	table = build_prices()

	table.preview(ndp.Preview(count=PREVIEW_COUNT, side=ndp.Side.END))

	captured = capsys.readouterr()
	row_numbers = read_row_numbers(captured.out)
	assert row_numbers == EXPECTED_END_ROWS


def test_a_random_preview_with_a_seed_shows_the_same_rows(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that two previews with the same seed print the same rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed text.
	"""
	table = build_prices()
	preview = ndp.Preview(count=PREVIEW_COUNT, side=ndp.Side.RANDOM, seed=SEED)

	table.preview(preview)
	first_output = capsys.readouterr()
	table.preview(preview)
	second_output = capsys.readouterr()

	assert first_output.out == second_output.out
