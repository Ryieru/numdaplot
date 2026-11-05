"""
Statistics of a Table: aggregation and description.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.aggregation.aggregated_frame import aggregate_frame
from numdaplot.tables.aggregation.aggregation import Aggregation
from numdaplot.tables.description.described_frame import describe_frame
from numdaplot.tables.description.description import Description
from numdaplot.tables.table_data import TableData


class TableCalculation(TableData):
	"""
	Statistics of a Table with ``aggregate`` and ``describe``. Missing values are ignored.

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
		0     count     2.0
		1      mean    20.0
		2       max    30.0
		"""
		if description is None:
			description = Description()

		described_frame = describe_frame(self._frame, description)
		described_table = self._wrap(described_frame)

		return described_table
