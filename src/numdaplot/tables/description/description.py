"""
Settings of the description of the columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.duplicate_statistic_error import DuplicateStatisticError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.setting_types import require_list_not_text, require_object_not_class
from numdaplot.statistics.count import Count
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.columns.column_names import require_column_names

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
COLUMNS_SETTING = "Description columns"
FUNCTION_SETTING = "Description functions"
FUNCTION_EXPECTED = "a statistic such as ndp.Mean()"


@dataclass(frozen=True)
class Description:
	"""
	Statistics describing columns of a Table, used by ``Table.describe``.

	.. versionadded:: 0.1.0

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
	InvalidSettingTypeError
		When ``columns`` is a single text instead of a list, or a function is a class written without its
		parentheses.
	EmptyListError
		When ``functions`` or ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.
	DuplicateStatisticError
		When a statistic appears twice in ``functions``.

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
		InvalidSettingTypeError
			When ``columns`` is a single text instead of a list, or a function is a class.
		EmptyListError
			When ``functions`` or ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		DuplicateStatisticError
			When a statistic appears twice in ``functions``.
		"""
		require_list_not_text(COLUMNS_SETTING, self.columns)

		if self.functions == []:
			raise EmptyListError(FUNCTION_ITEM_NAME)

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		if self.functions is not None:
			require_distinct_statistics(self.functions)
			functions_copy = list(self.functions)
			object.__setattr__(self, "functions", functions_copy)

		if self.columns is not None:
			require_column_names(self.columns)
			columns_copy = list(self.columns)
			object.__setattr__(self, "columns", columns_copy)


def require_distinct_statistics(functions: list[Statistic]) -> None:
	"""
	Check that the statistics of a description are objects, each one given once.

	.. versionadded:: 0.1.0

	Parameters
	----------
	functions
		The statistics of the description.

	Raises
	------
	InvalidSettingTypeError
		When a statistic is a class, written without its parentheses.
	DuplicateStatisticError
		When a statistic appears twice, with the same settings.

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
	seen_statistics = set[Statistic]()

	for function in functions:
		require_object_not_class(FUNCTION_SETTING, FUNCTION_EXPECTED, function)

		if function in seen_statistics:
			raise DuplicateStatisticError(function)

		seen_statistics.add(function)
