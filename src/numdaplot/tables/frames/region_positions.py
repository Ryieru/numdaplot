"""
Rows and columns of a Table chosen by a Region.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.arrays.selection.region_index import find_positions
from numdaplot.positions.index import Index
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region
from numdaplot.tables.columns.column_names import require_known_columns, require_unique_names

POSITION_DTYPE = numpy.int64


def take_region(frame: pandas.DataFrame, region: Region) -> pandas.DataFrame:
	"""
	Return the rows and the columns of a Table chosen by a Region.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	region
		The rows and the columns to take, every one of a dimension when omitted.

	Returns
	-------
	pandas.DataFrame
		The chosen part, rows numbered from 0, columns in the order of the region.

	Raises
	------
	InvalidPositionError
		When a position is not a whole number inside its dimension.
	ColumnNotFoundError
		When a column name matches no column.
	DuplicateColumnError
		When a column name appears twice in the region.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.region_positions import take_region
	>>> frame = pandas.DataFrame({"city": ["Paris", "Lyon"], "price": [1.5, 8.0]})
	>>> take_region(frame, ndp.Region(rows=ndp.Index(-1), columns=["price"]))
	   price
	0    8.0
	"""
	row_count = len(frame)
	row_positions = find_positions(region.rows, row_count)
	column_names = [str(column_name) for column_name in frame.columns]
	column_positions = find_column_positions(region.columns, column_names)
	region_frame = frame.iloc[row_positions, column_positions]
	numbered_frame = region_frame.reset_index(drop=True)

	return numbered_frame


def find_column_positions(columns: Index | Range | list[str] | None, column_names: list[str]) -> NDArray[Any]:
	"""
	Return the positions of the columns chosen by a Region.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		One position, a sequence of positions, a list of names, or ``None`` for every column.
	column_names
		The names of the columns of the Table.

	Returns
	-------
	NDArray
		The chosen positions, in the order of the region.

	Raises
	------
	InvalidPositionError
		When a position is not a whole number inside the columns.
	ColumnNotFoundError
		When a name matches no column.
	DuplicateColumnError
		When a name appears twice.

	Examples
	--------
	>>> from numdaplot.tables.frames.region_positions import find_column_positions
	>>> find_column_positions(["price", "city"], ["city", "price"])
	array([1, 0])
	"""
	if not isinstance(columns, list):
		column_count = len(column_names)
		positions = find_positions(columns, column_count)
		return positions

	require_unique_names(columns)
	require_known_columns(columns, column_names)
	positions_by_name = {column_name: position for position, column_name in enumerate(column_names)}
	named_positions = [positions_by_name[column_name] for column_name in columns]
	positions = numpy.array(named_positions, dtype=POSITION_DTYPE)

	return positions
