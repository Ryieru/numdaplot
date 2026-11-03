"""
Columns of a Table built from Arrays.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas

from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import build_column

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array

FROM_ARRAYS_OPERATION = "from_arrays"
COLUMN_ITEM_NAME = "column"
ONE_DIMENSION = 1


def build_array_frame(columns: dict[str, Array]) -> pandas.DataFrame:
	"""
	Return the columns of a Table holding the values of one-dimensional Arrays.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		One Array per column, by column name, all of the same length.

	Returns
	-------
	pandas.DataFrame
		The columns in the order of the dictionary, rows numbered from 0.

	Raises
	------
	EmptyListError
		When there is no column.
	InvalidColumnNameError
		When a column name is not a non-empty text.
	DimensionError
		When an Array does not have one dimension.
	ShapeMismatchError
		When the Arrays do not have the same length.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.array_frame import build_array_frame
	>>> build_array_frame({"city": ndp.Array.from_list(["Pau"]), "price": ndp.Array.from_list([1.5])})
	city  price
	0  Pau    1.5
	"""
	if columns == {}:
		raise EmptyListError(COLUMN_ITEM_NAME)

	column_names = list(columns)
	require_column_names(column_names)
	built_columns = dict[str, Column]()
	value_counts = list[int]()

	for column_name, array in columns.items():
		values = array.to_numpy()
		if values.ndim != ONE_DIMENSION:
			raise DimensionError(FROM_ARRAYS_OPERATION, values.ndim)

		column = build_column(values)
		built_columns[column_name] = column
		value_counts.append(values.size)

	row_count = value_counts[0]

	for value_count in value_counts:
		if value_count != row_count:
			raise ShapeMismatchError((row_count,), (value_count,))

	row_numbers = pandas.RangeIndex(row_count)
	frame = pandas.DataFrame(built_columns, index=row_numbers)

	return frame
