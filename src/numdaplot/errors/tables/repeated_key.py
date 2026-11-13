"""
Key repeated in a Table where a join expects each key once, given to JoinRelationError.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RepeatedKey:
	"""
	The first key repeated in a Table, the combination of its values for several key columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_names
		The names of the key columns.
	key_values
		The value of each key column, in the same order.
	count
		The number of rows having these values.

	Examples
	--------
	>>> from numdaplot.errors.tables.repeated_key import RepeatedKey
	>>> RepeatedKey(["Num_Acc"], [202500000001], 3).count
	3
	"""

	key_names: list[str]
	key_values: list[Any]
	count: int
