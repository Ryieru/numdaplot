"""
Unit tests of the choice, renaming and addition of Table columns.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.arrays.array import Array
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.files.conflict import Conflict
from numdaplot.tables.columns.added_column import add_frame_column
from numdaplot.tables.columns.chosen_columns import choose_frame_columns
from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.column_mode import ColumnMode
from numdaplot.tables.columns.name_change import NameChange
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renamed_columns import rename_frame_columns
from numdaplot.tables.columns.renaming import Renaming

FRAME = pandas.DataFrame({"city": ["Pau", "Lyon"], "price": [1.5, 8.0], "count": [1, 2]})
EXPECTED_KEPT_NAMES = ["count", "city"]
EXPECTED_REMAINING_NAMES = ["city", "count"]
EXPECTED_RENAMED_NAMES = ["town", "price", "count"]
EXPECTED_SWAPPED_NAMES = ["price", "city", "count"]
COUNTS = Array.from_list([3, 4])
SHORT_COUNTS = Array.from_list([3])
GRID = Array.from_list([[1, 2], [3, 4]])
EXPECTED_ADDED_NAMES = ["city", "price", "count", "visits"]
EXPECTED_REPLACED_COUNTS = [3, 4]
EXPECTED_ORIGINAL_NAMES = ["city", "price", "count"]
EMPTY_FRAME = pandas.DataFrame()
EXPECTED_NEW_ROW_COUNT = 2


def test_choose_frame_columns_keeps_the_order_of_the_list() -> None:
	"""
	Check that KEEP gives the named columns in the order of the list.

	.. versionadded:: 0.1.0
	"""
	choice = ColumnChoice(columns=["count", "city"])

	chosen_frame = choose_frame_columns(FRAME, choice)

	column_names = chosen_frame.columns.tolist()
	assert column_names == EXPECTED_KEPT_NAMES


def test_choose_frame_columns_drops_the_named_columns() -> None:
	"""
	Check that DROP removes the named columns and keeps the order of the others.

	.. versionadded:: 0.1.0
	"""
	choice = ColumnChoice(columns=["price"], mode=ColumnMode.DROP)

	chosen_frame = choose_frame_columns(FRAME, choice)

	column_names = chosen_frame.columns.tolist()
	assert column_names == EXPECTED_REMAINING_NAMES


def test_choose_frame_columns_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	choice = ColumnChoice(columns=["prise"])

	with pytest.raises(ColumnNotFoundError):
		choose_frame_columns(FRAME, choice)


def test_rename_frame_columns_renames_in_place() -> None:
	"""
	Check that a renamed column keeps its place.

	.. versionadded:: 0.1.0
	"""
	renaming = Renaming(changes=[NameChange(old_name="city", new_name="town")])

	renamed_frame = rename_frame_columns(FRAME, renaming)

	column_names = renamed_frame.columns.tolist()
	assert column_names == EXPECTED_RENAMED_NAMES


def test_rename_frame_columns_swaps_two_names() -> None:
	"""
	Check that two columns can swap their names in one call.

	.. versionadded:: 0.1.0
	"""
	swap = [NameChange(old_name="city", new_name="price"), NameChange(old_name="price", new_name="city")]
	renaming = Renaming(changes=swap)

	renamed_frame = rename_frame_columns(FRAME, renaming)

	column_names = renamed_frame.columns.tolist()
	assert column_names == EXPECTED_SWAPPED_NAMES


def test_rename_frame_columns_rejects_an_existing_new_name() -> None:
	"""
	Check that renaming to a name kept by another column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	renaming = Renaming(changes=[NameChange(old_name="city", new_name="price")])

	with pytest.raises(DuplicateColumnError):
		rename_frame_columns(FRAME, renaming)


def test_rename_frame_columns_rejects_an_unknown_column() -> None:
	"""
	Check that renaming an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	renaming = Renaming(changes=[NameChange(old_name="prise", new_name="cost")])

	with pytest.raises(ColumnNotFoundError):
		rename_frame_columns(FRAME, renaming)


def test_add_frame_column_places_a_new_column_last() -> None:
	"""
	Check that a new column comes after the others, and the original frame does not change.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name="visits", values=COUNTS)

	extended_frame = add_frame_column(FRAME, new_column)

	column_names = extended_frame.columns.tolist()
	original_names = FRAME.columns.tolist()
	assert column_names == EXPECTED_ADDED_NAMES
	assert original_names == EXPECTED_ORIGINAL_NAMES


def test_add_frame_column_replaces_an_existing_column_at_its_place() -> None:
	"""
	Check that REPLACE changes the values of the column without moving it.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name="count", values=COUNTS, on_conflict=Conflict.REPLACE)

	extended_frame = add_frame_column(FRAME, new_column)

	column_names = extended_frame.columns.tolist()
	count_column = extended_frame["count"]
	counts = count_column.tolist()
	assert column_names == EXPECTED_ORIGINAL_NAMES
	assert counts == EXPECTED_REPLACED_COUNTS


def test_add_frame_column_rejects_an_existing_name() -> None:
	"""
	Check that an existing name raises DuplicateColumnError with ERROR.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name="count", values=COUNTS)

	with pytest.raises(DuplicateColumnError):
		add_frame_column(FRAME, new_column)


def test_add_frame_column_rejects_a_wrong_length() -> None:
	"""
	Check that one value for two rows raises ShapeMismatchError.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name="visits", values=SHORT_COUNTS)

	with pytest.raises(ShapeMismatchError):
		add_frame_column(FRAME, new_column)


def test_add_frame_column_rejects_a_grid() -> None:
	"""
	Check that a two-dimensional Array raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name="visits", values=GRID)

	with pytest.raises(DimensionError):
		add_frame_column(FRAME, new_column)


def test_add_frame_column_gives_its_rows_to_a_table_without_column() -> None:
	"""
	Check that a Table without column takes the length of the new column.

	.. versionadded:: 0.1.0
	"""
	new_column = NewColumn(name="visits", values=COUNTS)

	extended_frame = add_frame_column(EMPTY_FRAME, new_column)

	row_count = len(extended_frame)
	assert row_count == EXPECTED_NEW_ROW_COUNT
