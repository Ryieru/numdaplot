"""
How many times each key may appear in the Tables of a join.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Relation(Enum):
	"""
	How many times each key may appear in the two Tables of a join, checked by ``Join`` before joining.

	The first word is for the left Table, the one joined, the second for the right Table, the other one. With
	several keys, their combination is checked. Rows with a missing key are not checked, as they never match.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 102])})
	>>> users = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 101, 102])})
	>>> accidents.join(ndp.Join(other=users, keys=["Num_Acc"], relation=ndp.Relation.ONE_TO_MANY)).row_count
	3
	"""

	MANY_TO_MANY = auto()
	"""
	Nothing is checked: each key may appear several times on both sides. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 101])})
	>>> users = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 101])})
	>>> accidents.join(ndp.Join(other=users, keys=["Num_Acc"], relation=ndp.Relation.MANY_TO_MANY)).row_count
	4
	"""

	ONE_TO_ONE = auto()
	"""
	Each key appears at most once in each Table.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 102])})
	>>> places = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 102])})
	>>> accidents.join(ndp.Join(other=places, keys=["Num_Acc"], relation=ndp.Relation.ONE_TO_ONE)).row_count
	2
	"""

	ONE_TO_MANY = auto()
	"""
	Each key appears at most once in the left Table, and any number of times in the right Table.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 102])})
	>>> users = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 101, 102])})
	>>> accidents.join(ndp.Join(other=users, keys=["Num_Acc"], relation=ndp.Relation.ONE_TO_MANY)).row_count
	3
	"""

	MANY_TO_ONE = auto()
	"""
	Each key appears any number of times in the left Table, and at most once in the right Table.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> users = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 101, 102])})
	>>> accidents = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 102])})
	>>> users.join(ndp.Join(other=accidents, keys=["Num_Acc"], relation=ndp.Relation.MANY_TO_ONE)).row_count
	3
	"""
