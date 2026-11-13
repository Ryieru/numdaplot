"""
Unit tests of Join.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.tables.invalid_column_name_error import InvalidColumnNameError
from numdaplot.tables.joining.join import Join

IDS = ndp.Array.from_list([1, 2])
USERS = ndp.Table.from_arrays({"id": IDS})
KEYS = ["id"]
EMPTY_KEYS = list[str]()
EMPTY_NAME_KEYS = [""]
REPEATED_KEYS = ["id", "id"]


def test_join_defaults_keep_matching_rows_of_keys_of_one_family() -> None:
	"""
	Check the defaults of a Join.

	.. versionadded:: 0.1.0
	"""
	join = Join(other=USERS, keys=KEYS)

	assert join.mode == ndp.JoinMode.INNER
	assert join.suffixes is None
	assert join.key_types == ndp.KeyTypes.SAME_FAMILY
	assert join.relation == ndp.Relation.MANY_TO_MANY


def test_join_keeps_its_own_copy_of_the_keys() -> None:
	"""
	Check that changing the given list afterwards does not change the join.

	.. versionadded:: 0.1.0
	"""
	given_keys = list(KEYS)
	join = Join(other=USERS, keys=given_keys)

	given_keys.append("age")

	assert join.keys == KEYS


def test_join_rejects_an_empty_list_of_keys() -> None:
	"""
	Check that a join without key raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Join(other=USERS, keys=EMPTY_KEYS)


def test_join_rejects_an_empty_key_name() -> None:
	"""
	Check that an empty key name raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		Join(other=USERS, keys=EMPTY_NAME_KEYS)


def test_join_rejects_a_repeated_key() -> None:
	"""
	Check that a key given twice raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		Join(other=USERS, keys=REPEATED_KEYS)
