"""
Unit tests of TableConversion.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.types.type import Type

COLUMN_NAME = "price"
COLUMN_NAMES = [COLUMN_NAME]
EXPECTED_COLUMN_NAMES = ["price"]
ADDED_NAME = "cost"
EMPTY_NAMES = list[str]()
REPEATED_NAMES = ["price", "price"]


def test_conversion_keeps_its_settings() -> None:
	"""
	Check that the columns and the type are available as attributes.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(columns=COLUMN_NAMES, dtype=Type.TEXT)

	assert conversion.columns == EXPECTED_COLUMN_NAMES
	assert conversion.dtype == Type.TEXT


def test_conversion_keeps_its_own_copy_of_the_columns() -> None:
	"""
	Check that changing the given list afterwards leaves the conversion unchanged.

	.. versionadded:: 0.2.0
	"""
	column_names = list(COLUMN_NAMES)
	conversion = TableConversion(columns=column_names, dtype=Type.TEXT)

	column_names.append(ADDED_NAME)

	assert conversion.columns == EXPECTED_COLUMN_NAMES


def test_conversion_rejects_no_column() -> None:
	"""
	Check that an empty list of columns raises EmptyListError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(EmptyListError):
		TableConversion(columns=EMPTY_NAMES, dtype=Type.TEXT)


def test_conversion_rejects_a_repeated_column() -> None:
	"""
	Check that a column given twice raises DuplicateColumnError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(DuplicateColumnError):
		TableConversion(columns=REPEATED_NAMES, dtype=Type.TEXT)
