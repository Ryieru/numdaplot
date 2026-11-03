"""
How the columns of a Condition combine.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ColumnMatch(Enum):
	"""
	How the columns of a ``Condition`` combine to satisfy it.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.ColumnMatch.ALL
	<ColumnMatch.ALL: 2>
	"""

	ANY = auto()
	"""A row satisfies the condition when at least one of the columns satisfies the rule. Default value."""

	ALL = auto()
	"""A row satisfies the condition when every column satisfies the rule."""
