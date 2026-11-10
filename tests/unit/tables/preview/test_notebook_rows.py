"""
Unit tests of the rows of the HTML table shown in a notebook.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.tables.preview.notebook_display import find_shown_row_count, format_table_html
from numdaplot.tables.preview.shown_columns import ShownColumns

MAX_ROWS_OPTION = "display.max_rows"
MIN_ROWS_OPTION = "display.min_rows"
MAX_ROWS = 60
MIN_ROWS = 10
SHORT_ROW_COUNT = 3
LONG_ROW_COUNT = 1000
FIRST_ROW_HTML = "<th>0</th>"
LAST_ROW_HTML = "<th>999</th>"
MIDDLE_ROW_HTML = "<th>500</th>"
LONG_SIZE_TEXT = "1000 rows"
SIZE_TEXT = " rows "
ROW_HTML = "<tr>"
HEADER_ROW_COUNT = 2


def build_price_frame(row_count: int) -> pandas.DataFrame:
	"""
	Return a frame of one price column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row_count
		The number of rows.

	Returns
	-------
	pandas.DataFrame
		The prices 0.0, 1.0, 2.0...
	"""
	row_numbers = range(row_count)
	prices = [float(row_number) for row_number in row_numbers]
	frame = pandas.DataFrame({"price": prices})

	return frame


def test_format_table_html_shows_every_row_of_a_short_table() -> None:
	"""
	Check that a short Table shows all its rows and not its size.

	.. versionadded:: 0.1.0
	"""
	frame = build_price_frame(SHORT_ROW_COUNT)

	table_html = format_table_html(frame, ShownColumns.ALL)

	row_html_count = table_html.count(ROW_HTML)
	assert row_html_count == HEADER_ROW_COUNT + SHORT_ROW_COUNT
	assert SIZE_TEXT not in table_html


def test_format_table_html_shows_the_first_and_last_rows_of_a_long_table() -> None:
	"""
	Check that a long Table only shows its first and last rows, then its size.

	.. versionadded:: 0.1.0
	"""
	frame = build_price_frame(LONG_ROW_COUNT)

	with pandas.option_context(MAX_ROWS_OPTION, MAX_ROWS, MIN_ROWS_OPTION, MIN_ROWS):
		table_html = format_table_html(frame, ShownColumns.ALL)

	assert FIRST_ROW_HTML in table_html
	assert LAST_ROW_HTML in table_html
	assert MIDDLE_ROW_HTML not in table_html
	assert LONG_SIZE_TEXT in table_html


def test_format_table_html_shows_every_row_without_a_pandas_row_limit() -> None:
	"""
	Check that a long Table shows all its rows when pandas sets no row limit.

	.. versionadded:: 0.1.0
	"""
	frame = build_price_frame(LONG_ROW_COUNT)

	with pandas.option_context(MAX_ROWS_OPTION, None):
		table_html = format_table_html(frame, ShownColumns.ALL)

	assert MIDDLE_ROW_HTML in table_html
	assert SIZE_TEXT not in table_html


def test_find_shown_row_count_shows_every_row_up_to_the_limit() -> None:
	"""
	Check that a Table of exactly the row limit shows every row.

	.. versionadded:: 0.1.0
	"""
	with pandas.option_context(MAX_ROWS_OPTION, MAX_ROWS, MIN_ROWS_OPTION, MIN_ROWS):
		shown_row_count = find_shown_row_count(MAX_ROWS)

	assert shown_row_count is None


def test_find_shown_row_count_gives_the_pandas_minimum_beyond_the_limit() -> None:
	"""
	Check that a Table longer than the row limit shows the pandas minimum of rows.

	.. versionadded:: 0.1.0
	"""
	with pandas.option_context(MAX_ROWS_OPTION, MAX_ROWS, MIN_ROWS_OPTION, MIN_ROWS):
		shown_row_count = find_shown_row_count(LONG_ROW_COUNT)

	assert shown_row_count == MIN_ROWS


def test_find_shown_row_count_gives_the_limit_without_a_minimum() -> None:
	"""
	Check that a long Table shows the row limit when pandas sets no minimum.

	.. versionadded:: 0.1.0
	"""
	with pandas.option_context(MAX_ROWS_OPTION, MAX_ROWS, MIN_ROWS_OPTION, None):
		shown_row_count = find_shown_row_count(LONG_ROW_COUNT)

	assert shown_row_count == MAX_ROWS


def test_find_shown_row_count_keeps_a_minimum_below_the_limit() -> None:
	"""
	Check that a minimum above the row limit shows the row limit.

	.. versionadded:: 0.1.0
	"""
	with pandas.option_context(MAX_ROWS_OPTION, MIN_ROWS, MIN_ROWS_OPTION, MAX_ROWS):
		shown_row_count = find_shown_row_count(LONG_ROW_COUNT)

	assert shown_row_count == MIN_ROWS


def test_find_shown_row_count_shows_every_row_without_a_limit() -> None:
	"""
	Check that pandas without a row limit shows every row.

	.. versionadded:: 0.1.0
	"""
	with pandas.option_context(MAX_ROWS_OPTION, None):
		shown_row_count = find_shown_row_count(LONG_ROW_COUNT)

	assert shown_row_count is None
