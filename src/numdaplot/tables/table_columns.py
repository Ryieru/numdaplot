"""
Column operations of a Table: choice, renaming, conversion and addition.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.tables.columns.added_column import add_frame_column
from numdaplot.tables.columns.chosen_columns import choose_frame_columns
from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.conversion import Conversion
from numdaplot.tables.columns.converted_column import convert_column
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renamed_columns import rename_frame_columns
from numdaplot.tables.columns.renaming import Renaming
from numdaplot.tables.table_data import TableData


class TableColumns(TableData):
	"""
	Column operations of a Table: ``choose_columns``, ``rename``, ``convert`` and ``add_column``.

	.. versionadded:: 0.1.0
	"""

	def choose_columns(self, choice: ColumnChoice) -> Self:
		"""
		Return the Table with only some columns, or without some columns.

		.. versionadded:: 0.1.0

		Parameters
		----------
		choice
			The columns, and whether to keep them, in the order of the list, or to drop them.

		Returns
		-------
		Self
			A new Table.

		Raises
		------
		ColumnNotFoundError
			When a named column does not exist.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris"])
		>>> prices = ndp.Array.from_list([1.5])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> table.choose_columns(ndp.ColumnChoice(columns=["city"], mode=ndp.ColumnMode.DROP)).column_names
		['price']
		"""
		chosen_frame = choose_frame_columns(self._frame, choice)
		chosen_table = self._wrap(chosen_frame)

		return chosen_table

	def rename(self, renaming: Renaming) -> Self:
		"""
		Return the Table with renamed columns, every renaming applied at once.

		Two columns can swap their names in a single call.

		.. versionadded:: 0.1.0

		Parameters
		----------
		renaming
			The ``NameChange`` of each renamed column.

		Returns
		-------
		Self
			A new Table, columns in the same order.

		Raises
		------
		ColumnNotFoundError
			When a renamed column does not exist.
		DuplicateColumnError
			When a new name is the name of a column kept as it is.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"prix": ndp.Array.from_list([1.5])})
		>>> table.rename(ndp.Renaming(changes=[ndp.NameChange(old_name="prix", new_name="price")])).column_names
		['price']
		"""
		renamed_frame = rename_frame_columns(self._frame, renaming)
		renamed_table = self._wrap(renamed_frame)

		return renamed_table

	def convert(self, conversion: Conversion) -> Self:
		"""
		Return the Table with a column converted to another type, missing values staying missing.

		.. versionadded:: 0.1.0

		Parameters
		----------
		conversion
			The column, its new type, and the date format or the time zone change. Accepted: between number
			types, from numbers, booleans, categories, dates, datetimes and durations to texts, from texts and
			categories to numbers, booleans (``"true"`` or ``"false"`` in any case), dates or datetimes, from any
			other type to categories, between dates and datetimes, and a time zone change of datetimes.

		Returns
		-------
		Self
			A new Table, the column at its place.

		Raises
		------
		ColumnNotFoundError
			When the column does not exist.
		IncompatibleTypesError
			When the conversion is not accepted.
		InvalidConversionError
			When the format or the time zone change does not apply to the conversion.
		ValueConversionError
			At the first value that cannot be stored in the new type, such as ``"abc"`` read as a number,
			2.5 stored as an integer, or ``"31/02/2026"`` read as a date.
		TimeZoneMismatchError
			When the time zone change does not apply to whether the datetimes have a zone.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"zip_code": ndp.Array.from_list(["06000", "75001"])})
		>>> table.convert(ndp.Conversion(column="zip_code", dtype=ndp.Type.INT32))
		  zip_code
		     INT32
		0     6000
		1    75001
		"""
		column = self._read_column(conversion.column)
		converted_column = convert_column(column, conversion)
		converted_frame = self._frame.copy(deep=False)
		converted_frame[conversion.column] = converted_column
		converted_table = self._wrap(converted_frame)

		return converted_table

	def add_column(self, new_column: NewColumn) -> Self:
		"""
		Return the Table with one more column, or with a column replaced.

		.. versionadded:: 0.1.0

		Parameters
		----------
		new_column
			The name, a one-dimensional Array with one value per row, and what to do when the name exists.

		Returns
		-------
		Self
			A new Table. A new column is placed last; a replaced column keeps its place.

		Raises
		------
		DimensionError
			When the Array does not have one dimension.
		ShapeMismatchError
			When the Array does not have one value per row.
		DuplicateColumnError
			When the name exists and ``on_conflict`` is ``Conflict.ERROR``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([10.0, 20.0])})
		>>> taxed_prices = table.column("price") * 1.2
		>>> table.add_column(ndp.NewColumn(name="taxed_price", values=taxed_prices))
		    price taxed_price
		  FLOAT64     FLOAT64
		0    10.0        12.0
		1    20.0        24.0
		"""
		extended_frame = add_frame_column(self._frame, new_column)
		extended_table = self._wrap(extended_frame)

		return extended_table
