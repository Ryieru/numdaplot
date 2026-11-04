"""
Text of a Table, with the type of each column under its name.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.time_zones import name_column_type


def build_typed_frame(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return a copy of the columns of a Table whose header shows the name, then the type, of each column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	pandas.DataFrame
		A copy with a two-level header: the column names, then the names of their ``ndp.Type``, followed by
		the time zone of a datetime column that has one.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.table_text import build_typed_frame
	>>> build_typed_frame(pandas.DataFrame({"price": [1.5]})).columns.tolist()
	[('price', 'FLOAT64')]
	"""
	column_names = list(frame.columns)
	type_names = list[str]()

	for column_name in column_names:
		column = frame[column_name]
		column_type = find_column_type(column)
		type_name = name_column_type(column, column_type)
		type_names.append(type_name)

	header = pandas.MultiIndex.from_arrays([column_names, type_names])
	typed_frame = frame.copy()
	typed_frame.columns = header

	return typed_frame


def format_table(frame: pandas.DataFrame) -> str:
	"""
	Return the text pandas shows for the columns of a Table, with the type of each column under its name.

	A long Table only shows its first and last rows, following the pandas display settings.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	str
		The text of the Table, with row numbers on the left.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.table_text import format_table
	>>> print(format_table(pandas.DataFrame({"price": [1.5, 8.0]})))
	    price
	  FLOAT64
	0     1.5
	1     8.0
	"""
	typed_frame = build_typed_frame(frame)
	table_text = repr(typed_frame)

	return table_text
