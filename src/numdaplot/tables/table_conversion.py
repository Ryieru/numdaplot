"""
Conversion of a Table to and from pandas, Arrays and Python values.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self, cast

import pandas

from numdaplot.arrays.array import Array
from numdaplot.arrays.conversion.python_values import to_python_list
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.errors.unsupported_operand_error import UnsupportedOperandError
from numdaplot.tables.frames.array_frame import build_array_frame
from numdaplot.tables.frames.column_values import convert_column_values, find_column_missing, read_array_values
from numdaplot.tables.frames.frame_equality import are_frames_equal
from numdaplot.tables.frames.table_text import format_table
from numdaplot.tables.frames.time_zones import find_column_time_zone
from numdaplot.tables.table_data import TableData

if TYPE_CHECKING:
	from numdaplot.arrays.equality import Equality

SINGLE_VALUE_COUNT = 1
FIRST_POSITION = 0


class TableConversion(TableData):
	"""
	Conversion of a Table to and from pandas, Arrays and Python values.

	.. versionadded:: 0.1.0
	"""

	@classmethod
	def from_pandas(cls, frame: pandas.DataFrame) -> Self:
		"""
		Return a Table holding a copy of a pandas DataFrame; changing the DataFrame never changes the Table.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			A pandas DataFrame whose index is the row numbers 0, 1, 2... Python objects become integers, decimals
			or booleans when they all are, and texts otherwise.

		Returns
		-------
		Self
			A new Table.

		Raises
		------
		UnsupportedIndexError
			When the index holds other values: call ``reset_index()`` first to keep them as a column.
		InvalidColumnNameError, DuplicateColumnError
			When a column name is not a non-empty text, or appears twice.
		UnsupportedTypeError
			When a column has a type numdaplot does not support, such as complex numbers
			or datetimes with a time zone.

		Examples
		--------
		>>> import pandas
		>>> import numdaplot as ndp
		>>> ndp.Table.from_pandas(pandas.DataFrame({"city": ["Pau", None], "count": [2, 3]}))
		   city count
		   TEXT INT64
		0   Pau     2
		1  <NA>     3
		"""
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_arrays(cls, columns: dict[str, Array]) -> Self:
		"""
		Return a Table whose columns hold the values of one-dimensional Arrays.

		.. versionadded:: 0.1.0

		Parameters
		----------
		columns
			One Array per column, by column name, all of the same length.

		Returns
		-------
		Self
			A new Table, columns in the order of the dictionary.

		Raises
		------
		EmptyListError
			When there is no column.
		InvalidColumnNameError
			When a column name is not a non-empty text.
		DimensionError
			When an Array does not have one dimension.
		ShapeMismatchError
			When the Arrays do not have the same length.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
		>>> prices = ndp.Array.from_list([1.5, 8.0])
		>>> ndp.Table.from_arrays({"city": cities, "price": prices})
		    city   price
		    TEXT FLOAT64
		0  Paris     1.5
		1   Lyon     8.0
		"""
		frame = build_array_frame(columns)
		table = cls(frame)

		return table

	def to_pandas(self) -> pandas.DataFrame:
		"""
		Return a pandas copy of the Table; changing it never changes the Table.

		Integers, booleans and texts use the pandas dtypes that accept missing values (``pd.NA``).

		.. versionadded:: 0.1.0

		Returns
		-------
		pandas.DataFrame
			A copy, rows numbered from 0.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Table.from_arrays({"count": ndp.Array.from_list([2, 3])}).to_pandas().dtypes.tolist()
		[Int64Dtype()]
		"""
		frame_copy = self._frame.copy(deep=True)

		return frame_copy

	def column(self, column_name: str) -> Array:
		"""
		Return the values of a column as an Array.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name of the column.

		Returns
		-------
		Array
			A one-dimensional Array of the type of the column; a ``CATEGORY`` column gives a ``TEXT`` Array.

		Raises
		------
		ColumnNotFoundError
			When no column has this name.
		UnsupportedMissingError
			When an integer, boolean, text or category column has missing values, which an Array cannot hold:
			convert it to ``FLOAT64`` first, or drop its missing values.
		TimeZoneMismatchError
			When the column holds datetimes with a time zone, which an Array cannot hold: remove the zone first
			with ``TimeZoneMode.REMOVE``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
		>>> table.column("price").compute(ndp.Sum()).to_value()
		9.5
		"""
		column = self._read_column(column_name)
		array_values = read_array_values(column)
		column_array = Array.from_numpy(array_values)

		return column_array

	def to_value(self) -> Any:
		"""
		Return the single value of a Table of one row and one column, as a Python value.

		.. versionadded:: 0.1.0

		Returns
		-------
		Any
			The value, ``None`` when it is missing. A datetime with a time zone keeps its zone.

		Raises
		------
		NotSingleValueError
			When the Table does not hold exactly one value.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
		>>> highest_price = ndp.Calculation(column="price", function=ndp.Max())
		>>> table.aggregate(ndp.Aggregation(calculations=[highest_price])).to_value()
		8.0
		"""
		column_count = len(self._frame.columns)
		value_count = self.row_count * column_count
		if value_count != SINGLE_VALUE_COUNT:
			raise NotSingleValueError(value_count)

		column = self._frame.iloc[:, FIRST_POSITION]
		missing = find_column_missing(column)
		is_missing = bool(missing[FIRST_POSITION])
		if is_missing:
			return None

		time_zone = find_column_time_zone(column)
		if time_zone is not None:
			moment = column.iloc[FIRST_POSITION]
			zone_datetime = moment.to_pydatetime()
			return zone_datetime

		values = convert_column_values(column)
		python_values = to_python_list(values)
		single_value = python_values[FIRST_POSITION]

		return single_value

	def is_equal(self, equality: Equality) -> bool:
		"""
		Return whether this Table and another one have the same columns, in the same order, with the same values.

		Two missing values at the same row are equal. Datetime columns in different time zones are different,
		even for the same instants.

		.. versionadded:: 0.1.0

		Parameters
		----------
		equality
			The other Table, and whether the type of each column must also be the same.

		Returns
		-------
		bool
			True when both Tables are equal.

		Raises
		------
		UnsupportedOperandError
			When the compared value is not a Table.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> integers = ndp.Table.from_arrays({"count": ndp.Array.from_list([1, 2])})
		>>> decimals = ndp.Table.from_arrays({"count": ndp.Array.from_list([1.0, 2.0])})
		>>> integers.is_equal(ndp.Equality(other=decimals))
		True
		"""
		other = cast(object, equality.other)
		if not isinstance(other, TableData):
			other_class = type(other)
			raise UnsupportedOperandError(other_class.__name__)

		other_frame = other._frame
		is_equal = are_frames_equal(self._frame, other_frame, equality.types)

		return is_equal

	def __repr__(self) -> str:
		"""
		Return the text of the Table, with the type of each column under its name.

		A long Table only shows its first and last rows, as in pandas.

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
