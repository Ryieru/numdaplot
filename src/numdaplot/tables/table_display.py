"""
Display of a few rows of a Table.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.preview.notebook_display import show_frame
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.preview_rows import choose_preview_rows
from numdaplot.tables.table_data import TableData


class TableDisplay(TableData):
	"""
	Display of a few rows of a Table with ``preview``.

	.. versionadded:: 0.1.0
	"""

	def preview(self, preview: Preview | None = None) -> None:
		"""
		Show a few rows, with their row numbers and the type of each column under its name.

		In a Jupyter notebook the rows are shown as an HTML table, elsewhere as text. Nothing is returned.

		.. versionadded:: 0.1.0

		Parameters
		----------
		preview
			How many rows, and which ones: the first 5 when omitted.

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
		show_frame(preview_frame)
