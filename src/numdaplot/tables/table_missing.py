"""
Missing values of a Table: count, summary and removal.

.. versionadded:: 0.1.0
"""

from typing import Self

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

	def count_missing(self, missing_count: MissingCount) -> Self:
		"""
		Return the number or the ratio of missing values, for the whole Table, each row or each column.

		.. versionadded:: 0.1.0

		Parameters
		----------
		missing_count
			The axis and the measure: a single number for the whole Table with ``ndp.MissingCount()``.

		Returns
		-------
		Self
			A new Table with a ``missing_count`` column, or ``missing_ratio`` for ``Measure.RATIO``:
			one row for the whole Table, read with ``to_value``, one row per row, or one row per column after
			a ``column`` column naming it. A ratio is missing when there is no value to count.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau", "Nice"])
		>>> prices = ndp.Array.from_list([120.0, None, None, 90.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> table.count_missing(ndp.MissingCount()).to_value()
		2
		>>> table.count_missing(ndp.MissingCount(axis=ndp.Axis.EACH_COLUMN, measure=ndp.Measure.RATIO))
		  column missing_ratio
		    TEXT       FLOAT64
		0   city           0.0
		1  price           0.5
		"""
		count_frame = count_frame_missing(self._frame, missing_count)
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
		0   city     TEXT              0         0.0 %
		1  price  FLOAT64              1        33.3 %
		2  total                       1        16.7 %
		"""
		summary = summarize_missing(self._frame)
		show_pandas_frame(summary)

	def drop_missing(self, missing_drop: MissingDrop) -> Self:
		"""
		Return the Table without its rows, or its columns, holding missing values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		missing_drop
			What is removed: every row holding a missing value with ``ndp.MissingDrop()``, or columns, and
			how many missing values are needed.

		Returns
		-------
		Self
			A new Table, remaining rows in their order and numbered from 0, or remaining columns in their order.

		Raises
		------
		ColumnNotFoundError
			When a looked at column does not exist.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
		>>> prices = ndp.Array.from_list([120.0, None, 150.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> table.drop_missing(ndp.MissingDrop())
		    city   price
		    TEXT FLOAT64
		0  Paris   120.0
		1    Pau   150.0
		"""
		remaining_frame = drop_frame_missing(self._frame, missing_drop)
		remaining_table = self._wrap(remaining_frame)

		return remaining_table
