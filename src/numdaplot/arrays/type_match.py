"""
Whether a comparison of two Arrays also compares their types.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class TypeMatch(Enum):
	"""
	Whether a comparison of two Arrays also compares their types, used by ``Equality``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> integers = ndp.Array.from_list([1, 2])
	>>> decimals = ndp.Array.from_list([1.0, 2.0])
	>>> integers.is_equal(ndp.Equality(other=decimals, types=ndp.TypeMatch.IGNORED))
	True
	>>> integers.is_equal(ndp.Equality(other=decimals, types=ndp.TypeMatch.STRICT))
	False
	"""

	STRICT = auto()
	"""
	The types must be the same: ``[1, 2]`` as ``INT64`` differs from ``[1.0, 2.0]`` as ``FLOAT64``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> integers = ndp.Array.from_list([1, 2])
	>>> decimals = ndp.Array.from_list([1.0, 2.0])
	>>> integers.is_equal(ndp.Equality(other=decimals, types=ndp.TypeMatch.STRICT))
	False
	"""

	IGNORED = auto()
	"""
	Only the values are compared: ``[1, 2]`` equals ``[1.0, 2.0]``. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> integers = ndp.Array.from_list([1, 2])
	>>> decimals = ndp.Array.from_list([1.0, 2.0])
	>>> integers.is_equal(ndp.Equality(other=decimals, types=ndp.TypeMatch.IGNORED))
	True
	"""
