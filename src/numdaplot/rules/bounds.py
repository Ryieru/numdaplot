"""
Which bounds of an interval are part of it.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Bounds(Enum):
	"""
	Which bounds of an interval are part of it, used by ``Between`` and ``Range``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> scores = ndp.Array.from_list([0, 5, 10])
	>>> scores.select(ndp.Between(low=0, high=10, bounds=ndp.Bounds.LOW_ONLY))
	Array([0, 5], dtype=INT64)
	"""

	INCLUDED = auto()
	"""
	Both bounds are included: low <= x <= high. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([10, 15, 20])
	>>> ages.select(ndp.Between(low=10, high=20, bounds=ndp.Bounds.INCLUDED))
	Array([10, 15, 20], dtype=INT64)
	"""

	EXCLUDED = auto()
	"""
	Both bounds are excluded: low < x < high.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([10, 15, 20])
	>>> ages.select(ndp.Between(low=10, high=20, bounds=ndp.Bounds.EXCLUDED))
	Array([15], dtype=INT64)
	"""

	LOW_ONLY = auto()
	"""
	Only the low bound is included: low <= x < high.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([10, 15, 20])
	>>> ages.select(ndp.Between(low=10, high=20, bounds=ndp.Bounds.LOW_ONLY))
	Array([10, 15], dtype=INT64)
	"""

	HIGH_ONLY = auto()
	"""
	Only the high bound is included: low < x <= high.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([10, 15, 20])
	>>> ages.select(ndp.Between(low=10, high=20, bounds=ndp.Bounds.HIGH_ONLY))
	Array([15, 20], dtype=INT64)
	"""


LOW_INCLUDED_BOUNDS = frozenset({Bounds.INCLUDED, Bounds.LOW_ONLY})
"""The bounds settings that include the low bound, or the start of a sequence.

.. versionadded:: 0.1.0
"""

HIGH_INCLUDED_BOUNDS = frozenset({Bounds.INCLUDED, Bounds.HIGH_ONLY})
"""The bounds settings that include the high bound, or the end of a sequence.

.. versionadded:: 0.1.0
"""
