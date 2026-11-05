"""
Settings of the filter of the rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter_mode import FilterMode

CONDITION_ITEM_NAME = "condition"


@dataclass(frozen=True)
class Filter:
	"""
	Conditions a row must satisfy to be kept, used by ``Table.filter``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	conditions
		The conditions, at least one. The filter keeps its own copy of the list.
	mode
		Whether a row must satisfy every condition, ``FilterMode.ALL`` by default, or at least one, ``FilterMode.ANY``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``conditions`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
	>>> in_lyon = ndp.Condition(rule=ndp.Equal("Lyon"), columns=["city"])
	>>> sales.filter(ndp.Filter(conditions=[expensive, in_lyon]))
	Empty DataFrame
	Columns: [(city, TEXT), (price, FLOAT64)]
	Index: []
	"""

	conditions: list[Condition]
	mode: FilterMode = FilterMode.ALL

	def __post_init__(self) -> None:
		"""
		Check that there is a condition and replace the list with a copy that only the filter holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``conditions`` is empty.
		"""
		require_field_types(self)

		if self.conditions == []:
			raise EmptyListError(CONDITION_ITEM_NAME)

		conditions_copy = list(self.conditions)
		object.__setattr__(self, "conditions", conditions_copy)
