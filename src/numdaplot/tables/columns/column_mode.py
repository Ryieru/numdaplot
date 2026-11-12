"""
Whether a ColumnChoice keeps or drops its columns.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ColumnMode(Enum):
	"""
	Whether a ``ColumnChoice`` keeps or drops the columns it names.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.choose_columns(ndp.ColumnChoice(columns=["price"], mode=ndp.ColumnMode.DROP))
	    city
	    TEXT
	0  Paris
	1   Lyon
	2  Paris
	"""

	KEEP = auto()
	"""
	Only the named columns remain, in the order of the list. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.choose_columns(ndp.ColumnChoice(columns=["price"], mode=ndp.ColumnMode.KEEP))
	    price
	  FLOAT64
	0   120.0
	1    80.0
	2   150.0
	"""

	DROP = auto()
	"""
	The named columns are removed, the others keep their order.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.choose_columns(ndp.ColumnChoice(columns=["price"], mode=ndp.ColumnMode.DROP))
	    city
	    TEXT
	0  Paris
	1   Lyon
	2  Paris
	"""
