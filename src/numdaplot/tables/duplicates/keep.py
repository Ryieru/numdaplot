"""
Which row of a group of duplicated rows is kept.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Keep(Enum):
	"""
	Which row of a group of duplicated rows is kept, used by ``Deduplication``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"], keep=ndp.Keep.LAST))
	    city   price
	    TEXT FLOAT64
	0   Lyon    80.0
	1  Paris   150.0
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"], keep=ndp.Keep.NONE))
	   city   price
	   TEXT FLOAT64
	0  Lyon    80.0
	"""

	FIRST = auto()
	"""
	The first row of each group is kept. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"], keep=ndp.Keep.FIRST))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	LAST = auto()
	"""
	The last row of each group is kept.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"], keep=ndp.Keep.LAST))
	    city   price
	    TEXT FLOAT64
	0   Lyon    80.0
	1  Paris   150.0
	"""

	NONE = auto()
	"""
	No row of a duplicated group is kept, only rows that appear once remain.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"], keep=ndp.Keep.NONE))
	   city   price
	   TEXT FLOAT64
	0  Lyon    80.0
	"""
