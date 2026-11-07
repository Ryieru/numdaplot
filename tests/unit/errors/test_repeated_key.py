"""
Unit tests of RepeatedKey.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.repeated_key import RepeatedKey

KEY_NAMES = ["Num_Acc", "id_vehicule"]
KEY_VALUES = [202500000001, "A01"]
COUNT = 3


def test_repeated_key_keeps_the_names_the_values_and_the_count() -> None:
	"""
	Check the fields of a repeated key.

	.. versionadded:: 0.1.0
	"""
	repeated_key = RepeatedKey(KEY_NAMES, KEY_VALUES, COUNT)

	assert repeated_key.key_names == KEY_NAMES
	assert repeated_key.key_values == KEY_VALUES
	assert repeated_key.count == COUNT
