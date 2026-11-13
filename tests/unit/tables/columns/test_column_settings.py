"""
Unit tests of ColumnChoice, NameChange, Renaming and NewColumn.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.array import Array
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.files.conflict import Conflict
from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.column_mode import ColumnMode
from numdaplot.tables.columns.name_change import NameChange
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renaming import Renaming

COLUMN_NAMES = ["city", "price"]
REPEATED_NAMES = ["city", "city"]
EMPTY_NAMES = list[str]()
EMPTY_NAME = ""
COLUMN_NAME = "price"
VALUES = Array.from_list([1.5])


def test_column_choice_keeps_its_columns_by_default() -> None:
	"""
	Check the default mode.

	.. versionadded:: 0.1.0
	"""
	choice = ColumnChoice(columns=COLUMN_NAMES)

	assert choice.mode == ColumnMode.KEEP


def test_column_choice_keeps_its_own_copy_of_the_columns() -> None:
	"""
	Check that changing the given list does not change the choice.

	.. versionadded:: 0.1.0
	"""
	column_names = list(COLUMN_NAMES)
	choice = ColumnChoice(columns=column_names)

	column_names.clear()

	assert choice.columns == COLUMN_NAMES


def test_column_choice_rejects_keeping_no_column() -> None:
	"""
	Check that an empty list with KEEP raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		ColumnChoice(columns=EMPTY_NAMES)


def test_column_choice_accepts_dropping_no_column() -> None:
	"""
	Check that an empty list with DROP is accepted.

	.. versionadded:: 0.1.0
	"""
	choice = ColumnChoice(columns=EMPTY_NAMES, mode=ColumnMode.DROP)

	assert choice.columns == EMPTY_NAMES


def test_column_choice_rejects_a_repeated_column() -> None:
	"""
	Check that a repeated name raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		ColumnChoice(columns=REPEATED_NAMES)


def test_name_change_rejects_an_empty_new_name() -> None:
	"""
	Check that an empty new name raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		NameChange(old_name=COLUMN_NAME, new_name=EMPTY_NAME)


def test_renaming_rejects_no_change() -> None:
	"""
	Check that an empty list of changes raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Renaming(changes=[])


@pytest.mark.parametrize(
	"changes",
	[
		[NameChange(old_name="city", new_name="town"), NameChange(old_name="city", new_name="place")],
		[NameChange(old_name="city", new_name="place"), NameChange(old_name="price", new_name="place")],
	],
)
def test_renaming_rejects_a_column_renamed_twice_or_a_new_name_given_twice(changes: list[NameChange]) -> None:
	"""
	Check that a repeated old name or a repeated new name raises DuplicateColumnError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	changes
		Changes repeating a name.
	"""
	with pytest.raises(DuplicateColumnError):
		Renaming(changes=changes)


def test_renaming_keeps_its_own_copy_of_the_changes() -> None:
	"""
	Check that changing the given list afterwards changes nothing.

	.. versionadded:: 0.1.0
	"""
	changes = [NameChange(old_name="city", new_name="town")]
	renaming = Renaming(changes=changes)

	changes.clear()

	change_count = len(renaming.changes)
	assert change_count == 1


def test_new_column_refuses_an_existing_name_by_default() -> None:
	"""
	Check the default conflict setting.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name=COLUMN_NAME, values=VALUES)

	assert new_column.on_conflict == Conflict.ERROR


def test_new_column_rejects_an_empty_name() -> None:
	"""
	Check that an empty name raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		NewColumn(name=EMPTY_NAME, values=VALUES)
