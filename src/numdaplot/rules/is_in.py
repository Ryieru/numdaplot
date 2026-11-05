"""
Rule keeping the values that belong to a list.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from numdaplot.errors.empty_values_error import EmptyValuesError
from numdaplot.rules.rule import Rule
from numdaplot.settings.field_types import require_field_types


# The type parameter has the name of the alias holding the same types: the documentation shows the alias,
# and every accepted value must be of one type.
@dataclass(frozen=True)
class IsIn[ScalarValue: (bool, int, float, str, date, datetime, timedelta)](Rule):
	"""
	Keep the values that belong to a list of accepted values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The accepted values, a list of ``ScalarValue`` such as ``["Paris", "Lyon"]`` or ``[1, 2]``, at least one and
		all of the same kind. The rule keeps its own copy, so changing the list afterwards does not change the rule.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyValuesError
		When ``values`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> countries = ndp.Array.from_list(["FR", "US", "DE"])
	>>> countries.select(ndp.IsIn(["FR", "DE"]))
	Array(['FR', 'DE'], dtype=TEXT)
	"""

	values: list[ScalarValue]

	def __post_init__(self) -> None:
		"""
		Check the list and its values, then replace it with a copy that only the rule holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyValuesError
			When ``values`` is empty.
		"""
		require_field_types(self)

		value_count = len(self.values)
		if value_count == 0:
			raise EmptyValuesError()

		values_copy = list(self.values)
		object.__setattr__(self, "values", values_copy)
