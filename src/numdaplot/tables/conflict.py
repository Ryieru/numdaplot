"""
What to do when a file or a column already exists.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Conflict(Enum):
	"""
	What to do when a file to write or a column to add already exists.

	Used by the ``to_*`` methods of a Table and by ``NewColumn``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Conflict.REPLACE
	<Conflict.REPLACE: 2>
	"""

	ERROR = auto()
	"""Raise an error and change nothing. Default value."""

	REPLACE = auto()
	"""Replace the existing file or column."""
