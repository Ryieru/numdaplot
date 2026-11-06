"""
Statistics of a Table: aggregation, pivot table and description.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.aggregation.aggregated_frame import aggregate_frame
from numdaplot.tables.aggregation.aggregation import Aggregation
from numdaplot.tables.description.described_frame import describe_frame
from numdaplot.tables.description.description import Description
from numdaplot.tables.pivot.pivot_table import PivotTable
from numdaplot.tables.pivot.pivoted_frame import pivot_frame
from numdaplot.tables.table_data import TableData


class TableCalculation(TableData):
	"""
	Statistics of a Table with ``aggregate``, ``pivot_table`` and ``describe``. Missing values are ignored.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def aggregate(self, aggregation: Aggregation) -> Self:
		"""
		Return statistics of the whole Table, or of each group of rows.

		.. versionadded:: 0.1.0

		Parameters
		----------
		aggregation
			The calculations, and the columns forming the groups.

		Returns
		-------
		Self
			A new Table: the group columns, then one column per calculation; one row per group, sorted by
			group values with missing values as a group of their own, last. Without groups, a single row.
			A statistic needing a value gives a missing value for a group without present value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a calculation or a group names a column the Table does not have.
		IncompatibleTypesError
			When a statistic does not apply to the type of its column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Pau", "Lyon", "Pau"])
		>>> prices = ndp.Array.from_list([10.0, 30.0, 20.0])
		>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> average_price = ndp.Calculation(column="price", function=ndp.Mean())
		>>> table.aggregate(ndp.Aggregation(calculations=[average_price], group_by=["city"]))
		   city price_mean
		   TEXT    FLOAT64
		0  Lyon       30.0
		1   Pau       15.0
		"""
		aggregated_frame = aggregate_frame(self._frame, aggregation)
		aggregated_table = self._wrap(aggregated_frame)

		return aggregated_table

	@checked_arguments
	def pivot_table(self, pivot: PivotTable) -> Self:
		"""
		Return one statistic for each combination of groups of rows and values of a column, as a wide Table.

		``aggregate`` gives one row per combination: ``pivot_table`` gives one column per value of a column, as
		``Plot.heatmap`` draws them.

		.. versionadded:: 0.1.0

		Parameters
		----------
		pivot
			The columns forming the rows and the columns of the result, and the statistic of each cell.

		Returns
		-------
		Self
			A new Table: the columns of ``rows``, then one column per value of ``columns``, named after the value;
			one row per group, sorted, with missing values as a group of their own, last.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a setting names a column the Table does not have.
		RefusedOperationError
			When the column of ``columns`` holds missing values: remove them with ``drop_missing``.
		DuplicateColumnError
			When a value written as a text is also the name of a column of ``rows``.
		InvalidColumnNameError
			When a value written as a text is empty.
		IncompatibleTypesError
			When the statistic does not apply to the type of its column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> hours = ndp.Array.from_list([8, 8, 9])
		>>> weekdays = ndp.Array.from_list(["Mon", "Tue", "Mon"])
		>>> fares = ndp.Array.from_list([7.0, 9.0, 5.0])
		>>> trips = ndp.Table.from_arrays({"hour": hours, "weekday": weekdays, "fare": fares})
		>>> trip_count = ndp.Calculation(column="fare", function=ndp.Count(missing=ndp.CountedMissing.INCLUDED))
		>>> trips.pivot_table(ndp.PivotTable(rows=["hour"], columns="weekday", calculation=trip_count))
		   hour   Mon   Tue
		  INT64 INT64 INT64
		0     8     1     1
		1     9     1     0
		"""
		pivoted_frame = pivot_frame(self._frame, pivot)
		pivoted_table = self._wrap(pivoted_frame)

		return pivoted_table

	@checked_arguments
	def describe(self, description: Description | None = None) -> Self:
		"""
		Return statistics describing columns, one row per statistic and one column per described column.

		.. versionadded:: 0.1.0

		Parameters
		----------
		description
			The statistics and the columns. When omitted, every number column is described with the
			statistics of pandas.

		Returns
		-------
		Self
			A new Table whose first column, ``statistic``, names each statistic, such as ``quantile_25``.
			A cell is missing when the statistic does not apply to the column or finds no value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a described column does not exist.
		DuplicateColumnError
			When a described column is named ``statistic``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([10.0, 30.0])})
		>>> table.describe(ndp.Description(functions=[ndp.Count(), ndp.Mean(), ndp.Max()]))
		        statistic   price
		             TEXT FLOAT64
		0  count_excluded     2.0
		1            mean    20.0
		2             max    30.0
		"""
		if description is None:
			description = Description()

		described_frame = describe_frame(self._frame, description)
		described_table = self._wrap(described_frame)

		return described_table
