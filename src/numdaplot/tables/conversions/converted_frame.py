"""
Conversion of columns of a Table to another type.

.. versionadded:: 0.2.0
"""

from functools import partial

import pandas

from numdaplot.conversions.converted_column import convert_column
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.tables.columns.replaced_columns import replace_frame_columns


def convert_frame_columns(frame: pandas.DataFrame, conversion: TableConversion) -> pandas.DataFrame:
	"""
	Return the columns of a Table with some of them converted to another type, each at its place.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	conversion
		The names of the columns, their new type and the settings of the conversion.

	Returns
	-------
	pandas.DataFrame
		A new DataFrame, the other columns unchanged.

	Raises
	------
	ColumnNotFoundError
		When a column does not exist, before any column is converted.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.conversions.converted_frame import convert_frame_columns
	>>> frame = pandas.DataFrame({"low": [1.0, 2.0], "high": [3.0, 4.0]}, dtype="float64")
	>>> small_integers = ndp.TableConversion(columns=["low", "high"], dtype=ndp.Type.INT8)
	>>> converted_frame = convert_frame_columns(frame, small_integers)
	>>> converted_frame.dtypes.tolist()
	[Int8Dtype(), Int8Dtype()]
	"""
	column_conversion = partial(convert_column, conversion=conversion)
	converted_frame = replace_frame_columns(frame, conversion.columns, column_conversion)

	return converted_frame
