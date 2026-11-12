"""
Which rows a join of two Tables keeps.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class JoinMode(Enum):
	"""
	Which rows a join keeps, used by ``Join``: the rows of both Tables whose keys match, and the rows left alone.

	A row whose keys match several rows of the other Table appears once per match. A missing key never matches.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2]), "dep": ndp.Array.from_list(["75", "69"])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 3]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], mode=ndp.JoinMode.OUTER))
	     id  dep   age
	  INT64 TEXT INT64
	0     1   75    34
	1     2   69  <NA>
	2     3 <NA>    51
	"""

	INNER = auto()
	"""
	Only the rows whose keys match a row of the other Table. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2]), "dep": ndp.Array.from_list(["75", "69"])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 3]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], mode=ndp.JoinMode.INNER))
	     id dep   age
	  INT64 TEXT INT64
	0     1  75    34
	"""

	LEFT = auto()
	"""
	Every row of the joined Table, with missing values where the other Table has no match.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2]), "dep": ndp.Array.from_list(["75", "69"])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 3]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], mode=ndp.JoinMode.LEFT))
	     id  dep   age
	  INT64 TEXT INT64
	0     1   75    34
	1     2   69  <NA>
	"""

	RIGHT = auto()
	"""
	Every row of the other Table, with missing values where the joined Table has no match.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2]), "dep": ndp.Array.from_list(["75", "69"])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 3]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], mode=ndp.JoinMode.RIGHT))
	     id  dep   age
	  INT64 TEXT INT64
	0     1   75    34
	1     3 <NA>    51
	"""

	OUTER = auto()
	"""
	Every row of both Tables, with missing values where one has no match.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2]), "dep": ndp.Array.from_list(["75", "69"])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 3]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], mode=ndp.JoinMode.OUTER))
	     id  dep   age
	  INT64 TEXT INT64
	0     1   75    34
	1     2   69  <NA>
	2     3 <NA>    51
	"""
