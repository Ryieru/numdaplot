"""
Which rows of a Table a preview shows.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Side(Enum):
	"""
	Which rows of a Table a ``Preview`` shows.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Side.RANDOM
	<Side.RANDOM: 3>
	"""

	START = auto()
	"""The first rows. Default value."""

	END = auto()
	"""The last rows."""

	RANDOM = auto()
	"""Rows drawn at random, shown in the order of the Table."""
