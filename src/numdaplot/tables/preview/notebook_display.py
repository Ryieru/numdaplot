"""
Display of a Table in a terminal or in a Jupyter notebook.

.. versionadded:: 0.1.0
"""

from importlib import import_module
from importlib.util import find_spec

import pandas

from numdaplot.tables.frames.table_text import build_typed_frame, format_table, write_empty_table_note
from numdaplot.tables.preview.shown_columns import ShownColumns

IPYTHON_PACKAGE = "IPython"
IPYTHON_DISPLAY_MODULE = "IPython.display"
NOTEBOOK_KERNEL = "IPKernelApp"
COMPACT_NOTEBOOK_COLUMN_COUNT = 10
NOTE_HTML = "<p>{note}</p>"
MAX_ROWS_OPTION = "display.max_rows"
MIN_ROWS_OPTION = "display.min_rows"


def show_frame(frame: pandas.DataFrame, shown_columns: ShownColumns) -> None:
	"""
	Show the columns of a Table: as an HTML table in a Jupyter notebook, as text anywhere else.

	The type of each column is shown under its name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The rows to show.
	shown_columns
		Whether every column is shown. A compact HTML table shows 10 columns.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.preview.notebook_display import show_frame
	>>> show_frame(pandas.DataFrame({"price": [1.5]}), ndp.ShownColumns.ALL)
	    price
	  FLOAT64
	0     1.5
	"""
	runs_in_notebook = is_notebook()
	if not runs_in_notebook:
		table_text = format_table(frame, shown_columns)
		print(table_text)
		return

	table_html = format_table_html(frame, shown_columns)
	display_html(table_html)


def format_table_html(frame: pandas.DataFrame, shown_columns: ShownColumns) -> str:
	"""
	Return the HTML table of the columns of a Table, with the type of each column under its name.

	A long Table only shows its first and last rows, following the pandas display settings, as its text does.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	shown_columns
		Whether every column is shown. A compact HTML table shows 10 columns.

	Returns
	-------
	str
		The HTML table, followed by a note for a Table without rows, or only the note for a Table without columns.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.preview.notebook_display import format_table_html
	>>> table_html = format_table_html(pandas.DataFrame({"price": [1.5]}), ndp.ShownColumns.ALL)
	>>> "FLOAT64" in table_html
	True
	"""
	note = write_empty_table_note(frame)
	column_count = len(frame.columns)
	if column_count == 0:
		note_html = NOTE_HTML.format(note=note)
		return note_html

	typed_frame = build_typed_frame(frame)
	column_limit = None
	are_columns_left_out = False
	if shown_columns == ShownColumns.COMPACT:
		column_limit = COMPACT_NOTEBOOK_COLUMN_COUNT
		are_columns_left_out = column_count > column_limit

	row_count = len(frame.index)
	row_limit = find_shown_row_count(row_count)
	are_rows_left_out = row_limit is not None
	# pandas writes the size of the Table under it, as in its text, only when rows or columns are left out.
	shows_size = are_rows_left_out or are_columns_left_out
	table_html = typed_frame.to_html(max_rows=row_limit, max_cols=column_limit, show_dimensions=shows_size)
	if note is not None:
		note_html = NOTE_HTML.format(note=note)
		table_html += note_html

	return table_html


def find_shown_row_count(row_count: int) -> int | None:
	"""
	Return how many rows pandas shows for a Table of this length.

	pandas shows every row up to ``display.max_rows``, and only ``display.min_rows`` of them, the first and last
	ones, beyond it. A missing ``display.min_rows`` or one above ``display.max_rows`` shows ``display.max_rows`` rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row_count
		The number of rows of the Table.

	Returns
	-------
	int or None
		The number of rows shown, or None to show every row.

	Examples
	--------
	>>> from numdaplot.tables.preview.notebook_display import find_shown_row_count
	>>> find_shown_row_count(5) is None
	True
	>>> find_shown_row_count(1000)
	10
	"""
	max_rows = pandas.get_option(MAX_ROWS_OPTION)
	if max_rows is None:
		return None

	if row_count <= max_rows:
		return None

	min_rows = pandas.get_option(MIN_ROWS_OPTION)
	if min_rows is None:
		return max_rows

	shown_row_count = min(min_rows, max_rows)

	return shown_row_count


def show_pandas_frame(frame: pandas.DataFrame) -> None:
	"""
	Show a pandas DataFrame as it is: as an HTML table in a Jupyter notebook, as text anywhere else.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The rows to show, with their header.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.preview.notebook_display import show_pandas_frame
	>>> show_pandas_frame(pandas.DataFrame({"price": [1.5]}))
	   price
	0    1.5
	"""
	runs_in_notebook = is_notebook()
	if not runs_in_notebook:
		frame_text = repr(frame)
		print(frame_text)
		return

	frame_html = frame.to_html()
	display_html(frame_html)


def display_html(frame_html: str) -> None:
	"""
	Show an HTML table in a Jupyter notebook.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame_html
		The HTML table.

	Examples
	--------
	>>> from numdaplot.tables.preview.notebook_display import display_html, is_notebook
	>>> if is_notebook():
	... 	display_html("<table></table>")
	"""
	display_module = import_module(IPYTHON_DISPLAY_MODULE)
	html_object = display_module.HTML(frame_html)
	display_module.display(html_object)


def is_notebook() -> bool:
	"""
	Return whether the code runs in a Jupyter notebook.

	IPython is optional: without it, the code never runs in a notebook.

	.. versionadded:: 0.1.0

	Returns
	-------
	bool
		True inside a Jupyter kernel, False in a terminal or a script.

	Examples
	--------
	>>> from numdaplot.tables.preview.notebook_display import is_notebook
	>>> is_notebook()
	False
	"""
	ipython_spec = find_spec(IPYTHON_PACKAGE)
	if ipython_spec is None:
		return False

	ipython_module = import_module(IPYTHON_PACKAGE)
	shell = ipython_module.get_ipython()
	if shell is None:
		return False

	runs_in_kernel = NOTEBOOK_KERNEL in shell.config

	return runs_in_kernel
