"""
A single position in one dimension.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Index:
	"""
	A single position in one dimension, used by ``Region``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		The position, starting at 0. A negative position counts from the end:
		-1 is the last one.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Index(-1)
	Index(position=-1)
	"""

	position: int
