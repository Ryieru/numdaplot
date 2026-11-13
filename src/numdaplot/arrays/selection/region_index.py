"""
Numpy index of the positions of a Region inside an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.creation.range_values import compute_range_values
from numdaplot.errors.positions.dimension_error import DimensionError
from numdaplot.errors.positions.invalid_position_error import InvalidPositionError
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.positions.first import First
from numdaplot.positions.index import Index
from numdaplot.positions.last import Last
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region

ONE_DIMENSION = 1
TWO_DIMENSIONS = 2
WHOLE_NUMBER_KINDS = frozenset({"i", "u"})
REGION_OPERATION = "A Region"
COLUMNS_OPERATION = "A Region with columns"
COLUMN_NAMES_OPERATION = "Column names in a Region for an Array"
COLUMN_NAMES_ALTERNATIVE = "Index, Range, First or Last positions"


def build_region_index(region: Region, dimensions: tuple[int, ...]) -> tuple[NDArray[Any], ...]:
	"""
	Return the numpy index selecting the positions of a Region.

	Rows and columns given as an ``Index`` keep their dimension, so the selection of one row
	of a two-dimensional Array is still two-dimensional.

	.. versionadded:: 0.1.0

	Parameters
	----------
	region
		The rows and the columns to select.
	dimensions
		The dimensions of the Array.

	Returns
	-------
	tuple[NDArray, ...]
		One array of positions per dimension, usable inside numpy brackets.

	Raises
	------
	DimensionError
		When the Array has more than two dimensions, or when columns are given for a
		one-dimensional Array.
	RefusedOperationError
		When columns are given as names, which only a Table has.
	InvalidPositionError
		When a position is not a whole number inside its dimension.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.region_index import build_region_index
	>>> build_region_index(ndp.Region(rows=ndp.Index(-1)), (3,))
	(array([-1]),)
	"""
	dimension_count = len(dimensions)
	if dimension_count > TWO_DIMENSIONS:
		raise DimensionError(REGION_OPERATION, dimension_count)

	if isinstance(region.columns, list):
		raise RefusedOperationError(COLUMN_NAMES_OPERATION, COLUMN_NAMES_ALTERNATIVE)

	row_count = dimensions[0]
	row_positions = find_positions(region.rows, row_count)
	if dimension_count == ONE_DIMENSION:
		if region.columns is not None:
			raise DimensionError(COLUMNS_OPERATION, dimension_count)

		return (row_positions,)

	column_count = dimensions[1]
	column_positions = find_positions(region.columns, column_count)
	region_index = numpy.ix_(row_positions, column_positions)

	return region_index


def find_positions(selector: Index | Range | First | Last | None, size: int) -> NDArray[Any]:
	"""
	Return the positions chosen in one dimension.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts ``First`` and ``Last``, which give every position of a dimension shorter than their count.

	Parameters
	----------
	selector
		One position, a sequence of positions, the first or the last positions, or ``None`` for every position.
	size
		The size of the dimension.

	Returns
	-------
	NDArray
		The chosen positions, negative ones counting from the end.

	Raises
	------
	InvalidPositionError
		When a position is not a whole number inside the dimension.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.region_index import find_positions
	>>> find_positions(ndp.Range(start=0, stop=4, step=2), 5)
	array([0, 2, 4])
	>>> find_positions(ndp.Last(2), 5)
	array([3, 4])
	"""
	match selector:
		case None:
			positions = numpy.arange(size)
		case Index():
			positions = numpy.array([selector.position])
		case Range():
			positions = compute_range_values(selector)
		case First():
			first_count = min(selector.count, size)
			positions = numpy.arange(first_count)
		case Last():
			last_count = min(selector.count, size)
			first_position = size - last_count
			positions = numpy.arange(first_position, size)

	require_valid_positions(positions, size)

	return positions


def require_valid_positions(positions: NDArray[Any], size: int) -> None:
	"""
	Check that positions are whole numbers inside a dimension.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The positions to check.
	size
		The size of the dimension, which accepts the positions from ``-size`` to ``size - 1``.

	Raises
	------
	InvalidPositionError
		At the first position that is not a whole number or falls outside the dimension.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.region_index import require_valid_positions
	>>> try:
	... 	require_valid_positions(numpy.array([0, 3]), 3)
	... except ndp.InvalidPositionError as error:
	... 	print(error)
	Expected a whole position between -3 and 2, got 3.
	"""
	if positions.size == 0:
		return

	if positions.dtype.kind not in WHOLE_NUMBER_KINDS:
		first_position = positions[0]
		rejected_position = first_position.item()
		raise InvalidPositionError(rejected_position, size)

	lowest_position = -size
	below_lowest = positions < lowest_position
	above_highest = positions >= size
	outside = below_lowest | above_highest
	has_outside_position = outside.any()
	if has_outside_position:
		outside_positions = positions[outside]
		first_outside_position = outside_positions[0]
		rejected_position = first_outside_position.item()
		raise InvalidPositionError(rejected_position, size)
