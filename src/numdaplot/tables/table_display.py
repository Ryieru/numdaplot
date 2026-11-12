"""
Display of a Table: its text, its notebook table and a few of its rows.

.. versionadded:: 0.1.0
"""

from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.frames.table_text import format_table
from numdaplot.tables.preview.notebook_display import format_table_html, show_frame
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.preview_rows import choose_preview_rows
from numdaplot.tables.preview.shown_columns import ShownColumns
from numdaplot.tables.table_data import TableData


class TableDisplay(TableData):
	"""
	Display of a Table: its text, the table shown by a notebook, and a few of its rows with ``preview``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def preview(self, preview: Preview | None = None) -> None:
		"""
		Show a few rows, with their row numbers and the type of each column under its name.

		In a Jupyter notebook the rows are shown as an HTML table, elsewhere as text. Every column is shown unless
		the settings ask for a compact display. Nothing is returned.

		.. versionadded:: 0.1.0

		Parameters
		----------
		preview
			How many rows, which ones, and how the columns are shown: the first 5, with every column, when omitted.


		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([10.0, 20.0, 30.0])})
		>>> table.preview(ndp.Preview(count=2, side=ndp.Side.END))
		    price
		  FLOAT64
		1    20.0
		2    30.0
		"""
		if preview is None:
			preview = Preview()

		preview_frame = choose_preview_rows(self._frame, preview)
		show_frame(preview_frame, preview.columns)

	def __repr__(self) -> str:
		"""
		Return the text of the Table, with the type of each column under its name.

		A long Table only shows its first and last rows, as in pandas. Every column is shown, going on after a line
		break, ended by a backslash, when they do not fit in the width of the terminal.

		.. versionadded:: 0.1.0

		Returns
		-------
		str
			The text shown by ``print(table)``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> print(ndp.Table.from_arrays({"paid": ndp.Array.from_list([True, False])}))
		    paid
		    BOOL
		0   True
		1  False
		"""
		table_text = format_table(self._frame)

		return table_text

	def _repr_html_(self) -> str:
		"""
		Return the HTML table a Jupyter notebook shows for a Table written at the end of a cell.

		The table is the one of ``preview``: every column, with the type of each column under its name. A long Table
		only shows its first and last rows, as its text does.

		.. versionadded:: 0.1.0

		Returns
		-------
		str
			The HTML table, or a note for a Table without rows or without columns.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"paid": ndp.Array.from_list([True, False])})
		>>> "BOOL" in table._repr_html_()
		True
		"""
		table_html = format_table_html(self._frame, ShownColumns.ALL)

		return table_html
