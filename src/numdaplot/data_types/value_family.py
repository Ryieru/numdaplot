"""
Families of types whose values can be compared and combined together.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto

from numdaplot.data_types.type import Type


class ValueFamily(Enum):
	"""
	Family of types whose values can be compared and combined together.

	An ``INT64`` and a ``FLOAT64`` are both numbers, while a number and a text cannot be compared.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.UINT8) == find_family(ndp.Type.FLOAT64)
	True
	>>> find_family(ndp.Type.CATEGORY)
	<ValueFamily.TEXT: 3>
	"""

	NUMBER = auto()
	"""
	Signed and unsigned integers, and decimals.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.UINT8)
	<ValueFamily.NUMBER: 1>
	"""

	BOOL = auto()
	"""
	True or false.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.BOOL)
	<ValueFamily.BOOL: 2>
	"""

	TEXT = auto()
	"""
	Texts and categories.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.TEXT)
	<ValueFamily.TEXT: 3>
	"""

	MOMENT = auto()
	"""
	Dates and datetimes.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.DATE)
	<ValueFamily.MOMENT: 4>
	"""

	DURATION = auto()
	"""
	Gaps between two moments.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.DURATION)
	<ValueFamily.DURATION: 5>
	"""

	TIME = auto()
	"""
	Times of day, compared only with each other.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.TIME)
	<ValueFamily.TIME: 6>
	"""


FAMILIES_BY_TYPE = {
	Type.INT8: ValueFamily.NUMBER,
	Type.INT16: ValueFamily.NUMBER,
	Type.INT32: ValueFamily.NUMBER,
	Type.INT64: ValueFamily.NUMBER,
	Type.UINT8: ValueFamily.NUMBER,
	Type.UINT16: ValueFamily.NUMBER,
	Type.UINT32: ValueFamily.NUMBER,
	Type.UINT64: ValueFamily.NUMBER,
	Type.FLOAT32: ValueFamily.NUMBER,
	Type.FLOAT64: ValueFamily.NUMBER,
	Type.BOOL: ValueFamily.BOOL,
	Type.TEXT: ValueFamily.TEXT,
	Type.CATEGORY: ValueFamily.TEXT,
	Type.DATE: ValueFamily.MOMENT,
	Type.DATETIME: ValueFamily.MOMENT,
	Type.DURATION: ValueFamily.DURATION,
	Type.TIME: ValueFamily.TIME,
}


def find_family(data_type: Type) -> ValueFamily:
	"""
	Return the family of a numdaplot type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		The type to classify.

	Returns
	-------
	ValueFamily
		The family whose values can be compared with values of this type.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_family import find_family
	>>> find_family(ndp.Type.DATETIME)
	<ValueFamily.MOMENT: 4>
	"""
	family = FAMILIES_BY_TYPE[data_type]

	return family
