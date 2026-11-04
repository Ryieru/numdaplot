"""
A rule applied to one or several columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.rules.rule import Rule
from numdaplot.tables.columns.column_names import require_unique_names
from numdaplot.tables.filtering.column_match import ColumnMatch

COLUMN_ITEM_NAME = "column"


@dataclass(frozen=True)
class Condition:
	"""
	A rule applied to one or several columns of a Table, used by ``Filter``.

	A missing value only satisfies ``IsMissing``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		Any rule of numdaplot, such as ``ndp.Greater(100)``.
	columns
		The names of the columns the rule applies to, every column when omitted.
		The condition keeps its own copy of the list.
	mode
		Whether one column satisfying the rule is enough, which is the default, or every column must.

	Raises
	------
	EmptyListError
		When ``columns`` is an empty list.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
	>>> sales.filter(ndp.Filter(conditions=[expensive]))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1  Paris   150.0
	"""

	rule: Rule
	columns: list[str] | None = None
	mode: ColumnMatch = ColumnMatch.ANY

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the condition holds.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyListError
			When ``columns`` is an empty list.
		DuplicateColumnError
			When a column name appears twice.
		"""
		if self.columns is None:
			return

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_unique_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
