"""
Unit tests of the checks of column names.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.tables.columns.column_names import (
	copy_column_names,
	require_column_name,
	require_column_names,
	require_known_columns,
	require_optional_column_name,
	require_unique_names,
)

GIVEN_NAMES = ["city", "price"]
EXPECTED_NAMES = ["city", "price"]
ADDED_NAME = "count"
NO_NAMES = list[str]()
VALID_NAME = "price"
REJECTED_NAMES = ["", 0, None]
UNIQUE_NAMES = ["city", "price"]
REPEATED_NAMES = ["city", "price", "city"]
REPEATED_NAME = "city"
NAMES_WITH_NUMBER = ["city", 1]
UNKNOWN_NAMES = ["price", "prise"]
UNKNOWN_NAME = "prise"


def test_require_column_name_accepts_a_text() -> None:
	"""
	Check that a non-empty text passes.

	.. versionadded:: 0.1.0
	"""
	require_column_name(VALID_NAME)


@pytest.mark.parametrize("column_name", REJECTED_NAMES)
def test_require_column_name_rejects_an_empty_text_or_another_value(column_name: object) -> None:
	"""
	Check that an empty text, a number or None raises InvalidColumnNameError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		A rejected name.
	"""
	with pytest.raises(InvalidColumnNameError):
		require_column_name(column_name)


def test_require_unique_names_accepts_different_names() -> None:
	"""
	Check that different names pass.

	.. versionadded:: 0.1.0
	"""
	require_unique_names(UNIQUE_NAMES)


def test_require_unique_names_names_the_repeated_name() -> None:
	"""
	Check that the repeated name is the one in the error.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError) as error_info:
		require_unique_names(REPEATED_NAMES)

	error = error_info.value
	assert error.column_name == REPEATED_NAME


def test_require_column_names_rejects_a_number() -> None:
	"""
	Check that a number among names raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		require_column_names(NAMES_WITH_NUMBER)


def test_require_column_names_rejects_a_repeated_name() -> None:
	"""
	Check that a repeated name raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		require_column_names(REPEATED_NAMES)


def test_require_known_columns_names_the_unknown_column() -> None:
	"""
	Check that the first unknown name is the one in the error.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError) as error_info:
		require_known_columns(UNKNOWN_NAMES, UNIQUE_NAMES)

	error = error_info.value
	assert error.column_name == UNKNOWN_NAME


def test_require_optional_column_name_accepts_none() -> None:
	"""
	Check that an omitted name passes.

	.. versionadded:: 0.1.0
	"""
	require_optional_column_name(None)


def test_require_optional_column_name_rejects_an_empty_text() -> None:
	"""
	Check that an empty name raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		require_optional_column_name("")


def test_copy_column_names_gives_a_list_of_its_own() -> None:
	"""
	Check that the copy keeps the names, and does not change with the given list.

	.. versionadded:: 0.2.0
	"""
	given_names = list(GIVEN_NAMES)
	names_copy = copy_column_names(given_names)

	given_names.append(ADDED_NAME)

	assert names_copy == EXPECTED_NAMES


def test_copy_column_names_rejects_an_empty_list() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(EmptyListError):
		copy_column_names(NO_NAMES)


def test_copy_column_names_rejects_a_repeated_name() -> None:
	"""
	Check that a name given twice raises DuplicateColumnError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(DuplicateColumnError):
		copy_column_names(REPEATED_NAMES)
