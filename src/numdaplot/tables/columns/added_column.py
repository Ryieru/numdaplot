"""
Addition of a column to a Table.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.frames.column_values import build_column

ADD_COLUMN_OPERATION = "add_column"
ONE_DIMENSION = 1


def add_frame_column(frame: pandas.DataFrame, new_column: NewColumn) -> pandas.DataFrame:
	"""
	Return the columns of a Table with one more column, or with a column replaced.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table, which are not changed.
	new_column
		The name, the values and what to do when the name exists.

	Returns
	-------
	pandas.DataFrame
		A new column is placed last; a replaced column keeps its place. A Table without column
		takes as many rows as the new column has values.

	Raises
	------
	DimensionError
		When the Array of values does not have one dimension.
	ShapeMismatchError
		When the Array does not have one value per row of the Table.
	DuplicateColumnError
		When the name exists and ``on_conflict`` is ``ERROR``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.added_column import add_frame_column
	>>> frame = pandas.DataFrame({"price": [1.5, 8.0]})
	>>> add_frame_column(frame, ndp.NewColumn(name="count", values=ndp.Array.from_list([2, 1])))
	price  count
	0    1.5      2
	1    8.0      1
	"""
	values = new_column.values.to_numpy()
	if values.ndim != ONE_DIMENSION:
		raise DimensionError(ADD_COLUMN_OPERATION, values.ndim)

	column_names = [str(column_name) for column_name in frame.columns]
	value_count = values.size
	row_count = len(frame)
	has_columns = column_names != []
	has_wrong_length = has_columns and value_count != row_count
	if has_wrong_length:
		raise ShapeMismatchError((value_count,), (row_count,))

	name_exists = new_column.name in column_names
	refuses_existing_name = name_exists and new_column.on_conflict == Conflict.ERROR
	if refuses_existing_name:
		raise DuplicateColumnError(new_column.name)

	column = build_column(values)
	extended_frame = frame.copy(deep=False)
	if not has_columns:
		row_numbers = pandas.RangeIndex(value_count)
		extended_frame = pandas.DataFrame(index=row_numbers)

	extended_frame[new_column.name] = column

	return extended_frame
