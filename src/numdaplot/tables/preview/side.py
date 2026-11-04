"""
Which rows of a Table a preview shows.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Side(Enum):
	"""
	Which rows of a Table a ``Preview`` shows.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(count=1, side=ndp.Side.END))
	    city   price
	    TEXT FLOAT64
	2  Paris   150.0
	>>> sales.preview(ndp.Preview(count=2, side=ndp.Side.RANDOM, seed=42))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	2  Paris   150.0
	"""

	START = auto()
	"""
	The first rows. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(count=2, side=ndp.Side.START))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	END = auto()
	"""
	The last rows.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(count=2, side=ndp.Side.END))
	    city   price
	    TEXT FLOAT64
	1   Lyon    80.0
	2  Paris   150.0
	"""

	RANDOM = auto()
	"""
	Rows drawn at random, shown in the order of the Table.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(count=2, side=ndp.Side.RANDOM, seed=42))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	2  Paris   150.0
	"""
