"""
Settings of the sort of an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.settings.field_types import require_field_types


@dataclass(frozen=True)
class ArraySorting:
	"""
	Settings of the sort of an Array, used by ``Array.sort``.

	The axis, inside each row or each column, is given to ``Array.sort`` itself.

	.. versionadded:: 0.1.0

	Parameters
	----------
	order
		Ascending by default.
	missing
		Place of the missing values, last by default whatever the order.


	Raises
	------
	InvalidSettingTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> grid = ndp.Array.from_list([[3, 1], [2, 4]])
	>>> grid.sort(ndp.ArraySorting(order=ndp.Order.DESCENDING), axis=ndp.Axis.EACH_COLUMN)
	Array([[3, 4],
	       [2, 1]], dtype=INT64)
	"""

	order: Order = Order.ASCENDING
	missing: MissingPosition = MissingPosition.LAST

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
