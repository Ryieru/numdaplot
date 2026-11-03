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
	>>> ndp.Between(low=10, high=20, bounds=ndp.Bounds.LOW_ONLY).bounds
	<Bounds.LOW_ONLY: 3>
	"""

	INCLUDED = auto()
	"""Both bounds are included: low <= x <= high. Default value."""

	EXCLUDED = auto()
	"""Both bounds are excluded: low < x < high."""

	LOW_ONLY = auto()
	"""Only the low bound is included: low <= x < high."""

	HIGH_ONLY = auto()
	"""Only the high bound is included: low < x <= high."""
