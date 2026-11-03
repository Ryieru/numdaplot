"""
Unit tests of ArraySorting.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array_sorting import ArraySorting
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.positions.axis import Axis


def test_array_sorting_sorts_ascending_each_row_with_missing_values_last_by_default() -> None:
	"""
	Check the default order, axis and place of missing values.

	.. versionadded:: 0.1.0
	"""
	sorting = ArraySorting()

	assert sorting.order == Order.ASCENDING
	assert sorting.axis is None
	assert sorting.missing == MissingPosition.LAST


def test_array_sorting_keeps_its_settings() -> None:
	"""
	Check that given settings are available as attributes.

	.. versionadded:: 0.1.0
	"""
	sorting = ArraySorting(order=Order.DESCENDING, axis=Axis.EACH_COLUMN, missing=MissingPosition.FIRST)

	assert sorting.order == Order.DESCENDING
	assert sorting.axis == Axis.EACH_COLUMN
	assert sorting.missing == MissingPosition.FIRST
