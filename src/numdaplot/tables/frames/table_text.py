"""
Text of a Table, with the type of each column under its name.

.. versionadded:: 0.1.0
"""

from shutil import get_terminal_size

import pandas

from numdaplot.column_storage.column_values import find_column_type
from numdaplot.column_storage.time_columns import is_time_column, write_time_texts_column
from numdaplot.column_storage.time_zones import name_column_type
from numdaplot.tables.preview.shown_columns import ShownColumns

MAX_COLUMNS_OPTION = "display.max_columns"
WIDTH_OPTION = "display.width"
# In pandas, no limit shows every column, and a limit of 0 only shows those fitting in the width.
NO_ROWS_NOTE = "(0 rows)"
NO_COLUMNS_NOTE = "(no columns, {rows_text})"
ONE_ROW_TEXT = "1 row"
ROWS_TEXT = "{row_count} rows"
BLANK_CELL = ""
BLANK_ROW_START = "0"
LINE_BREAK = "\n"
SHOW_DIMENSIONS_OPTION = "display.show_dimensions"
COLUMN_LIMITS = {
	ShownColumns.ALL: None,
	ShownColumns.COMPACT: 0,
}


def build_typed_frame(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return a copy of the columns of a Table whose header shows the name, then the type, of each column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	pandas.DataFrame
		A copy with a two-level header: the column names, then the names of their ``ndp.Type``, followed by
		the time zone of a datetime column that has one.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.table_text import build_typed_frame
	>>> build_typed_frame(pandas.DataFrame({"price": [1.5]})).columns.tolist()
	[('price', 'FLOAT64')]
	"""
	column_names = list(frame.columns)
	type_names = list[str]()

	for column_name in column_names:
		column = frame[column_name]
		column_type = find_column_type(column)
		type_name = name_column_type(column, column_type)
		type_names.append(type_name)

	header = pandas.MultiIndex.from_arrays([column_names, type_names])
	typed_frame = frame.copy()
	for column_name in column_names:
		column = frame[column_name]
		if is_time_column(column):
			typed_frame[column_name] = write_time_texts_column(column)

	typed_frame.columns = header

	return typed_frame


def format_table(frame: pandas.DataFrame, shown_columns: ShownColumns = ShownColumns.ALL) -> str:
	"""
	Return the text pandas shows for the columns of a Table, with the type of each column under its name.

	A long Table only shows its first and last rows, following the pandas display settings. The columns follow the
	width of the terminal, whatever the pandas display settings.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	shown_columns
		``ShownColumns.ALL`` by default for every column, going on after a line break when they do not fit, or
		``ShownColumns.COMPACT`` to replace those that do not fit by ``...``.

	Returns
	-------
	str
		The text of the Table, with row numbers on the left.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.table_text import format_table
	>>> print(format_table(pandas.DataFrame({"price": [1.5, 8.0]})))
	    price
	  FLOAT64
	0     1.5
	1     8.0
	"""
	empty_table_text = format_empty_table(frame, shown_columns)
	if empty_table_text is not None:
		return empty_table_text

	typed_frame = build_typed_frame(frame)
	column_limit = COLUMN_LIMITS[shown_columns]
	terminal_size = get_terminal_size()
	with pandas.option_context(MAX_COLUMNS_OPTION, column_limit, WIDTH_OPTION, terminal_size.columns):
		table_text = repr(typed_frame)

	return table_text


def write_empty_table_note(frame: pandas.DataFrame) -> str | None:
	"""
	Return the note replacing the rows of a Table without rows or without columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	str or None
		``(0 rows)``, ``(no columns, 2 rows)``, or None for a Table with values.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.table_text import write_empty_table_note
	>>> write_empty_table_note(pandas.DataFrame({"price": [1.5]})) is None
	True
	>>> write_empty_table_note(pandas.DataFrame(index=[0, 1]))
	'(no columns, 2 rows)'
	>>> write_empty_table_note(pandas.DataFrame(index=[0]))
	'(no columns, 1 row)'
	"""
	row_count = len(frame.index)
	column_count = len(frame.columns)
	if column_count == 0:
		rows_text = ONE_ROW_TEXT if row_count == 1 else ROWS_TEXT.format(row_count=row_count)
		no_columns_note = NO_COLUMNS_NOTE.format(rows_text=rows_text)
		return no_columns_note

	if row_count == 0:
		return NO_ROWS_NOTE

	return None


def format_empty_table(frame: pandas.DataFrame, shown_columns: ShownColumns) -> str | None:
	"""
	Return the text of a Table without rows or without columns: its header if any, then a note.

	pandas writes such a Table with its own words, so the header comes from a Table of one blank row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	shown_columns
		``ShownColumns.ALL`` for every column, or ``ShownColumns.COMPACT`` to replace those that do not fit by ``...``.

	Returns
	-------
	str or None
		The text, or None for a Table with values.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.table_text import format_empty_table
	>>> from numdaplot.tables.preview.shown_columns import ShownColumns
	>>> prices = pandas.DataFrame({"price": pandas.Series(dtype="float64")})
	>>> print(format_empty_table(prices, ShownColumns.ALL))
	    price
	  FLOAT64
	(0 rows)
	"""
	note = write_empty_table_note(frame)
	if note is None:
		return None

	column_count = len(frame.columns)
	if column_count == 0:
		return note

	typed_frame = build_typed_frame(frame)
	blank_row = [[BLANK_CELL] * column_count]
	blank_frame = pandas.DataFrame(blank_row, columns=typed_frame.columns)
	column_limit = COLUMN_LIMITS[shown_columns]
	terminal_size = get_terminal_size()
	with pandas.option_context(
		MAX_COLUMNS_OPTION,
		column_limit,
		WIDTH_OPTION,
		terminal_size.columns,
		SHOW_DIMENSIONS_OPTION,
		False,
	):
		blank_text = repr(blank_frame)

	lines = blank_text.splitlines()
	header_lines = [line for line in lines if not line.startswith(BLANK_ROW_START)]
	empty_table_lines = [*header_lines, note]
	empty_table_text = LINE_BREAK.join(empty_table_lines)

	return empty_table_text
