"""
A rule applied to one or several columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.rules.rule import Rule
from numdaplot.settings.setting_types import require_list_not_text, require_object_not_class
from numdaplot.tables.columns.column_names import require_unique_names
from numdaplot.tables.filtering.column_match import ColumnMatch

COLUMN_ITEM_NAME = "column"
COLUMNS_SETTING = "Condition columns"
RULE_SETTING = "Condition rule"
RULE_EXPECTED = "a rule such as ndp.Greater(10)"


@dataclass(frozen=True)
class Condition:
	"""
	A rule applied to one or several columns of a Table, used by ``Filter``.

	A missing value only satisfies ``IsMissing``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		A ``Rule``, such as ``ndp.Greater(100)`` or ``ndp.IsIn(["Paris"])``: see ``Rule`` for every rule.
	columns
		The names of the columns the rule applies to, every column when omitted.
		The condition keeps its own copy of the list.
	mode
		Whether one column satisfying the rule is enough, which is the default, or every column must.

	Raises
	------
	InvalidSettingTypeError
		When ``rule`` is a class written without its parentheses, or ``columns`` is a single text.
	EmptyListError
		When ``columns`` is an empty list.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([120.0, 80.0, 90.0])
	>>> costs = ndp.Array.from_list([70.0, 60.0, 110.0])
	>>> sales = ndp.Table.from_arrays({"price": prices, "cost": costs})
	>>> above_hundred = ndp.Condition(rule=ndp.Greater(100), columns=["price", "cost"])
	>>> sales.filter(ndp.Filter(conditions=[above_hundred]))
	    price    cost
	  FLOAT64 FLOAT64
	0   120.0    70.0
	1    90.0   110.0
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
		InvalidSettingTypeError
			When ``rule`` is a class, written without its parentheses.
		InvalidSettingTypeError
			When ``columns`` is a single text instead of a list.
		EmptyListError
			When ``columns`` is an empty list.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_object_not_class(RULE_SETTING, RULE_EXPECTED, self.rule)
		require_list_not_text(COLUMNS_SETTING, self.columns)

		if self.columns is None:
			return

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_unique_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
