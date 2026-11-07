"""
Columns stored by a Table, shared by every group of Table methods.

.. versionadded:: 0.1.0
"""

from typing import Never, Self

import pandas

from numdaplot.data_types.type import Type
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.frames.cleaned_names import clean_frame_names
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.frame_normalization import normalize_frame
from numdaplot.tables.frames.time_zones import find_column_time_zone

CONSTRUCTOR_OPERATION = "Creating a Table with ndp.Table(...)"
CONSTRUCTOR_ALTERNATIVE = "ndp.Table.from_arrays, from_pandas or a file method such as from_csv"


class TableData:
	"""
	Columns stored by a Table, shared by every group of Table methods.

	Use ``ndp.Table`` and its ``from_*`` methods; this base class only holds the columns.

	.. versionadded:: 0.1.0
	"""

	_frame: pandas.DataFrame

	def __init__(self, *arguments: Never, **keyword_arguments: Never) -> None:
		"""
		Refuse the creation of a Table by its constructor: the ``from_*`` methods create Tables.

		.. versionadded:: 0.1.0

		Parameters
		----------
		arguments
			Any value, refused.
		keyword_arguments
			Any named value, refused.

		Raises
		------
		RefusedOperationError
			Always, naming the ``from_*`` methods.
		"""
		raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)

	@classmethod
	def _create(cls, frame: pandas.DataFrame) -> Self:
		"""
		Return a new Table storing normalized columns without copy.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns, already stored with the dtypes given by ``to_pandas_dtype`` and numbered from 0,
			never changed afterwards.

		Returns
		-------
		Self
			The new Table.
		"""
		created_table = cls.__new__(cls)
		created_table._frame = frame

		return created_table

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
	def column_count(self) -> int:
		"""
		Number of columns.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])}).column_count
		1
		"""
		column_count = len(self._frame.columns)

		return column_count

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

	@property
	def column_time_zones(self) -> dict[str, TimeZone | None]:
		"""
		Time zone of each datetime column, by column name, ``None`` for a datetime column without zone.

		Columns of other types are not listed.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> from datetime import datetime
		>>> import numdaplot as ndp
		>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
		>>> times.column_time_zones
		{'time': None}
		"""
		column_time_zones = dict[str, TimeZone | None]()

		for column_name in self.column_names:
			column = self._frame[column_name]
			column_type = find_column_type(column)
			if column_type == Type.DATETIME:
				column_time_zones[column_name] = find_column_time_zone(column)

		return column_time_zones

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
		table = cls._create(normalized_frame)

		return table

	@classmethod
	def _from_read_frame(cls, frame: pandas.DataFrame, column_names: ColumnNames) -> Self:
		"""
		Return a new Table holding a DataFrame read from a file or given by the user, its names cleaned when asked.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			A pandas DataFrame read from outside numdaplot, which is not changed.
		column_names
			Whether the spaces, tabs and line breaks at the start and the end of each name are removed.

		Returns
		-------
		Self
			The new Table.

		Raises
		------
		DuplicateColumnError
			When two names become the same once cleaned, or a name appears twice.
		InvalidColumnNameError, UnsupportedIndexError, UnsupportedTypeError
			When the pandas DataFrame cannot become a Table, as in ``normalize_frame``.
		"""
		cleaned_frame = clean_frame_names(frame, column_names)
		table = cls._from_frame(cleaned_frame)

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
		wrapped_table = table_class._create(frame)

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
