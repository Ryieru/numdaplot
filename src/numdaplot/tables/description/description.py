"""
Settings of the description of the columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.statistics.count import Count
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.columns.column_names import require_unique_names

LOWER_QUARTILE = 0.25
UPPER_QUARTILE = 0.75
DEFAULT_FUNCTIONS = (
	Count(),
	Mean(),
	StandardDeviation(),
	Min(),
	Quantile(LOWER_QUARTILE),
	Median(),
	Quantile(UPPER_QUARTILE),
	Max(),
)
FUNCTION_ITEM_NAME = "function"
COLUMN_ITEM_NAME = "column"


@dataclass(frozen=True)
class Description:
	"""
	Statistics describing columns of a Table, used by ``Table.describe``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	functions
		The statistics, one row each. When omitted: ``Count``, ``Mean``, ``StandardDeviation``, ``Min``,
		``Quantile(0.25)``, ``Median``, ``Quantile(0.75)`` and ``Max``, as in pandas.
	columns
		The names of the columns to describe, one result column each. Every number column when omitted.

	Raises
	------
	EmptyListError
		When ``functions`` or ``columns`` is an empty list.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.describe(ndp.Description(functions=[ndp.Min(), ndp.Mean(), ndp.Max()]))
	statistic       price
	TEXT     FLOAT64
	0       min   80.000000
	1      mean  116.666667
	2       max  150.000000
	"""

	functions: list[Statistic] | None = None
	columns: list[str] | None = None

	def __post_init__(self) -> None:
		"""
		Check the lists and replace them with copies that only the description holds.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyListError
			When ``functions`` or ``columns`` is an empty list.
		DuplicateColumnError
			When a column name appears twice.
		"""
		if self.functions == []:
			raise EmptyListError(FUNCTION_ITEM_NAME)

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		if self.functions is not None:
			functions_copy = list(self.functions)
			object.__setattr__(self, "functions", functions_copy)

		if self.columns is not None:
			require_unique_names(self.columns)
			columns_copy = list(self.columns)
			object.__setattr__(self, "columns", columns_copy)
