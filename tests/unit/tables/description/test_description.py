"""
Unit tests of Description.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.description.description import Description

COLUMN_NAMES = ["price"]
REPEATED_NAMES = ["price", "price"]
EMPTY_NAMES = list[str]()
EMPTY_FUNCTIONS = list[Statistic]()


def test_description_uses_the_default_functions_and_number_columns() -> None:
	"""
	Check that functions and columns are omitted by default.

	.. versionadded:: 0.1.0
	"""
	description = Description()

	assert description.functions is None
	assert description.columns is None


def test_description_keeps_its_own_copy_of_the_lists() -> None:
	"""
	Check that changing the given lists does not change the description.

	.. versionadded:: 0.1.0
	"""
	functions = list[Statistic]([Min(), Max()])
	column_names = list(COLUMN_NAMES)
	description = Description(functions=functions, columns=column_names)

	functions.clear()
	column_names.clear()

	assert description.functions == [Min(), Max()]
	assert description.columns == COLUMN_NAMES


@pytest.mark.parametrize(
	("functions", "columns"),
	[
		(EMPTY_FUNCTIONS, None),
		(None, EMPTY_NAMES),
	],
)
def test_description_rejects_empty_lists(functions: list[Statistic] | None, columns: list[str] | None) -> None:
	"""
	Check that an empty list of functions or columns raises EmptyListError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	functions
		The statistics.
	columns
		The described columns.
	"""
	with pytest.raises(EmptyListError):
		Description(functions=functions, columns=columns)


def test_description_rejects_a_repeated_column() -> None:
	"""
	Check that a repeated column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		Description(columns=REPEATED_NAMES)
