"""
How many missing values make a row or a column removed.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class MissingMode(Enum):
	"""
	How many missing values make a row or a column removed, used by ``MissingDrop``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices, "stock": stocks})
	>>> table.drop_missing(ndp.MissingDrop(columns=["price", "stock"], rule=ndp.MissingMode.ALL))
	    city   price   stock
	    TEXT FLOAT64 FLOAT64
	0  Paris   120.0     3.0
	1   Lyon     NaN     5.0
	"""

	ANY = auto()
	"""
	A single missing value is enough. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices, "stock": stocks})
	>>> table.drop_missing(ndp.MissingDrop(columns=["price", "stock"], rule=ndp.MissingMode.ANY))
	    city   price   stock
	    TEXT FLOAT64 FLOAT64
	0  Paris   120.0     3.0
	"""

	ALL = auto()
	"""
	Every value must be missing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices, "stock": stocks})
	>>> table.drop_missing(ndp.MissingDrop(columns=["price", "stock"], rule=ndp.MissingMode.ALL))
	    city   price   stock
	    TEXT FLOAT64 FLOAT64
	0  Paris   120.0     3.0
	1   Lyon     NaN     5.0
	"""
