"""
Columns stored by a Table, shared by every group of Table methods.

.. versionadded:: 0.1.0
"""

from typing import Self

import pandas

from numdaplot.data_types.type import Type
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.frame_normalization import normalize_frame


class TableData:
	"""
	Columns stored by a Table, shared by every group of Table methods.

	Use ``ndp.Table`` and its ``from_*`` methods; this base class only holds the columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns, already stored with the dtypes given by ``to_pandas_dtype`` and numbered from 0.
	"""

	def __init__(self, frame: pandas.DataFrame) -> None:
		"""
		Store normalized columns without copy.

		The ``from_*`` methods create Tables; this constructor is reserved to numdaplot.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns, never changed afterwards.
		"""
		self._frame = frame

	@property
	def row_count(self) -> int:
		"""
		Number of rows.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])}).row_count
		2
		"""
		row_count = len(self._frame)

		return row_count

	@property
	def column_names(self) -> list[str]:
		"""
		Names of the columns, in order. Changing the returned list never changes the Table.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris"])
		>>> prices = ndp.Array.from_list([1.5])
		>>> ndp.Table.from_arrays({"city": cities, "price": prices}).column_names
		['city', 'price']
		"""
		column_names = [str(column_name) for column_name in self._frame.columns]

		return column_names

	@property
	def column_types(self) -> dict[str, Type]:
		"""
		Type of each column, by column name, in the order of the columns.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])}).column_types
		{'price': <Type.FLOAT64: 10>}
		"""
		column_types = dict[str, Type]()

		for column_name in self.column_names:
			column = self._frame[column_name]
			column_type = find_column_type(column)
			column_types[column_name] = column_type

		return column_types

	@classmethod
	def _from_frame(cls, frame: pandas.DataFrame) -> Self:
		"""
		Return a new Table holding the normalized copy of any pandas DataFrame.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			Any pandas DataFrame, which is not changed.

		Returns
		-------
		Self
			The new Table.

		Raises
		------
		InvalidColumnNameError, DuplicateColumnError, UnsupportedIndexError, UnsupportedTypeError
			When the pandas DataFrame cannot become a Table, as in ``normalize_frame``.
		"""
		normalized_frame = normalize_frame(frame)
		table = cls(normalized_frame)

		return table

	def _wrap(self, frame: pandas.DataFrame) -> Self:
		"""
		Return a new Table of the same class holding other normalized columns.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns of the new Table, stored without copy.

		Returns
		-------
		Self
			The new Table.
		"""
		table_class = type(self)
		wrapped_table = table_class(frame)

		return wrapped_table

	def _read_column(self, column_name: str) -> Column:
		"""
		Return a column of the Table.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name of the column.

		Returns
		-------
		Column
			The stored column, which must not be changed.

		Raises
		------
		ColumnNotFoundError
			When no column has this name.
		"""
		requested_names = [column_name]
		require_known_columns(requested_names, self.column_names)
		column = self._frame[column_name]

		return column
