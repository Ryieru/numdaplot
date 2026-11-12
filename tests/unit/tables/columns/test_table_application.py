"""
Unit tests of TableApplication.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.arrays.math_functions.square_root import SquareRoot
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.tables.columns.table_application import TableApplication

FUNCTION = SquareRoot()
COLUMN_NAMES = ["area", "volume"]
EXPECTED_COLUMN_NAMES = ["area", "volume"]
ADDED_NAME = "weight"
EMPTY_NAMES = list[str]()
REPEATED_NAMES = ["area", "area"]
NAMES_WITH_EMPTY_NAME = ["area", ""]
COLUMN_NAME = "area"


def test_table_application_keeps_its_own_copy_of_the_columns() -> None:
	"""
	Check that changing the given list afterwards leaves the application unchanged.

	.. versionadded:: 0.2.0
	"""
	column_names = list(COLUMN_NAMES)
	application = TableApplication(function=FUNCTION, columns=column_names)

	column_names.append(ADDED_NAME)

	assert application.columns == EXPECTED_COLUMN_NAMES


def test_table_application_rejects_no_column() -> None:
	"""
	Check that an empty list of columns raises EmptyListError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(EmptyListError):
		TableApplication(function=FUNCTION, columns=EMPTY_NAMES)


def test_table_application_rejects_a_repeated_column() -> None:
	"""
	Check that a column given twice raises DuplicateColumnError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(DuplicateColumnError):
		TableApplication(function=FUNCTION, columns=REPEATED_NAMES)


def test_table_application_rejects_an_empty_column_name() -> None:
	"""
	Check that an empty column name raises InvalidColumnNameError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidColumnNameError):
		TableApplication(function=FUNCTION, columns=NAMES_WITH_EMPTY_NAME)


def test_table_application_rejects_a_column_name_instead_of_a_list() -> None:
	"""
	Check that one name given without list raises InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidTypeError):
		TableApplication(function=FUNCTION, columns=COLUMN_NAME)  # pyright: ignore[reportArgumentType]
