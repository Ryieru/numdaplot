"""
Unit tests of Region.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import pytest

from numdaplot.errors.positions.empty_region_error import EmptyRegionError
from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.tables.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.types.invalid_type_error import InvalidTypeError
from numdaplot.positions.index import Index
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region

COLUMN_NAMES = ["mois", "total"]
ADDED_COLUMN = "prix"
FIRST_ROW = Index(0)
FIRST_ROWS = Range(start=0, stop=4)


def test_region_refuses_neither_rows_nor_columns() -> None:
	"""
	Check that a Region without rows and columns raises EmptyRegionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyRegionError):
		Region()


def test_region_takes_every_column_when_columns_are_omitted() -> None:
	"""
	Check that columns stay None, meaning every column, when only rows are given.

	.. versionadded:: 0.1.0
	"""
	region = Region(rows=FIRST_ROW)

	assert region.columns is None


def test_region_keeps_positions_as_given() -> None:
	"""
	Check that an Index and a Range are kept as they are.

	.. versionadded:: 0.1.0
	"""
	region = Region(rows=FIRST_ROWS, columns=FIRST_ROW)

	assert region.rows == FIRST_ROWS
	assert region.columns == FIRST_ROW


def test_region_is_not_changed_by_a_later_change_of_the_given_column_names() -> None:
	"""
	Check that the region holds its own copy of the list of column names.

	.. versionadded:: 0.1.0
	"""
	given_columns = list(COLUMN_NAMES)
	region = Region(columns=given_columns)

	given_columns.append(ADDED_COLUMN)

	assert region.columns == COLUMN_NAMES


@pytest.mark.parametrize(("rows", "columns"), [(0, None), ([0, 1], None), (None, "price")])
def test_region_rejects_positions_of_another_kind(rows: object, columns: object) -> None:
	"""
	Check that a number, a list of rows or a single column text raises InvalidTypeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rows
		The rows given.
	columns
		The columns given.
	"""
	untyped_region = cast(Any, Region)

	with pytest.raises(InvalidTypeError):
		untyped_region(rows=rows, columns=columns)


@pytest.mark.parametrize(
	("columns", "error_class"),
	[([], EmptyListError), (["price", "price"], DuplicateColumnError), ([""], InvalidColumnNameError)],
)
def test_region_rejects_an_empty_or_wrong_list_of_columns(columns: list[str], error_class: type[Exception]) -> None:
	"""
	Check that an empty list, a repeated name or an empty name is refused when the Region is created.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		The rejected list of column names.
	error_class
		The expected error.
	"""
	with pytest.raises(error_class):
		Region(columns=columns)
