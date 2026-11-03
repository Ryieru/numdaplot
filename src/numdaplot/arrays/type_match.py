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
	>>> ndp.TypeMatch.STRICT
	<TypeMatch.STRICT: 1>
	"""

	STRICT = auto()
	"""The types must be the same: ``[1, 2]`` as ``INT64`` differs from ``[1.0, 2.0]`` as ``FLOAT64``."""

	IGNORED = auto()
	"""Only the values are compared: ``[1, 2]`` equals ``[1.0, 2.0]``. Default value."""
