"""
Column operations of a Table: choice, renaming, conversion, application of a function and addition.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.conversions.converted_column import convert_column
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.columns.added_column import add_frame_column
from numdaplot.tables.columns.applied_columns import apply_frame_columns
from numdaplot.tables.columns.chosen_columns import choose_frame_columns
from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renamed_columns import rename_frame_columns
from numdaplot.tables.columns.renaming import Renaming
from numdaplot.tables.columns.table_application import TableApplication
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
from numdaplot.tables.table_data import TableData


class TableColumns(TableData):
	"""
	Column operations of a Table: ``choose_columns``, ``rename``, ``convert``, ``apply`` and ``add_column``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
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
		InvalidTypeError
			When an argument is not of the type its annotation names.
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

	@checked_arguments
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
		InvalidTypeError
			When an argument is not of the type its annotation names.
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

	@checked_arguments
	def convert(self, conversion: TableConversion) -> Self:
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
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When the column does not exist.
		IncompatibleTypesError
			When the conversion is not accepted.
		InvalidConversionError
			When the format, the time zone change or the boolean rule does not apply to the conversion.
		InvalidLimitsError
			When ``Brackets`` cut integers and a bracket between two limits holds no integer.
		UnmatchedValueError
			When a number is in no bracket of ``Brackets`` whose ``others`` is ``Unmatched.ERROR``.
		ValueConversionError
			At the first value that cannot be stored in the new type, such as ``"abc"`` read as a number,
			2.5 stored as an integer, 3 read as a boolean with ``ZERO_ONE``, ``"31/02/2026"`` read as a date, or
			``"25:00"`` read as a time of day.
		TimeOverflowError
			When a value converted to ``DATETIME`` is outside 1677 to 2262.
		TimeZoneMismatchError
			When the time zone change does not apply to whether the datetimes have a zone.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"zip_code": ndp.Array.from_list(["06000", "75001"])})
		>>> table.convert(ndp.TableConversion(column="zip_code", dtype=ndp.Type.INT32))
		  zip_code
		     INT32
		0     6000
		1    75001
		"""
		column = self._read_column(conversion.column)
		with NamedColumnErrors(column):
			converted_column = convert_column(column, conversion)

		converted_frame = self._frame.copy(deep=False)
		converted_frame[conversion.column] = converted_column
		converted_table = self._wrap(converted_frame)

		return converted_table

	@checked_arguments
	def apply(self, application: TableApplication) -> Self:
		"""
		Return the Table with a math function, a time function or a value mapping applied to each value of columns.

		Unlike ``Array.apply``, an integer or boolean column keeps its type when a ``ValueMapping`` gives it missing
		values, since a Table column can hold them.

		.. versionadded:: 0.2.0

		Parameters
		----------
		application
			The function, as ``Array.apply`` takes, and the names of the columns it applies to.

		Returns
		-------
		Self
			A new Table, each column replaced at its place, under its name. Missing values stay missing.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a column does not exist, before any column is changed.
		IncompatibleTypesError
			When the function does not apply to the type of a column, or a ``ValueMapping`` with ``Unmatched.KEEP``
			gives new values of another family than the kept values, such as texts among numbers.
		OutOfDomainError
			When a value is outside the domain of a math function, such as the square root of -1.
		TimeZoneMismatchError
			When a column holds datetimes with a time zone: remove it first with ``convert`` and a
			``TimeZoneChange``.
		UnmatchedValueError
			When a value has no ``ValueChange`` in a ``ValueMapping`` whose ``others`` is ``Unmatched.ERROR``.
		ValueConversionError
			When a ``ValueMapping`` gives a number that does not fit the number type of a column.

		The first column that fails stops the operation, and the error names it.

		Warns
		-----
		CalculationWarning
			When a result of a math function becomes an infinite value or NaN.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> first_answers = ndp.Array.from_list([1, 7, 2])
		>>> second_answers = ndp.Array.from_list([9, 3, 1])
		>>> survey = ndp.Table.from_arrays({"q1": first_answers, "q2": second_answers})
		>>> unknown_answers = [ndp.ValueChange(7, None), ndp.ValueChange(9, None)]
		>>> mapping = ndp.ValueMapping(changes=unknown_answers, others=ndp.Unmatched.KEEP)
		>>> survey.apply(ndp.TableApplication(function=mapping, columns=["q1", "q2"]))
		     q1    q2
		  INT64 INT64
		0     1  <NA>
		1  <NA>     3
		2     2     1
		"""
		applied_frame = apply_frame_columns(self._frame, application)
		applied_table = self._wrap(applied_frame)

		return applied_table

	@checked_arguments
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
		InvalidTypeError
			When an argument is not of the type its annotation names.
		DimensionError
			When the Array does not have one dimension.
		ShapeMismatchError
			When the Array does not have one value per row.
		DuplicateColumnError
			When the name exists and ``on_conflict`` is ``Conflict.ERROR``.
		TimeOverflowError
			When a column holds a datetime outside 1677 to 2262, or a duration beyond about 292 years.

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
