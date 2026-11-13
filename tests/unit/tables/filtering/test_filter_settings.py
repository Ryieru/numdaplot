"""
Unit tests of Condition and Filter.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.rules.greater import Greater
from numdaplot.tables.filtering.column_match import ColumnMatch
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.filtering.filter_mode import FilterMode

RULE = Greater(10)
COLUMN_NAMES = ["low", "high"]
REPEATED_NAMES = ["low", "low"]
EMPTY_NAMES = list[str]()
CONDITION = Condition(rule=RULE)


def test_condition_applies_to_every_column_with_any_match_by_default() -> None:
	"""
	Check the default columns and mode.

	.. versionadded:: 0.1.0
	"""
	condition = Condition(rule=RULE)

	assert condition.columns is None
	assert condition.mode == ColumnMatch.ANY


def test_condition_keeps_its_own_copy_of_the_columns() -> None:
	"""
	Check that changing the given list does not change the condition.

	.. versionadded:: 0.1.0
	"""
	column_names = list(COLUMN_NAMES)
	condition = Condition(rule=RULE, columns=column_names)

	column_names.clear()

	assert condition.columns == COLUMN_NAMES


def test_condition_rejects_an_empty_list_of_columns() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Condition(rule=RULE, columns=EMPTY_NAMES)


def test_condition_rejects_a_repeated_column() -> None:
	"""
	Check that a repeated column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		Condition(rule=RULE, columns=REPEATED_NAMES)


def test_filter_requires_every_condition_by_default() -> None:
	"""
	Check the default mode.

	.. versionadded:: 0.1.0
	"""
	row_filter = Filter(conditions=[CONDITION])

	assert row_filter.mode == FilterMode.ALL


def test_filter_rejects_no_condition() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Filter(conditions=[])
