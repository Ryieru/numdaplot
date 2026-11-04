"""
How the conditions of a Filter combine.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class FilterMode(Enum):
	"""
	How the conditions of a ``Filter`` combine to keep a row.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> expensive = ndp.Condition(rule=ndp.Greater(130), columns=["price"])
	>>> in_lyon = ndp.Condition(rule=ndp.Equal("Lyon"), columns=["city"])
	>>> sales.filter(ndp.Filter(conditions=[expensive, in_lyon], mode=ndp.FilterMode.ANY))
	    city   price
	    TEXT FLOAT64
	0   Lyon    80.0
	1  Paris   150.0
	"""

	ALL = auto()
	"""
	A row is kept when it satisfies every condition. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
	>>> in_lyon = ndp.Condition(rule=ndp.Equal("Lyon"), columns=["city"])
	>>> sales.filter(ndp.Filter(conditions=[expensive, in_lyon], mode=ndp.FilterMode.ALL))
	Empty DataFrame
	Columns: [(city, TEXT), (price, FLOAT64)]
	Index: []
	"""

	ANY = auto()
	"""
	A row is kept when it satisfies at least one condition.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
	>>> in_lyon = ndp.Condition(rule=ndp.Equal("Lyon"), columns=["city"])
	>>> sales.filter(ndp.Filter(conditions=[expensive, in_lyon], mode=ndp.FilterMode.ANY))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	2  Paris   150.0
	"""
