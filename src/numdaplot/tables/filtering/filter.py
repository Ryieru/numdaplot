"""
Settings of the filter of the rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
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
		Whether a row must satisfy every condition, which is the default, or at least one.

	Raises
	------
	EmptyListError
		When ``conditions`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
	>>> in_paris = ndp.Condition(rule=ndp.Equal("Paris"), columns=["city"])
	>>> ndp.Filter(conditions=[expensive, in_paris], mode=ndp.FilterMode.ANY).mode
	<FilterMode.ANY: 2>
	"""

	conditions: list[Condition]
	mode: FilterMode = FilterMode.ALL

	def __post_init__(self) -> None:
		"""
		Check that there is a condition and replace the list with a copy that only the filter holds.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyListError
			When ``conditions`` is empty.
		"""
		if self.conditions == []:
			raise EmptyListError(CONDITION_ITEM_NAME)

		conditions_copy = list(self.conditions)
		object.__setattr__(self, "conditions", conditions_copy)
