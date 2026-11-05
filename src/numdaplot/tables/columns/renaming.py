"""
The new names of columns of a Table, applied at once.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_unique_names
from numdaplot.tables.columns.name_change import NameChange

CHANGE_ITEM_NAME = "name change"


@dataclass(frozen=True)
class Renaming:
	"""
	The new names of columns of a Table, applied at once, used by ``Table.rename``.

	Two columns can swap their names in a single renaming.

	.. versionadded:: 0.1.0

	Parameters
	----------
	changes
		The ``NameChange`` of each renamed column, at least one. The renaming keeps its own copy of the list.

	Raises
	------
	InvalidSettingTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``changes`` is an empty list.
	DuplicateColumnError
		When a column is renamed twice, or two columns receive the same new name.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> low = ndp.Array.from_list([1.0, 2.0])
	>>> high = ndp.Array.from_list([9.0, 8.0])
	>>> bounds = ndp.Table.from_arrays({"low": low, "high": high})
	>>> swap = [ndp.NameChange(old_name="low", new_name="high"), ndp.NameChange(old_name="high", new_name="low")]
	>>> bounds.rename(ndp.Renaming(changes=swap))
	     high     low
	  FLOAT64 FLOAT64
	0     1.0     9.0
	1     2.0     8.0
	"""

	changes: list[NameChange]

	def __post_init__(self) -> None:
		"""
		Check the list of changes and replace it with a copy that only the renaming holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``changes`` is an empty list.
		DuplicateColumnError
			When a column is renamed twice, or two columns receive the same new name.
		"""
		require_field_types(self)

		if self.changes == []:
			raise EmptyListError(CHANGE_ITEM_NAME)

		old_names = [change.old_name for change in self.changes]
		require_unique_names(old_names)
		new_names = [change.new_name for change in self.changes]
		require_unique_names(new_names)
		changes_copy = list(self.changes)
		object.__setattr__(self, "changes", changes_copy)
