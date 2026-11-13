"""
Selection of the rows and columns of a Table, by conditions and by position, and check of its values.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.positions.region import Region
from numdaplot.rules.rule import Rule
from numdaplot.tables.filtering.checked_frame import check_frame
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.filtering.row_mask import build_filter_mask
from numdaplot.tables.frames.region_positions import take_region
from numdaplot.tables.table_data import TableData


class TableSelection(TableData):
	"""
	Selection of rows with ``filter``, of a region with ``take``, and check of every value with ``check``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def filter(self, row_filter: Filter) -> Self:
		"""
		Return the rows satisfying a filter.

		.. versionadded:: 0.1.0

		Parameters
		----------
		row_filter
			The conditions and how they combine. A missing value only satisfies ``IsMissing``.

		Returns
		-------
		Self
			A new Table with the kept rows, in their order, numbered from 0.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a condition names a column the Table does not have.
		IncompatibleTypesError
			When a rule does not apply to the type of one of its columns.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
		>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
		>>> table.filter(ndp.Filter(conditions=[expensive]))
		    city   price
		    TEXT FLOAT64
		0  Paris   120.0
		1    Pau   150.0
		"""
		mask = build_filter_mask(self._frame, row_filter)
		kept_frame = self._frame[mask]
		numbered_frame = kept_frame.reset_index(drop=True)
		filtered_table = self._wrap(numbered_frame)

		return filtered_table

	@checked_arguments
	def take(self, region: Region) -> Self:
		"""
		Return the rows and the columns of a region.

		A row chosen with ``Index`` gives a Table of one row. Use ``to_value`` to read a single value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		region
			The rows and the columns, every one of a dimension when omitted. Columns are positions or names;
			negative positions count from the end.

		Returns
		-------
		Self
			A new Table, rows numbered from 0, columns in the order of the region.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		InvalidPositionError
			When a position is not a whole number inside its dimension.
		ColumnNotFoundError
			When a column name matches no column.
		DuplicateColumnError
			When a column name appears twice in the region.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
		>>> table = ndp.Table.from_arrays({"price": prices})
		>>> table.take(ndp.Region(rows=ndp.Range(start=1, stop=2), columns=["price"]))
		    price
		  FLOAT64
		0    80.0
		1   150.0
		"""
		region_frame = take_region(self._frame, region)
		region_table = self._wrap(region_frame)

		return region_table

	@checked_arguments
	def check(self, rule: Rule) -> Self:
		"""
		Return which values satisfy a rule, in every column.

		To check some columns only, choose them first with ``choose_columns``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		rule
			A ``Rule``, such as ``ndp.Greater(10)`` or ``ndp.IsIn(["Paris"])``: see ``Rule`` for every rule.
			A missing value only satisfies ``IsMissing``.

		Returns
		-------
		Self
			A new Table with the same columns and rows, holding True where the value satisfies the rule.
			Every column is of type ``BOOL``.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the rule does not apply to the type of one of the columns.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([120.0, None, 150.0])
		>>> stocks = ndp.Array.from_list([3.0, 5.0, None])
		>>> table = ndp.Table.from_arrays({"price": prices, "stock": stocks})
		>>> table.check(ndp.IsMissing())
		   price  stock
		    BOOL   BOOL
		0  False  False
		1   True  False
		2  False   True
		"""
		checked_frame = check_frame(self._frame, rule)
		checked_table = self._wrap(checked_frame)

		return checked_table
