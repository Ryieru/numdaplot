"""
Unit tests of the groups of number types.

.. versionadded:: 0.2.0
"""

from numdaplot.data_types.number_types import DECIMAL_TYPES, INTEGER_TYPES
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family


def test_number_types_hold_every_number_type_once() -> None:
	"""
	Check that every type of the number family is either an integer type or a decimal type, never both.

	.. versionadded:: 0.2.0
	"""
	number_types = {data_type for data_type in Type if find_family(data_type) == ValueFamily.NUMBER}
	shared_types = INTEGER_TYPES & DECIMAL_TYPES
	grouped_types = INTEGER_TYPES | DECIMAL_TYPES

	assert grouped_types == number_types
	assert shared_types == frozenset()
