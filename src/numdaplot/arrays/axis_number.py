"""
Conversion of an ``ndp.Axis`` to a numpy axis number.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.dimension_error import DimensionError
from numdaplot.positions.axis import Axis

AXIS_DIMENSION_COUNT = 2
AXIS_OPERATION = "An axis"
NUMPY_AXES = {
	Axis.EACH_ROW: 1,
	Axis.EACH_COLUMN: 0,
}


def find_numpy_axis(axis: Axis | None, dimension_count: int) -> int | None:
	"""
	Return the numpy axis number an operation runs along.

	``EACH_ROW`` handles every row on its own, so the numpy operation runs along the columns, axis 1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The numdaplot axis, or ``None`` when omitted.
	dimension_count
		The number of dimensions of the Array.

	Returns
	-------
	int or None
		1 for ``EACH_ROW``, 0 for ``EACH_COLUMN``, ``None`` when the axis is omitted.

	Raises
	------
	DimensionError
		When an axis is given for an Array that is not two-dimensional.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.axis_number import find_numpy_axis
	>>> find_numpy_axis(ndp.Axis.EACH_COLUMN, 2)
	0
	"""
	if axis is None:
		return None

	if dimension_count != AXIS_DIMENSION_COUNT:
		raise DimensionError(AXIS_OPERATION, dimension_count)

	numpy_axis = NUMPY_AXES[axis]

	return numpy_axis
