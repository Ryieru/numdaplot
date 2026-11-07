"""
Unit tests of ValueChange.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.mapping.value_change import ValueChange
from numdaplot.errors.invalid_type_error import InvalidTypeError

OLD_CODE = -1
NEW_LABEL = "Femme"


def test_value_change_keeps_its_values() -> None:
	"""
	Check that the old and the new values are available as attributes.

	.. versionadded:: 0.1.0
	"""
	change = ValueChange(OLD_CODE, NEW_LABEL)

	assert change.old_value == OLD_CODE
	assert change.new_value == NEW_LABEL


def test_value_change_accepts_none_as_new_value() -> None:
	"""
	Check that None makes the old value missing.

	.. versionadded:: 0.1.0
	"""
	change = ValueChange(OLD_CODE, None)

	assert change.new_value is None


def test_value_change_rejects_none_as_old_value() -> None:
	"""
	Check that a missing value cannot be replaced.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidTypeError):
		ValueChange(None, NEW_LABEL)  # pyright: ignore[reportArgumentType]
