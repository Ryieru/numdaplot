"""
Missing values of a Table: count, summary and removal.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.positions.axis import Axis
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_counts import count_frame_missing
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.missing.missing_removal import drop_frame_missing
from numdaplot.tables.missing.missing_summary import summarize_missing
from numdaplot.tables.preview.notebook_display import show_pandas_frame
from numdaplot.tables.table_data import TableData


class TableMissing(TableData):
	"""
	Missing values of a Table with ``count_missing``, ``preview_missing`` and ``drop_missing``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def count_missing(self, missing_count: MissingCount | None = None, axis: Axis | None = None) -> Self:
		"""
		Return the number or the ratio of missing values, for the whole Table, each row or each column.

		.. versionadded:: 0.1.0

		Parameters
		----------
		missing_count
			The measure, the number of missing values when omitted.
		axis
			One count per row with ``Axis.EACH_ROW``, one per column with ``Axis.EACH_COLUMN``, a single count for
			the whole Table when omitted.

		Returns
		-------
		Self
			A new Table with a ``missing_count`` column, or ``missing_ratio`` for ``Measure.RATIO``:
			one row for the whole Table, read with ``to_value``, one row per row, or one row per column after
			a ``column`` column naming it. A ratio is missing when there is no value to count.


		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau", "Nice"])
		>>> prices = ndp.Array.from_list([120.0, None, None, 90.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> table.count_missing().to_value()
		2
		>>> table.count_missing(ndp.MissingCount(measure=ndp.Measure.RATIO), axis=ndp.Axis.EACH_COLUMN)
		  column missing_ratio
		    TEXT       FLOAT64
		0   city           0.0
		1  price           0.5
		"""
		if missing_count is None:
			missing_count = MissingCount()

		count_frame = count_frame_missing(self._frame, missing_count, axis)
		count_table = self._wrap(count_frame)

		return count_table

	def preview_missing(self) -> None:
		"""
		Show the number and the percentage of missing values of each column, then of the whole Table.

		In a Jupyter notebook the summary is shown as an HTML table, elsewhere as text. Nothing is returned:
		use ``count_missing`` to compute with these numbers.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
		>>> prices = ndp.Array.from_list([120.0, None, 150.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> table.preview_missing()
		          column     type  missing_count missing_ratio
		0           city     TEXT              0         0.0 %
		1          price  FLOAT64              1        33.3 %
		2  (all columns)                       1        16.7 %
		"""
		summary = summarize_missing(self._frame)
		show_pandas_frame(summary)

	@checked_arguments
	def drop_missing(self, missing_drop: MissingDrop | None = None, axis: Axis = Axis.EACH_ROW) -> Self:
		"""
		Return the Table without its rows, or its columns, holding missing values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		missing_drop
			The columns looked at and how many missing values are needed: a single one in any column when
			omitted.
		axis
			``Axis.EACH_ROW`` by default to remove rows, ``Axis.EACH_COLUMN`` to remove columns.

		Returns
		-------
		Self
			A new Table, remaining rows in their order and numbered from 0, or remaining columns in their order.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a looked at column does not exist.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
		>>> prices = ndp.Array.from_list([120.0, None, 150.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> table.drop_missing()
		    city   price
		    TEXT FLOAT64
		0  Paris   120.0
		1    Pau   150.0
		"""
		if missing_drop is None:
			missing_drop = MissingDrop()

		remaining_frame = drop_frame_missing(self._frame, missing_drop, axis)
		remaining_table = self._wrap(remaining_frame)

		return remaining_table
