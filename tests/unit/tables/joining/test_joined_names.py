"""
Unit tests of the names of the columns of a join.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.tables.joining.joined_names import add_suffix, name_joined_columns

KEYS = ["dep"]
COLUMN_NAMES = ["dep", "deaths", "area"]
OTHER_NAMES = ["dep", "deaths"]
DISTINCT_OTHER_NAMES = ["dep", "population"]
YEARS = ndp.JoinSuffixes(left="_2024", right="_2025")
EXPECTED_NAMES = ["deaths_2024", "area"]
EXPECTED_OTHER_NAMES = ["deaths_2025"]
EXPECTED_DISTINCT_NAMES = (["deaths", "area"], ["population"])
TAKEN_NAMES = ["dep", "deaths", "deaths_2025"]
SHARED_NAMES = {"deaths"}
SUFFIX = "_2024"
KEPT_NAMES = ["deaths", "area"]


def test_name_joined_columns_keeps_names_both_tables_do_not_share() -> None:
	"""
	Check that columns of different names keep their names, the keys left out.

	.. versionadded:: 0.1.0
	"""
	names = name_joined_columns(COLUMN_NAMES, DISTINCT_OTHER_NAMES, KEYS, None)

	assert names == EXPECTED_DISTINCT_NAMES


def test_name_joined_columns_adds_the_suffixes_to_shared_names() -> None:
	"""
	Check that only the names both Tables have get a suffix.

	.. versionadded:: 0.1.0
	"""
	joined_names, other_joined_names = name_joined_columns(COLUMN_NAMES, OTHER_NAMES, KEYS, YEARS)

	assert joined_names == EXPECTED_NAMES
	assert other_joined_names == EXPECTED_OTHER_NAMES


def test_name_joined_columns_rejects_a_shared_name_without_suffixes() -> None:
	"""
	Check that a column both Tables have raises DuplicateColumnError without suffixes.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.DuplicateColumnError):
		name_joined_columns(COLUMN_NAMES, OTHER_NAMES, KEYS, None)


def test_name_joined_columns_rejects_a_suffixed_name_already_taken() -> None:
	"""
	Check that a suffixed name equal to another column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.DuplicateColumnError):
		name_joined_columns(TAKEN_NAMES, OTHER_NAMES, KEYS, YEARS)


def test_add_suffix_changes_only_the_shared_names() -> None:
	"""
	Check that the names not shared stay as they are.

	.. versionadded:: 0.1.0
	"""
	suffixed_names = add_suffix(KEPT_NAMES, SHARED_NAMES, SUFFIX)

	assert suffixed_names == EXPECTED_NAMES
