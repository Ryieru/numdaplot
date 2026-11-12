"""
Which columns of a Table a preview shows.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ShownColumns(Enum):
	"""
	Which columns of a Table ``Preview`` shows when they do not fit in the width of the terminal.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> prices = ndp.Array.from_list([120.0, 80.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(columns=ndp.ShownColumns.ALL))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	ALL = auto()
	"""
	Every column, the columns going on after a line break, ended by a backslash, when they do not fit. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> prices = ndp.Array.from_list([120.0, 80.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(columns=ndp.ShownColumns.ALL))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	COMPACT = auto()
	"""
	Only the first and last columns that fit, the others replaced by ``...``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> long_name = "a_very_long_column_name_{number}"
	>>> columns = {long_name.format(number=number): ndp.Array.from_list([number]) for number in range(6)}
	>>> wide_table = ndp.Table.from_arrays(columns)
	>>> wide_table.preview(ndp.Preview(columns=ndp.ShownColumns.COMPACT))
	  a_very_long_column_name_0  ... a_very_long_column_name_5
	                      INT64  ...                     INT64
	0                         0  ...                         5
	<BLANKLINE>
	[1 rows x 6 columns]
	"""
