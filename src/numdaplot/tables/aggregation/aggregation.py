"""
Settings of the aggregation of the rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.duplicate_column_error import RESULT_NAME_ADVICE, DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.aggregation.calculation import Calculation, find_result_name
from numdaplot.tables.columns.column_names import require_column_names

CALCULATION_ITEM_NAME = "calculation"
GROUP_COLUMN_ITEM_NAME = "group column"


@dataclass(frozen=True)
class Aggregation:
	"""
	Statistics computed on the whole Table or on each group of rows, used by ``Table.aggregate``.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		The error for a repeated result name advises a ``result_name`` for each calculation.

	Parameters
	----------
	calculations
		The statistics to compute, at least one. The aggregation keeps its own copy of the list.
	group_by
		The names of the columns whose values form the groups: one result row per combination
		of values. The whole Table gives a single row when omitted.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``calculations`` or ``group_by`` is an empty list.
	InvalidColumnNameError
		When a group column name is an empty text.
	DuplicateColumnError
		When a name appears twice among the group columns and the result names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> average_price = ndp.Calculation(column="price", function=ndp.Mean())
	>>> sales.aggregate(ndp.Aggregation(calculations=[average_price], group_by=["city"]))
	    city price_mean
	    TEXT    FLOAT64
	0   Lyon       80.0
	1  Paris      135.0
	"""

	calculations: list[Calculation]
	group_by: list[str] | None = None

	def __post_init__(self) -> None:
		"""
		Check the lists and replace them with copies that only the aggregation holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``calculations`` or ``group_by`` is an empty list.
		InvalidColumnNameError
			When a group column name is an empty text.
		DuplicateColumnError
			When a name appears twice among the group columns and the result names.
		"""
		require_field_types(self)

		if self.calculations == []:
			raise EmptyListError(CALCULATION_ITEM_NAME)

		if self.group_by == []:
			raise EmptyListError(GROUP_COLUMN_ITEM_NAME)

		calculations_copy = list(self.calculations)
		object.__setattr__(self, "calculations", calculations_copy)
		group_names = list[str]()
		if self.group_by is not None:
			require_column_names(self.group_by)
			group_by_copy = list(self.group_by)
			object.__setattr__(self, "group_by", group_by_copy)
			group_names.extend(group_by_copy)

		require_unique_result_names(calculations_copy, group_names)


def require_unique_result_names(calculations: list[Calculation], group_names: list[str]) -> None:
	"""
	Check that each calculation gives a result name of its own, different from the group column names.

	.. versionadded:: 0.2.0

	Parameters
	----------
	calculations
		The calculations of the aggregation.
	group_names
		The names of the group columns, already distinct.

	Raises
	------
	DuplicateColumnError
		At the first result name already used, advising a ``result_name`` for each calculation.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.aggregation import require_unique_result_names
	>>> total = ndp.Calculation(column="price", function=ndp.Sum(), result_name="city")
	>>> try:
	... 	require_unique_result_names([total], ["city"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'city' appears more than once. Give each Calculation its own result_name.
	"""
	used_names = set(group_names)

	for calculation in calculations:
		result_name = find_result_name(calculation)
		if result_name in used_names:
			raise DuplicateColumnError(result_name, advice=RESULT_NAME_ADVICE)

		used_names.add(result_name)
