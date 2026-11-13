"""
What to do when a file or a column already exists.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Conflict(Enum):
	"""
	What to do when a file to write or a column to add already exists.

	Used by the ``to_*`` methods of a Table and by ``NewColumn``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> taxed_prices = sales.column("price") * 1.2
	>>> sales.add_column(ndp.NewColumn(name="price", values=taxed_prices, on_conflict=ndp.Conflict.REPLACE))
	    city   price
	    TEXT FLOAT64
	0  Paris   144.0
	1   Lyon    96.0
	2  Paris   180.0
	"""

	ERROR = auto()
	"""
	Raise an error and change nothing. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> taxed_prices = sales.column("price") * 1.2
	>>> try:
	... 	sales.add_column(ndp.NewColumn(name="price", values=taxed_prices, on_conflict=ndp.Conflict.ERROR))
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'price' appears more than once.
	"""

	REPLACE = auto()
	"""
	Replace the existing file or column.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> taxed_prices = sales.column("price") * 1.2
	>>> sales.add_column(ndp.NewColumn(name="price", values=taxed_prices, on_conflict=ndp.Conflict.REPLACE))
	    city   price
	    TEXT FLOAT64
	0  Paris   144.0
	1   Lyon    96.0
	2  Paris   180.0
	"""
