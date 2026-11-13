"""
Unit tests of ValueMapping.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.mapping.value_change import ValueChange
from numdaplot.arrays.mapping.value_mapping import ValueMapping, find_new_type, require_unique_values
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.errors.settings.duplicate_value_error import DuplicateValueError
from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.rule_values import ScalarValue
from numdaplot.types.type import Type

LABEL_CHANGES = [ValueChange(1, "Homme"), ValueChange(2, "Femme")]
NO_CHANGE = list[ValueChange]()
MIXED_OLD_VALUES = [ValueChange(1, "Homme"), ValueChange("2", "Femme")]
MIXED_NEW_VALUES = [ValueChange(1, "Homme"), ValueChange(2, 2)]
REPEATED_OLD_VALUES = [ValueChange(2, "Femme"), ValueChange(2.0, "F")]
NUMBER_CHANGES = [ValueChange(1, 10), ValueChange(2, 2.5), ValueChange(-1, None)]
MISSING_ONLY_CHANGES = [ValueChange(-1, None)]
UNIQUE_VALUES = list[ScalarValue]([1, 2, 3])


def test_value_mapping_raises_for_unmatched_values_by_default() -> None:
	"""
	Check the default of others.

	.. versionadded:: 0.1.0
	"""
	mapping = ValueMapping(changes=LABEL_CHANGES)

	assert mapping.others == Unmatched.ERROR


def test_value_mapping_keeps_its_own_copy_of_the_changes() -> None:
	"""
	Check that changing the given list afterwards does not change the mapping.

	.. versionadded:: 0.1.0
	"""
	changes = list(LABEL_CHANGES)
	mapping = ValueMapping(changes=changes)

	changes.clear()

	assert mapping.changes == LABEL_CHANGES


def test_value_mapping_rejects_an_empty_list() -> None:
	"""
	Check that a mapping needs at least one change.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		ValueMapping(changes=NO_CHANGE)


@pytest.mark.parametrize("changes", [MIXED_OLD_VALUES, MIXED_NEW_VALUES])
def test_value_mapping_rejects_values_of_several_families(changes: list[ValueChange]) -> None:
	"""
	Check that old values, or new values, mixing numbers and texts raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	changes
		Changes mixing two families among their old or new values.
	"""
	with pytest.raises(IncompatibleTypesError):
		ValueMapping(changes=changes)


def test_value_mapping_rejects_an_old_value_given_twice() -> None:
	"""
	Check that 2 and 2.0 are the same old value.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateValueError):
		ValueMapping(changes=REPEATED_OLD_VALUES)


def test_require_unique_values_accepts_distinct_values() -> None:
	"""
	Check that distinct values raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_unique_values(UNIQUE_VALUES)


def test_find_new_type_gives_decimals_for_integers_and_decimals() -> None:
	"""
	Check that 10 and 2.5 give FLOAT64, None being ignored.

	.. versionadded:: 0.1.0
	"""
	new_type = find_new_type(NUMBER_CHANGES)

	assert new_type == Type.FLOAT64


def test_find_new_type_gives_none_when_every_new_value_is_none() -> None:
	"""
	Check the case of a mapping that only makes values missing.

	.. versionadded:: 0.1.0
	"""
	new_type = find_new_type(MISSING_ONLY_CHANGES)

	assert new_type is None
