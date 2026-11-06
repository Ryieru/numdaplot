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

	note = write_empty_table_note(frame)
	column_count = len(frame.columns)
	if column_count == 0:
		note_html = NOTE_HTML.format(note=note)
		display_html(note_html)
		return

	typed_frame = build_typed_frame(frame)
	column_limit = None
	if shown_columns == ShownColumns.COMPACT:
		column_limit = COMPACT_NOTEBOOK_COLUMN_COUNT

	frame_html = typed_frame.to_html(max_cols=column_limit)
	if note is not None:
		frame_html += NOTE_HTML.format(note=note)

	display_html(frame_html)


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
