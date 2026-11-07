"""
Settings of a join of two Tables.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.joining.join_mode import JoinMode
from numdaplot.tables.joining.join_suffixes import JoinSuffixes
from numdaplot.tables.joining.key_types import KeyTypes

if TYPE_CHECKING:
	from numdaplot.tables.table import Table

KEY_ITEM_NAME = "key"


# eq=False because comparing two settings would compare their Tables with ==, which they refuse.
@dataclass(frozen=True, eq=False)
class Join:
	"""
	Settings of a join of two Tables on the values of key columns, used by ``Table.join``.

	Each row of the joined Table meets each row of the other Table having the same keys. A missing key never matches,
	as in SQL. The rows of the joined Table come first, in their order, then the unmatched rows of the other Table.
	The columns are the keys, then the other columns of the joined Table, then those of the other Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	other
		The Table joined to this one.
	keys
		The names of the key columns, which both Tables have: rename them with ``Table.rename`` first when they differ.
		Several keys match on their combination. The join keeps its own copy of the list.
	mode
		Which rows are kept, ``JoinMode.INNER`` by default: only the rows whose keys match.
	suffixes
		The suffixes of the columns both Tables have besides the keys. When omitted, such a column raises
		``DuplicateColumnError``.
	key_types
		How close the types of each key must be, ``KeyTypes.SAME_FAMILY`` by default: ``INT64`` matches ``FLOAT64``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``keys`` is an empty list.
	InvalidColumnNameError
		When a name in ``keys`` is an empty text.
	DuplicateColumnError
		When a name appears twice in ``keys``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2]), "dep": ndp.Array.from_list(["75", "69"])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 1]), "age": ndp.Array.from_list([34, 8])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"]))
	     id  dep   age
	  INT64 TEXT INT64
	0     1   75    34
	1     1   75     8
	"""

	other: Table
	keys: list[str]
	mode: JoinMode = JoinMode.INNER
	suffixes: JoinSuffixes | None = None
	key_types: KeyTypes = KeyTypes.SAME_FAMILY

	def __post_init__(self) -> None:
		"""
		Check the keys and replace them with a copy that only the join holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``keys`` is an empty list.
		InvalidColumnNameError
			When a name in ``keys`` is an empty text.
		DuplicateColumnError
			When a name appears twice in ``keys``.
		"""
		require_field_types(self)

		if self.keys == []:
			raise EmptyListError(KEY_ITEM_NAME)

		require_column_names(self.keys)
		keys_copy = list(self.keys)
		object.__setattr__(self, "keys", keys_copy)
