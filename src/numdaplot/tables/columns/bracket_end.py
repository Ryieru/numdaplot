"""
Whether the first or the last bracket of Brackets has a limit.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class BracketEnd(Enum):
	"""
	Whether the first or the last bracket of ``Brackets`` stops at a limit or holds every value beyond it.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Table.from_arrays({"age": ndp.Array.from_list([4, 30, 92])})
	>>> brackets = ndp.Brackets(limits=[0, 18, 65], last=ndp.BracketEnd.OPEN)
	>>> ages.convert(ndp.Conversion(column="age", dtype=ndp.Type.CATEGORY, format=brackets)).column("age").to_list()
	['0 to 17', '18 to 64', '65 or more']
	"""

	CLOSED = auto()
	"""
	The bracket stops at its limit. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Table.from_arrays({"age": ndp.Array.from_list([4, 30])})
	>>> brackets = ndp.Brackets(limits=[0, 18, 65], last=ndp.BracketEnd.CLOSED)
	>>> ages.convert(ndp.Conversion(column="age", dtype=ndp.Type.CATEGORY, format=brackets)).column("age").to_list()
	['0 to 17', '18 to 64']
	"""

	OPEN = auto()
	"""
	The bracket holds every value beyond the limit: below the first one, or above the last one.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> temperatures = ndp.Table.from_arrays({"celsius": ndp.Array.from_list([-3.5, 12.0])})
	>>> brackets = ndp.Brackets(limits=[0, 15], first=ndp.BracketEnd.OPEN)
	>>> conversion = ndp.Conversion(column="celsius", dtype=ndp.Type.CATEGORY, format=brackets)
	>>> temperatures.convert(conversion).column("celsius").to_list()
	['under 0', '0 to under 15']
	"""
