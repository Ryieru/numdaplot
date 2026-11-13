"""
Settings of the description of the columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.duplicate_statistic_error import DuplicateStatisticError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.field_types import require_field_types
from numdaplot.statistics.count import Count
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.aggregation.statistic_name import name_statistic
from numdaplot.tables.columns.column_names import copy_column_names

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


@dataclass(frozen=True)
class Description:
	"""
	Statistics describing columns of a Table, used by ``Table.describe``.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		Refuses two statistics giving rows of the same name, such as two ``Share``.

	Parameters
	----------
	functions
		The ``Statistic`` objects, one row each, such as ``[ndp.Min(), ndp.Quantile(0.9)]``: see ``Statistic``
		for every statistic. When omitted: ``Count``, ``Mean``, ``StandardDeviation``, ``Min``,
		``Quantile(0.25)``, ``Median``, ``Quantile(0.75)`` and ``Max``, as in pandas.
	columns
		The names of the columns to describe, one result column each. Every number column when omitted.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``functions`` or ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.
	DuplicateStatisticError
		When a statistic appears twice in ``functions``, or two statistics give rows of the same name, such as two
		``Share``.
	RefusedOperationError
		When a statistic is not a statistic of numdaplot.

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
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``functions`` or ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		DuplicateStatisticError
			When a statistic appears twice in ``functions``, or two statistics give rows of the same name.
		RefusedOperationError
			When a statistic is not a statistic of numdaplot.
		"""
		require_field_types(self)

		if self.functions == []:
			raise EmptyListError(FUNCTION_ITEM_NAME)

		if self.functions is not None:
			require_distinct_statistics(self.functions)
			functions_copy = list(self.functions)
			object.__setattr__(self, "functions", functions_copy)

		if self.columns is not None:
			columns_copy = copy_column_names(self.columns)
			object.__setattr__(self, "columns", columns_copy)


def require_distinct_statistics(functions: list[Statistic]) -> None:
	"""
	Check that the statistics of a description give rows of different names.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		Compares the names of the rows, so that two ``Share`` with different rules are refused.

	Parameters
	----------
	functions
		The statistics of the description.

	Raises
	------
	DuplicateStatisticError
		When a statistic appears twice, or two statistics give rows of the same name.
	RefusedOperationError
		When a statistic is not a statistic of numdaplot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.description.description import require_distinct_statistics
	>>> require_distinct_statistics([ndp.Quantile(0.25), ndp.Quantile(0.75)])
	>>> try:
	... 	require_distinct_statistics([ndp.Mean(), ndp.Mean()])
	... except ndp.DuplicateStatisticError as error:
	... 	print(error)
	The statistic Mean() appears more than once.
	"""
	seen_statistics = dict[str, Statistic]()

	for function in functions:
		function_name = name_statistic(function)
		if function_name not in seen_statistics:
			seen_statistics[function_name] = function
			continue

		seen_function = seen_statistics[function_name]
		if seen_function == function:
			raise DuplicateStatisticError(function)

		raise DuplicateStatisticError(seen_function, function)
