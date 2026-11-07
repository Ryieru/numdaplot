"""
How close the types of the keys of a join must be.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class KeyTypes(Enum):
	"""
	How close the types of the two columns of each key of a join must be, used by ``Join``.

	A ``DATE`` key never matches a ``DATETIME`` key, and datetimes must have the same time zone on both sides.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1.0, 2.0]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], key_types=ndp.KeyTypes.SAME_FAMILY)).column_types
	{'id': <Type.FLOAT64: 10>, 'age': <Type.INT64: 4>}
	"""

	SAME_FAMILY = auto()
	"""
	Both columns hold numbers, texts, booleans, dates, datetimes, durations or times of day. Default value.

	The key of the result takes the type holding both: ``INT64`` and ``FLOAT64`` give ``FLOAT64``, ``TEXT`` and
	``CATEGORY`` give ``TEXT``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1.0, 2.0]), "age": ndp.Array.from_list([34, 51])})
	>>> accidents.join(ndp.Join(other=users, keys=["id"], key_types=ndp.KeyTypes.SAME_FAMILY)).column_types
	{'id': <Type.FLOAT64: 10>, 'age': <Type.INT64: 4>}
	"""

	SAME_TYPE = auto()
	"""
	Both columns have the same type: ``INT64`` and ``FLOAT64`` are refused.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 2])})
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1.0, 2.0])})
	>>> try:
	... 	accidents.join(ndp.Join(other=users, keys=["id"], key_types=ndp.KeyTypes.SAME_TYPE))
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply Join to the INT64 column 'id' and FLOAT64.
	"""
