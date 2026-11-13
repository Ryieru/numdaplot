"""
Unit tests of Replacement.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.arrays.selection.replacement import Replacement
from numdaplot.positions.index import Index
from numdaplot.positions.region import Region

FIRST_ROW = Region(rows=Index(0))
NEW_VALUE = 0
NEW_VALUES = [7, 8]


def test_replacement_keeps_a_single_value() -> None:
	"""
	Check that the region and a single value are available as attributes.

	.. versionadded:: 0.1.0
	"""
	replacement = Replacement(region=FIRST_ROW, value=NEW_VALUE)

	assert replacement.region == FIRST_ROW
	assert replacement.value == NEW_VALUE


def test_replacement_keeps_an_array_of_values() -> None:
	"""
	Check that an Array of new values is kept as given.

	.. versionadded:: 0.1.0
	"""
	new_values = Array.from_list(NEW_VALUES)

	replacement = Replacement(region=FIRST_ROW, value=new_values)

	assert replacement.value is new_values
